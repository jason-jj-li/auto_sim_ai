"""Survey configuration management for storing and loading survey designs."""
import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from .survey_templates import QuestionMetadata, SurveySection, SurveyTemplate


@dataclass
class SurveyConfig:
    """Complete survey configuration including metadata, sections, and settings."""
    
    # Metadata
    title: str
    description: str = ""
    purpose: str = ""
    time_reference: str = ""
    estimated_minutes: int = 5
    
    # Survey structure
    sections: List[SurveySection] = field(default_factory=list)
    
    # Instructions
    pre_survey_text: str = ""
    instructions: str = ""
    post_survey_text: str = ""
    
    # Response format settings
    global_response_format: Optional[Dict[str, Any]] = None
    per_question_formats: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    
    # Scoring configuration
    scoring_info: Dict[str, Any] = field(default_factory=dict)
    
    # Template info (if loaded from template)
    template_name: str = ""
    template_version: str = ""
    
    # Timestamps
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def get_all_questions(self) -> List[QuestionMetadata]:
        """Get all questions from all sections."""
        questions = []
        for section in self.sections:
            questions.extend(section.questions)
        return questions
    
    def get_question_texts(self) -> List[str]:
        """Get list of question texts only."""
        return [q.text for q in self.get_all_questions()]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SurveyConfig':
        """Create SurveyConfig from dictionary."""
        # Reconstruct sections with QuestionMetadata objects
        sections_data = data.get('sections', [])
        sections = []
        for section_dict in sections_data:
            questions = [
                QuestionMetadata(**q) for q in section_dict.get('questions', [])
            ]
            sections.append(SurveySection(
                title=section_dict.get('title', ''),
                description=section_dict.get('description', ''),
                questions=questions
            ))
        
        # Create config
        config = cls(
            title=data.get('title', ''),
            description=data.get('description', ''),
            purpose=data.get('purpose', ''),
            time_reference=data.get('time_reference', ''),
            estimated_minutes=data.get('estimated_minutes', 5),
            sections=sections,
            pre_survey_text=data.get('pre_survey_text', ''),
            instructions=data.get('instructions', ''),
            post_survey_text=data.get('post_survey_text', ''),
            global_response_format=data.get('global_response_format'),
            per_question_formats=data.get('per_question_formats', {}),
            scoring_info=data.get('scoring_info', {}),
            template_name=data.get('template_name', ''),
            template_version=data.get('template_version', ''),
            created_at=data.get('created_at', datetime.now().isoformat()),
            modified_at=data.get('modified_at', datetime.now().isoformat())
        )
        
        return config
    
    @classmethod
    def from_template(cls, template: SurveyTemplate) -> 'SurveyConfig':
        """Create SurveyConfig from a survey template."""
        return cls(
            title=template.name,
            description=template.description,
            time_reference=template.time_reference,
            estimated_minutes=template.estimated_minutes,
            sections=template.sections.copy(),
            instructions=template.instructions,
            scoring_info=template.scoring_info.copy(),
            template_name=template.name,
            template_version=template.version
        )
    
    def update_modified_time(self):
        """Update the modified_at timestamp."""
        self.modified_at = datetime.now().isoformat()


class SurveyConfigManager:
    """Manages saving, loading, and deleting survey configurations."""
    
    def __init__(self, config_dir: str = "data/survey_configs"):
        """Initialize the survey config manager.
        
        Args:
            config_dir: Directory to store survey configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def save_config(self, config: SurveyConfig, name: str) -> bool:
        """Save a survey configuration.
        
        Args:
            config: SurveyConfig object to save
            name: Name for the configuration file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            config.update_modified_time()
            filename = f"{self._sanitize_filename(name)}.json"
            filepath = self.config_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving survey config: {e}")
            return False
    
    def load_config(self, name: str) -> Optional[SurveyConfig]:
        """Load a survey configuration.
        
        Args:
            name: Name of the configuration (without .json extension)
            
        Returns:
            SurveyConfig object if found, None otherwise
        """
        try:
            filename = f"{self._sanitize_filename(name)}.json"
            filepath = self.config_dir / filename
            
            if not filepath.exists():
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return SurveyConfig.from_dict(data)
        except Exception as e:
            print(f"Error loading survey config: {e}")
            return None
    
    def list_configs(self) -> List[Dict[str, str]]:
        """List all available survey configurations.
        
        Returns:
            List of dictionaries with config info (name, title, description, modified date)
        """
        configs = []
        
        try:
            for filepath in self.config_dir.glob("*.json"):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    configs.append({
                        'name': filepath.stem,
                        'title': data.get('title', 'Untitled'),
                        'description': data.get('description', ''),
                        'modified': data.get('modified_at', ''),
                        'template': data.get('template_name', ''),
                        'questions': len([q for s in data.get('sections', []) for q in s.get('questions', [])])
                    })
                except:
                    continue
            
            # Sort by modified date (newest first)
            configs.sort(key=lambda x: x['modified'], reverse=True)
        except Exception as e:
            print(f"Error listing configs: {e}")
        
        return configs
    
    def delete_config(self, name: str) -> bool:
        """Delete a survey configuration.
        
        Args:
            name: Name of the configuration to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filename = f"{self._sanitize_filename(name)}.json"
            filepath = self.config_dir / filename
            
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting config: {e}")
            return False
    
    def config_exists(self, name: str) -> bool:
        """Check if a configuration exists.
        
        Args:
            name: Name of the configuration
            
        Returns:
            True if exists, False otherwise
        """
        filename = f"{self._sanitize_filename(name)}.json"
        filepath = self.config_dir / filename
        return filepath.exists()
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Sanitize a filename by removing invalid characters.
        
        Args:
            name: Original name
            
        Returns:
            Sanitized filename
        """
        # Replace spaces and special characters
        name = name.lower().strip()
        name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
        return name

