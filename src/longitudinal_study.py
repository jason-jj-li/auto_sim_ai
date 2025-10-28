"""
Longitudinal Study Module with Multi-turn Conversation Memory

This module implements longitudinal intervention studies where personas maintain
conversation history across multiple waves, using DeepSeek's multi-turn dialogue
approach for more coherent and realistic responses.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import json
import asyncio
from pathlib import Path

from .persona import Persona
from .llm_client import LMStudioClient, AsyncLLMClient


@dataclass
class ConversationHistory:
    """Maintains conversation history for a persona across waves."""
    persona_name: str
    messages: List[Dict[str, str]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_system_message(self, content: str):
        """Add a system message to history."""
        self.messages.append({
            "role": "system",
            "content": content
        })
    
    def add_user_message(self, content: str):
        """Add a user message (question) to history."""
        self.messages.append({
            "role": "user",
            "content": content
        })
    
    def add_assistant_message(self, content: str):
        """Add an assistant message (response) to history."""
        self.messages.append({
            "role": "assistant",
            "content": content
        })
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages for API call."""
        return self.messages.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "persona_name": self.persona_name,
            "messages": self.messages,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationHistory':
        """Create from dictionary."""
        return cls(
            persona_name=data["persona_name"],
            messages=data.get("messages", []),
            metadata=data.get("metadata", {})
        )


@dataclass
class WaveConfig:
    """Configuration for a single wave in the longitudinal study."""
    wave_number: int
    wave_name: str
    days_from_baseline: int
    questions: List[str]
    intervention_text: Optional[str] = None
    is_intervention_wave: bool = False
    wave_context: Optional[str] = None  # Additional context for this wave
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "wave_number": self.wave_number,
            "wave_name": self.wave_name,
            "days_from_baseline": self.days_from_baseline,
            "questions": self.questions,
            "intervention_text": self.intervention_text,
            "is_intervention_wave": self.is_intervention_wave,
            "wave_context": self.wave_context
        }


@dataclass
class LongitudinalStudyConfig:
    """Configuration for the entire longitudinal study."""
    study_id: str
    study_name: str
    description: str
    waves: List[WaveConfig]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "study_id": self.study_id,
            "study_name": self.study_name,
            "description": self.description,
            "waves": [w.to_dict() for w in self.waves],
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LongitudinalStudyConfig':
        """Create from dictionary."""
        waves = [
            WaveConfig(
                wave_number=w["wave_number"],
                wave_name=w["wave_name"],
                days_from_baseline=w["days_from_baseline"],
                questions=w["questions"],
                intervention_text=w.get("intervention_text"),
                is_intervention_wave=w.get("is_intervention_wave", False),
                wave_context=w.get("wave_context")
            )
            for w in data["waves"]
        ]
        return cls(
            study_id=data["study_id"],
            study_name=data["study_name"],
            description=data["description"],
            waves=waves,
            created_at=data.get("created_at", datetime.now().isoformat())
        )


@dataclass
class WaveResult:
    """Results from a single wave."""
    wave_number: int
    wave_name: str
    persona_name: str
    responses: List[Dict[str, Any]]  # List of {question, response, timestamp}
    conversation_snapshot: List[Dict[str, str]]  # Conversation history at end of wave
    completed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "wave_number": self.wave_number,
            "wave_name": self.wave_name,
            "persona_name": self.persona_name,
            "responses": self.responses,
            "conversation_snapshot": self.conversation_snapshot,
            "completed_at": self.completed_at
        }


@dataclass
class LongitudinalStudyResult:
    """Complete results from a longitudinal study."""
    study_id: str
    study_name: str
    persona_results: Dict[str, List[WaveResult]]  # persona_name -> list of wave results
    started_at: str
    completed_at: Optional[str] = None
    
    def add_wave_result(self, result: WaveResult):
        """Add a wave result for a persona."""
        if result.persona_name not in self.persona_results:
            self.persona_results[result.persona_name] = []
        self.persona_results[result.persona_name].append(result)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "study_id": self.study_id,
            "study_name": self.study_name,
            "persona_results": {
                name: [wr.to_dict() for wr in wave_results]
                for name, wave_results in self.persona_results.items()
            },
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }


