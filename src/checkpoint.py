"""Checkpoint system for saving and resuming long-running simulations."""
import json
import pickle
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Checkpoint:
    """Checkpoint data for simulation state."""
    checkpoint_id: str
    timestamp: str
    simulation_type: str
    total_personas: int
    total_questions: int
    completed_responses: int
    total_responses: int
    percent_complete: float
    
    # Simulation configuration
    personas_json: List[Dict[str, Any]]
    questions: List[str]
    temperature: float
    max_tokens: int
    survey_context: Optional[str]
    intervention_text: Optional[str]
    response_validation: Optional[Dict[str, Any]]
    survey_config: Optional[Dict[str, Any]]
    
    # Progress tracking
    completed_persona_indices: List[int]
    completed_question_indices: Dict[int, List[int]]  # persona_idx -> [question_indices]
    
    # Results accumulated so far
    partial_results: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class CheckpointManager:
    """Manages checkpoints for simulation progress."""
    
    def __init__(self, checkpoint_dir: str = "data/checkpoints"):
        """
        Initialize checkpoint manager.
        
        Args:
            checkpoint_dir: Directory for storing checkpoints
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.auto_save_frequency = 50  # Save every N responses
        self.max_checkpoints = 10  # Keep only last N checkpoints
    
    def create_checkpoint(
        self,
        simulation_type: str,
        personas: List[Any],  # List of Persona objects
        questions: List[str],
        completed_responses: List[Dict[str, Any]],
        completed_persona_indices: List[int],
        completed_question_indices: Dict[int, List[int]],
        temperature: float = 0.7,
        max_tokens: int = 500,
        survey_context: Optional[str] = None,
        intervention_text: Optional[str] = None,
        response_validation: Optional[Dict[str, Any]] = None,
        survey_config: Optional[Dict[str, Any]] = None
    ) -> Checkpoint:
        """
        Create a checkpoint of current simulation state.
        
        Args:
            simulation_type: 'survey' or 'intervention'
            personas: List of Persona objects
            questions: List of questions
            completed_responses: List of completed response dictionaries
            completed_persona_indices: List of persona indices that are fully complete
            completed_question_indices: Dict mapping persona_idx to list of completed question indices
            temperature: LLM temperature
            max_tokens: Max tokens per response
            survey_context: Optional survey context
            intervention_text: Optional intervention text
            response_validation: Optional validation rules
            survey_config: Optional survey configuration
            
        Returns:
            Checkpoint object
        """
        checkpoint_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        total_responses = len(personas) * len(questions)
        
        # Serialize personas to JSON-compatible format
        personas_json = []
        for p in personas:
            personas_json.append({
                'name': p.name,
                'age': p.age,
                'gender': p.gender,
                'occupation': p.occupation,
                'background': p.background,
                'personality_traits': p.personality_traits,
                'values': p.values
            })
        
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            timestamp=datetime.now().isoformat(),
            simulation_type=simulation_type,
            total_personas=len(personas),
            total_questions=len(questions),
            completed_responses=len(completed_responses),
            total_responses=total_responses,
            percent_complete=(len(completed_responses) / total_responses * 100) if total_responses > 0 else 0,
            personas_json=personas_json,
            questions=questions,
            temperature=temperature,
            max_tokens=max_tokens,
            survey_context=survey_context,
            intervention_text=intervention_text,
            response_validation=response_validation,
            survey_config=survey_config,
            completed_persona_indices=completed_persona_indices,
            completed_question_indices=completed_question_indices,
            partial_results=completed_responses
        )
        
        return checkpoint
    
    def save_checkpoint(self, checkpoint: Checkpoint) -> str:
        """
        Save checkpoint to disk.
        
        Args:
            checkpoint: Checkpoint to save
            
        Returns:
            Path to saved checkpoint file
        """
        filename = f"checkpoint_{checkpoint.checkpoint_id}.pkl"
        filepath = self.checkpoint_dir / filename
        
        with open(filepath, 'wb') as f:
            pickle.dump(checkpoint, f)
        
        # Save a JSON version for easy inspection
        json_filepath = self.checkpoint_dir / f"checkpoint_{checkpoint.checkpoint_id}.json"
        with open(json_filepath, 'w') as f:
            json_data = checkpoint.to_dict()
            # Remove large data from JSON (keep metadata only)
            json_data['partial_results'] = f"[{len(checkpoint.partial_results)} responses]"
            json_data['personas_json'] = f"[{len(checkpoint.personas_json)} personas]"
            json.dump(json_data, f, indent=2)
        
        # Cleanup old checkpoints
        self._cleanup_old_checkpoints()
        
        return str(filepath)
    
    def load_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """
        Load checkpoint from disk.
        
        Args:
            checkpoint_id: ID of checkpoint to load
            
        Returns:
            Checkpoint object or None if not found
        """
        filename = f"checkpoint_{checkpoint_id}.pkl"
        filepath = self.checkpoint_dir / filename
        
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'rb') as f:
                checkpoint = pickle.load(f)
            return checkpoint
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
            return None
    
    def get_latest_checkpoint(self) -> Optional[Checkpoint]:
        """
        Get the most recent checkpoint.
        
        Returns:
            Latest checkpoint or None if no checkpoints exist
        """
        checkpoints = list(self.checkpoint_dir.glob("checkpoint_*.pkl"))
        if not checkpoints:
            return None
        
        # Sort by modification time
        latest_file = max(checkpoints, key=lambda p: p.stat().st_mtime)
        checkpoint_id = latest_file.stem.replace("checkpoint_", "")
        
        return self.load_checkpoint(checkpoint_id)
    
    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """
        List all available checkpoints with metadata.
        
        Returns:
            List of checkpoint metadata dictionaries
        """
        checkpoints = []
        
        for filepath in sorted(self.checkpoint_dir.glob("checkpoint_*.pkl"), 
                              key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                checkpoint_id = filepath.stem.replace("checkpoint_", "")
                
                # Try to load JSON metadata first (faster)
                json_filepath = self.checkpoint_dir / f"checkpoint_{checkpoint_id}.json"
                if json_filepath.exists():
                    with open(json_filepath, 'r') as f:
                        metadata = json.load(f)
                else:
                    # Fallback to loading full checkpoint
                    checkpoint = self.load_checkpoint(checkpoint_id)
                    if checkpoint:
                        metadata = checkpoint.to_dict()
                    else:
                        continue
                
                checkpoints.append({
                    'checkpoint_id': checkpoint_id,
                    'timestamp': metadata['timestamp'],
                    'simulation_type': metadata['simulation_type'],
                    'percent_complete': metadata['percent_complete'],
                    'completed_responses': metadata['completed_responses'],
                    'total_responses': metadata['total_responses'],
                    'total_personas': metadata['total_personas'],
                    'total_questions': metadata['total_questions']
                })
            except Exception as e:
                print(f"Error reading checkpoint {filepath}: {e}")
                continue
        
        return checkpoints
    
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Delete a checkpoint.
        
        Args:
            checkpoint_id: ID of checkpoint to delete
            
        Returns:
            True if deleted, False if not found
        """
        pkl_file = self.checkpoint_dir / f"checkpoint_{checkpoint_id}.pkl"
        json_file = self.checkpoint_dir / f"checkpoint_{checkpoint_id}.json"
        
        deleted = False
        
        if pkl_file.exists():
            pkl_file.unlink()
            deleted = True
        
        if json_file.exists():
            json_file.unlink()
            deleted = True
        
        return deleted
    
    def clear_all_checkpoints(self):
        """Delete all checkpoints."""
        for filepath in self.checkpoint_dir.glob("checkpoint_*"):
            try:
                filepath.unlink()
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")
    
    def _cleanup_old_checkpoints(self):
        """Remove old checkpoints beyond the max limit."""
        checkpoints = sorted(
            self.checkpoint_dir.glob("checkpoint_*.pkl"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        # Keep only the most recent max_checkpoints
        for old_checkpoint in checkpoints[self.max_checkpoints:]:
            try:
                checkpoint_id = old_checkpoint.stem.replace("checkpoint_", "")
                self.delete_checkpoint(checkpoint_id)
            except Exception as e:
                print(f"Error cleaning up old checkpoint: {e}")
    
    def should_save_checkpoint(self, completed_responses: int) -> bool:
        """
        Check if we should save a checkpoint based on frequency.
        
        Args:
            completed_responses: Number of completed responses
            
        Returns:
            True if checkpoint should be saved
        """
        return completed_responses % self.auto_save_frequency == 0
