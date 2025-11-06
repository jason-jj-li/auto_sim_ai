"""Persona management for simulation."""
import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class Persona:
    """Represents a simulated person with background and characteristics."""
    
    name: str
    age: int
    gender: str
    occupation: str
    background: str
    personality_traits: List[str]
    values: List[str]
    education: Optional[str] = None
    location: Optional[str] = None
    marital_status: Optional[str] = None
    ethnicity: Optional[str] = None
    political_affiliation: Optional[str] = None
    religion: Optional[str] = None
    
    # Store any additional dynamic attributes
    _extra_attributes: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize extra attributes dictionary."""
        if self._extra_attributes is None:
            object.__setattr__(self, '_extra_attributes', {})
    
    def __setattr__(self, name: str, value: Any):
        """Allow setting dynamic attributes."""
        # Check if it's a defined field
        if name in self.__dataclass_fields__ or name == '_extra_attributes':
            object.__setattr__(self, name, value)
        else:
            # Store in extra attributes
            if not hasattr(self, '_extra_attributes') or self._extra_attributes is None:
                object.__setattr__(self, '_extra_attributes', {})
            if self._extra_attributes is not None:
                self._extra_attributes[name] = value
    
    def __getattr__(self, name: str):
        """Allow getting dynamic attributes."""
        if '_extra_attributes' in self.__dict__ and self._extra_attributes is not None and name in self._extra_attributes:
            return self._extra_attributes[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert persona to dictionary, including extra attributes."""
        result = asdict(self)
        # Remove internal _extra_attributes field
        if '_extra_attributes' in result:
            extra = result.pop('_extra_attributes')
            if extra:
                result.update(extra)
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Persona':
        """Create persona from dictionary, handling extra fields."""
        # Separate known fields from extra fields
        known_fields = set(cls.__dataclass_fields__.keys()) - {'_extra_attributes'}
        known_data = {k: v for k, v in data.items() if k in known_fields}
        extra_data = {k: v for k, v in data.items() if k not in known_fields}
        
        # Create instance with known fields
        instance = cls(**known_data)
        
        # Add extra attributes
        if extra_data:
            for key, value in extra_data.items():
                setattr(instance, key, value)
        
        return instance
    
    def to_prompt_context(self, use_json_format: bool = True) -> str:
        """
        Generate a context string for LLM prompts.
        
        Args:
            use_json_format: If True, includes structured JSON data for better LLM processing
        """
        if use_json_format:
            # Create structured JSON representation
            import json
            import re
            
            # Parse background to extract structured information
            persona_data = {
                "name": self.name,
                "age": self.age,
                "gender": self.gender,
                "occupation": self.occupation
            }
            
            # Add structured fields
            if self.education:
                persona_data["education"] = self.education
            if self.location:
                persona_data["location"] = self.location
            if self.personality_traits:
                persona_data["personality_traits"] = self.personality_traits
            if self.values:
                persona_data["values"] = self.values
            
            # Parse background text to extract additional structured data
            if self.background:
                background_dict = {}
                # Split by periods or newlines and parse key-value pairs
                statements = re.split(r'[.\n]+', self.background)
                for statement in statements:
                    statement = statement.strip()
                    if ':' in statement:
                        key, value = statement.split(':', 1)
                        key = key.strip().lower().replace(' ', '_')
                        value = value.strip()
                        if key and value and key not in ['name', 'age', 'gender', 'occupation']:
                            background_dict[key] = value
                    elif statement:
                        # If no colon, add as general info
                        if 'additional_info' not in background_dict:
                            background_dict['additional_info'] = []
                        if isinstance(background_dict['additional_info'], list):
                            background_dict['additional_info'].append(statement)
                        else:
                            background_dict['additional_info'] = [background_dict['additional_info'], statement]
                
                # Merge background data into persona_data
                persona_data.update(background_dict)
            
            # Create a comprehensive summary
            background_summary = self.background if self.background else "No additional background information"
            
            context = f"""You are roleplaying as the following person. Here is your complete profile in structured JSON format:

```json
{json.dumps(persona_data, indent=2)}
```

**CRITICAL INSTRUCTIONS:**
1. You MUST use ALL the information in the JSON above when forming your response
2. Your responses should reflect ALL aspects of your profile including:
   - Your demographic information (age: {self.age}, gender: {self.gender})
   - Your occupation and related experiences: {self.occupation}
   - ALL background details provided in the JSON (income, marital status, children, health, education, location, etc.)
   - Your personality traits: {', '.join(self.personality_traits) if self.personality_traits else 'Not specified'}
   - Your core values: {', '.join(self.values) if self.values else 'Not specified'}

3. Consider how EACH piece of information in your profile affects your perspective, attitudes, and responses
4. Be authentic and natural - respond as this person would, drawing from their complete life context

Your background summary: {background_summary}

Respond to the following as this person would, staying in character."""
        else:
            # Original text format
            context = f"""You are roleplaying as {self.name}, a {self.age}-year-old {self.gender} who works as a {self.occupation}.

Background: {self.background}

Personality Traits: {', '.join(self.personality_traits) if self.personality_traits else 'None specified'}
Core Values: {', '.join(self.values) if self.values else 'None specified'}"""
            
            if self.education:
                context += f"\nEducation: {self.education}"
            if self.location:
                context += f"\nLocation: {self.location}"
                
            context += "\n\nRespond to the following as this person would, staying in character and drawing on their background, personality, and values. Be authentic and natural in your response."
        
        return context


class PersonaManager:
    """Manages loading, saving, and creating personas."""
    
    def __init__(self, personas_dir: str = "data/personas"):
        """
        Initialize persona manager.
        
        Args:
            personas_dir: Directory to store persona JSON files
        """
        self.personas_dir = Path(personas_dir)
        self.personas_dir.mkdir(parents=True, exist_ok=True)
    
    def save_persona(self, persona: Persona) -> bool:
        """
        Save persona to JSON file.
        
        Args:
            persona: Persona to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filename = f"{persona.name.lower().replace(' ', '_')}.json"
            filepath = self.personas_dir / filename
            with open(filepath, 'w') as f:
                json.dump(persona.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving persona: {str(e)}")
            return False
    
    def load_persona(self, filename: str) -> Optional[Persona]:
        """
        Load persona from JSON file.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            Persona object or None if error
        """
        try:
            filepath = self.personas_dir / filename
            with open(filepath, 'r') as f:
                data = json.load(f)
            return Persona.from_dict(data)
        except Exception as e:
            print(f"Error loading persona: {str(e)}")
            return None
    
    def load_all_personas(self) -> List[Persona]:
        """
        Load all personas from the personas directory.
        
        Returns:
            List of Persona objects
        """
        personas = []
        for filepath in self.personas_dir.glob("*.json"):
            persona = self.load_persona(filepath.name)
            if persona:
                personas.append(persona)
        return personas
    
    def delete_persona(self, filename: str) -> bool:
        """
        Delete a persona file.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = self.personas_dir / filename
            filepath.unlink()
            return True
        except Exception as e:
            print(f"Error deleting persona: {str(e)}")
            return False
    
    def get_persona_files(self) -> List[str]:
        """
        Get list of persona filenames.
        
        Returns:
            List of filenames
        """
        return [f.name for f in self.personas_dir.glob("*.json")]