class LongitudinalStudyEngine:
    """
    Engine for running longitudinal studies with conversation memory.
    
    Key features:
    - Maintains conversation history across waves for each persona
    - Uses multi-turn dialogue approach (DeepSeek style)
    - Simulates time progression between waves
    - Supports intervention waves with memory retention
    """
    
    def __init__(
        self,
        llm_client: LMStudioClient,
        storage_dir: str = "data/longitudinal_studies"
    ):
        """
        Initialize the longitudinal study engine.
        
        Args:
            llm_client: LLM client for generating responses
            storage_dir: Directory for storing study data
        """
        self.llm_client = llm_client
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Storage for conversation histories
        self.conversation_histories: Dict[str, ConversationHistory] = {}
    
    def _initialize_persona_conversation(self, persona: Persona) -> ConversationHistory:
        """
        Initialize conversation history for a persona.
        
        Args:
            persona: The persona object
            
        Returns:
            ConversationHistory object
        """
        history = ConversationHistory(persona_name=persona.name)
        
        # Add system message with persona context
        system_prompt = f"""You are roleplaying as {persona.name}. Here is your complete profile:

Name: {persona.name}
Age: {persona.age}
Gender: {persona.gender}
Occupation: {persona.occupation}
Education: {persona.education or 'Not specified'}
Location: {persona.location or 'Not specified'}

Background: {persona.background}

Personality Traits: {', '.join(persona.personality_traits)}
Core Values: {', '.join(persona.values)}

CRITICAL INSTRUCTIONS:
1. Stay in character at ALL times
2. Answer based on YOUR background, values, and personality
3. Remember previous conversations and be consistent
4. Your responses should reflect your age, occupation, and life experiences
5. Be authentic and realistic - consider your constraints and motivations
6. Track time progression between conversations

You are participating in a longitudinal research study. You will be asked questions at different time points. Remember what you said before and maintain consistency while allowing for natural changes over time."""

        history.add_system_message(system_prompt)
        history.metadata["persona_id"] = persona.name
        history.metadata["initialized_at"] = datetime.now().isoformat()
        
        return history
    
    def _generate_wave_context(self, wave: WaveConfig) -> str:
        """
        Generate contextual prompt for a specific wave.
        
        Args:
            wave: Wave configuration
            
        Returns:
            Context string to add to conversation
        """
        context_parts = []
        
        # Time context
        if wave.days_from_baseline == 0:
            context_parts.append("This is your first survey (baseline).")
        else:
            context_parts.append(
                f"It has been {wave.days_from_baseline} days since your first survey. "
                f"Think about what might have changed in your life during this time."
            )
        
        # Wave-specific context
        if wave.wave_context:
            context_parts.append(wave.wave_context)
        
        # Intervention context
        if wave.is_intervention_wave and wave.intervention_text:
            context_parts.append(
                f"\n--- IMPORTANT INFORMATION ---\n{wave.intervention_text}\n--- END ---\n"
                "Please read the above information carefully and consider it when answering the following questions."
            )
        
        return "\n".join(context_parts)
    
    def run_wave_for_persona(
        self,
        persona: Persona,
        wave: WaveConfig,
        temperature: float = 0.7,
        max_tokens: int = 300
    ) -> WaveResult:
        """
        Run a single wave for a single persona with conversation memory.
        
        Args:
            persona: The persona object
            wave: Wave configuration
            temperature: LLM temperature
            max_tokens: Maximum tokens for response
            
        Returns:
            WaveResult object
        """
        # Get or create conversation history
        if persona.name not in self.conversation_histories:
            self.conversation_histories[persona.name] = \
                self._initialize_persona_conversation(persona)
        
        history = self.conversation_histories[persona.name]
        
        # Add wave context as user message
        wave_context = self._generate_wave_context(wave)
        history.add_user_message(f"[Wave {wave.wave_number}: {wave.wave_name}]\n{wave_context}")
        
        # Add brief acknowledgment from assistant
        acknowledgment = f"I understand. I'm ready to answer questions for Wave {wave.wave_number}."
        history.add_assistant_message(acknowledgment)
        
        # Collect responses for this wave
        wave_responses = []
        
        for question in wave.questions:
            # Add question to history
            history.add_user_message(question)
            
            # Generate response using full conversation history
            messages = history.get_messages()
            
            try:
                response = self.llm_client.generate_with_messages(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Add response to history
                history.add_assistant_message(response)
                
                # Store response
                wave_responses.append({
                    "question": question,
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                # Handle error but continue
                error_msg = f"Error generating response: {str(e)}"
                history.add_assistant_message(f"[Error: Unable to respond - {error_msg}]")
                wave_responses.append({
                    "question": question,
                    "response": f"[Error: {error_msg}]",
                    "timestamp": datetime.now().isoformat(),
                    "error": True
                })
        
        # Create wave result
        result = WaveResult(
            wave_number=wave.wave_number,
            wave_name=wave.wave_name,
            persona_name=persona.name,
            responses=wave_responses,
            conversation_snapshot=history.get_messages()
        )
        
        return result
    
    def run_study(
        self,
        config: LongitudinalStudyConfig,
        personas: List[Persona],
        temperature: float = 0.7,
        max_tokens: int = 300,
        progress_callback: Optional[Callable[[str], None]] = None,
        save_checkpoints: bool = True
    ) -> LongitudinalStudyResult:
        """
        Run complete longitudinal study for all personas.
        
        Args:
            config: Study configuration
            personas: List of personas to participate
            temperature: LLM temperature
            max_tokens: Maximum tokens per response
            progress_callback: Optional callback for progress updates
            save_checkpoints: Whether to save after each wave
            
        Returns:
            LongitudinalStudyResult object
        """
        result = LongitudinalStudyResult(
            study_id=config.study_id,
            study_name=config.study_name,
            persona_results={},
            started_at=datetime.now().isoformat()
        )
        
        total_operations = len(personas) * len(config.waves)
        completed = 0
        
        # Run each wave for each persona
        for wave in config.waves:
            if progress_callback:
                progress_callback(f"Starting Wave {wave.wave_number}: {wave.wave_name}")
            
            for persona in personas:
                if progress_callback:
                    progress_callback(
                        f"Wave {wave.wave_number} - {persona.name} "
                        f"({completed + 1}/{total_operations})"
                    )
                
                # Run wave for this persona
                wave_result = self.run_wave_for_persona(
                    persona=persona,
                    wave=wave,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Add to results
                result.add_wave_result(wave_result)
                completed += 1
            
            # Save checkpoint after each wave
            if save_checkpoints:
                self._save_checkpoint(result, wave.wave_number)
        
        result.completed_at = datetime.now().isoformat()
        
        # Save final result
        self.save_result(result)
        
        return result
    
    def _save_checkpoint(self, result: LongitudinalStudyResult, wave_number: int):
        """Save checkpoint after a wave."""
        checkpoint_path = self.storage_dir / f"{result.study_id}_checkpoint_wave_{wave_number}.json"
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
    
    def save_result(self, result: LongitudinalStudyResult):
        """Save complete study result."""
        result_path = self.storage_dir / f"{result.study_id}_final.json"
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
    
    def save_conversation_histories(self, study_id: str):
        """Save all conversation histories for a study."""
        histories_path = self.storage_dir / f"{study_id}_conversations.json"
        histories_data = {
            name: history.to_dict()
            for name, history in self.conversation_histories.items()
        }
        with open(histories_path, 'w', encoding='utf-8') as f:
            json.dump(histories_data, f, indent=2, ensure_ascii=False)
    
    def load_conversation_histories(self, study_id: str):
        """Load conversation histories for a study."""
        histories_path = self.storage_dir / f"{study_id}_conversations.json"
        if not histories_path.exists():
            return
        
        with open(histories_path, 'r', encoding='utf-8') as f:
            histories_data = json.load(f)
        
        self.conversation_histories = {
            name: ConversationHistory.from_dict(data)
            for name, data in histories_data.items()
        }


class LongitudinalStudyBuilder:
    """Builder for creating longitudinal study configurations."""
    
    @staticmethod
    def create_pre_post_study(
        study_name: str,
        baseline_questions: List[str],
        intervention_text: str,
        followup_questions: Optional[List[str]] = None,
        num_pre_waves: int = 3,
        num_post_waves: int = 5,
        days_between_waves: int = 7
    ) -> LongitudinalStudyConfig:
        """
        Create a pre-post intervention study design.
        
        Args:
            study_name: Name of the study
            baseline_questions: Questions asked at all waves
            intervention_text: Intervention content
            followup_questions: Optional additional questions post-intervention
            num_pre_waves: Number of waves before intervention (default: 3)
            num_post_waves: Number of waves after intervention (default: 5)
            days_between_waves: Days between each wave (default: 7)
            
        Returns:
            LongitudinalStudyConfig
        """
        waves = []
        wave_count = 0
        
        # Pre-intervention waves
        for i in range(num_pre_waves):
            wave_count += 1
            waves.append(WaveConfig(
                wave_number=wave_count,
                wave_name=f"Baseline {i+1}" if i > 0 else "Baseline",
                days_from_baseline=i * days_between_waves,
                questions=baseline_questions,
                wave_context=f"Pre-intervention measurement {i+1}"
            ))
        
        # Intervention wave
        wave_count += 1
        waves.append(WaveConfig(
            wave_number=wave_count,
            wave_name="Intervention",
            days_from_baseline=(num_pre_waves) * days_between_waves,
            questions=baseline_questions,
            intervention_text=intervention_text,
            is_intervention_wave=True,
            wave_context="You will now receive important information."
        ))
        
        # Post-intervention waves
        followup_qs = followup_questions or baseline_questions
        for i in range(num_post_waves):
            wave_count += 1
            waves.append(WaveConfig(
                wave_number=wave_count,
                wave_name=f"Follow-up {i+1}",
                days_from_baseline=(num_pre_waves + i + 1) * days_between_waves,
                questions=followup_qs,
                wave_context=f"Post-intervention measurement {i+1}. "
                            f"Remember the intervention from {(i+1) * days_between_waves} days ago."
            ))
        
        study_id = study_name.lower().replace(' ', '_') + '_' + datetime.now().strftime('%Y%m%d_%H%M%S')
        
        return LongitudinalStudyConfig(
            study_id=study_id,
            study_name=study_name,
            description=f"Pre-post intervention study with {num_pre_waves} pre-waves, "
                       f"1 intervention, and {num_post_waves} follow-up waves",
            waves=waves
        )
    
    @staticmethod
    def create_multiple_intervention_study(
        study_name: str,
        baseline_questions: List[str],
        interventions: List[Dict[str, Any]],  # {wave_number, text, questions}
        total_waves: int = 10,
        days_between_waves: int = 7
    ) -> LongitudinalStudyConfig:
        """
        Create a study with multiple intervention points.
        
        Args:
            study_name: Name of the study
            baseline_questions: Questions asked at all waves
            interventions: List of intervention configs
            total_waves: Total number of waves
            days_between_waves: Days between waves
            
        Returns:
            LongitudinalStudyConfig
        """
        intervention_map = {i['wave_number']: i for i in interventions}
        waves = []
        
        for wave_num in range(1, total_waves + 1):
            is_intervention = wave_num in intervention_map
            
            if is_intervention:
                intervention_data = intervention_map[wave_num]
                wave_questions = baseline_questions + intervention_data.get('questions', [])
                wave = WaveConfig(
                    wave_number=wave_num,
                    wave_name=f"Intervention {list(intervention_map.keys()).index(wave_num) + 1}",
                    days_from_baseline=(wave_num - 1) * days_between_waves,
                    questions=wave_questions,
                    intervention_text=intervention_data['text'],
                    is_intervention_wave=True,
                    wave_context=f"Intervention wave {wave_num}"
                )
            else:
                wave_name = "Baseline" if wave_num == 1 else f"Wave {wave_num}"
                wave = WaveConfig(
                    wave_number=wave_num,
                    wave_name=wave_name,
                    days_from_baseline=(wave_num - 1) * days_between_waves,
                    questions=baseline_questions,
                    wave_context=f"Regular measurement wave {wave_num}"
                )
            
            waves.append(wave)
        
        study_id = study_name.lower().replace(' ', '_') + '_' + datetime.now().strftime('%Y%m%d_%H%M%S')
        
        return LongitudinalStudyConfig(
            study_id=study_id,
            study_name=study_name,
            description=f"Multiple intervention study with {len(interventions)} intervention points",
            waves=waves
        )
