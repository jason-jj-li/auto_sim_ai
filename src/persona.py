"""Persona management for simulation."""
import json
import re
import hashlib
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
    persona_id: Optional[str] = None
    
    # Store any additional dynamic attributes
    _extra_attributes: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize extra attributes dictionary."""
        if self._extra_attributes is None:
            object.__setattr__(self, '_extra_attributes', {})
        if not self.persona_id:
            identity = json.dumps({
                "name": self.name,
                "age": self.age,
                "gender": self.gender,
                "occupation": self.occupation,
                "background": self.background,
            }, ensure_ascii=False, sort_keys=True)
            digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]
            object.__setattr__(self, 'persona_id', f"legacy-{digest}")
    
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

            # Sampled custom variables (e.g. life_satisfaction) are first-class profile
            # fields — the LLM should see them as structured data, not buried in prose
            if self._extra_attributes:
                persona_data.update({k: v for k, v in self._extra_attributes.items() if v is not None})
            
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

    def get_context(self) -> str:
        """Backward-compatible alias for the original public API."""
        return self.to_prompt_context()


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
            # Reuse an existing legacy filename for the same stable ID.  This
            # avoids leaving a second copy behind when an old name-based file
            # is edited after the ID migration.
            filepath = None
            for candidate in self.personas_dir.glob("*.json"):
                existing = self.load_persona(candidate.name)
                if existing and existing.persona_id == persona.persona_id:
                    filepath = candidate
                    break
            if filepath is None:
                filepath = self.personas_dir / self._filename_for_persona(persona)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(persona.to_dict(), f, indent=2, ensure_ascii=False)
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
            filepath = self._resolve_child(filename)
            with open(filepath, 'r', encoding='utf-8') as f:
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
        personas_by_id = {}
        for filepath in self.personas_dir.glob("*.json"):
            persona = self.load_persona(filepath.name)
            if persona:
                personas_by_id[persona.persona_id] = persona
        return list(personas_by_id.values())
    
    def delete_persona(self, identifier: str) -> bool:
        """
        Delete a persona file.
        
        Args:
            identifier: Persona ID, display name, or legacy JSON filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            candidates = []
            if identifier.endswith('.json'):
                try:
                    candidates.append(self._resolve_child(identifier))
                except ValueError:
                    return False

            for filepath in self.personas_dir.glob("*.json"):
                persona = self.load_persona(filepath.name)
                if persona and identifier in {persona.persona_id, persona.name}:
                    candidates.append(filepath)

            for filepath in dict.fromkeys(candidates):
                if filepath.exists():
                    filepath.unlink()
                    return True
            return False
        except Exception as e:
            print(f"Error deleting persona: {str(e)}")
            return False

    def persona_exists(self, identifier: str) -> bool:
        """Return whether a persona ID or display name already exists."""
        return any(identifier in {p.persona_id, p.name} for p in self.load_all_personas())

    @staticmethod
    def _safe_component(value: str) -> str:
        cleaned = re.sub(r'[^A-Za-z0-9._-]+', '-', str(value)).strip('.-_')
        return cleaned[:120] or 'persona'

    def _filename_for_persona(self, persona: Persona) -> str:
        return f"{self._safe_component(persona.persona_id or persona.name)}.json"

    def _resolve_child(self, filename: str) -> Path:
        """Resolve a direct child and reject absolute/path-traversal filenames."""
        root = self.personas_dir.resolve()
        candidate = (root / filename).resolve()
        if candidate.parent != root:
            raise ValueError("Persona filename escapes the personas directory")
        return candidate
    
    def get_persona_files(self) -> List[str]:
        """
        Get list of persona filenames.
        
        Returns:
            List of filenames
        """
        return [f.name for f in self.personas_dir.glob("*.json")]



_CSV_COL_ALIAS = {
    '姓名': 'name', '名字': 'name', '编号': 'id',
    '年龄': 'age', '性别': 'gender', '职业': 'occupation', '工作': 'occupation',
    '教育': 'education', '学历': 'education', '地区': 'location', '城市': 'location',
    '婚姻': 'marital_status', '民族': 'ethnicity', '宗教': 'religion',
    '背景': 'background', '简介': 'background',
}
_CSV_KNOWN = {'name', 'id', 'age', 'gender', 'occupation', 'education', 'location',
              'marital_status', 'ethnicity', 'political_affiliation', 'religion', 'background',
              'personality_traits', 'values'}


def _split_list(s: Optional[str]) -> List[str]:
    if not s:
        return []
    return [t.strip() for t in re.split(r'[,;、]', s) if t.strip()]


def _parse_age(s: Optional[str], default: int = 30) -> int:
    """'45' -> 45; '25-34' -> midpoint; anything else -> default."""
    if not s:
        return default
    m = re.match(r'^(\d+)\s*[-–~]\s*(\d+)$', s)
    if m:
        age = (int(m.group(1)) + int(m.group(2))) // 2
        return age if 0 <= age <= 120 else default
    m = re.search(r'\d+', s)
    age = int(m.group()) if m else default
    return age if 0 <= age <= 120 else default


def personas_from_dataframe(df) -> List[Persona]:
    """Build personas from ANY DataFrame — no required columns.

    Column mapping (case/space-insensitive, common Chinese aliases in _CSV_COL_ALIAS):
    name/id/age/gender/occupation/education/location/marital_status/ethnicity/
    political_affiliation/religion/background -> the matching persona field;
    personality_traits/values -> split on , ; 、 into lists; every other column is
    kept as a custom attribute (shows on the persona card and in the LLM prompt).
    """
    import pandas as pd  # local import: persona.py stays pandas-free for non-CSV users
    df = df.copy()
    df.columns = [_CSV_COL_ALIAS.get(c, c) for c in (str(c).strip().lower() for c in df.columns)]
    df = df.loc[:, ~df.columns.duplicated()]  # alias collisions (教育 + education) keep the first
    personas = []
    used_ids = set()
    for n, (_, row) in enumerate(df.iterrows(), 1):
        def val(col: str) -> Optional[str]:
            return str(row[col]).strip() if col in df.columns and pd.notna(row[col]) else None

        raw_id = val('id')
        if raw_id:
            base_id = f"csv-{hashlib.sha256(raw_id.encode('utf-8')).hexdigest()[:16]}"
        else:
            row_identity = json.dumps(
                {str(k): (None if pd.isna(v) else str(v)) for k, v in row.items()},
                ensure_ascii=False,
                sort_keys=True,
            )
            base_id = f"csv-{hashlib.sha256(row_identity.encode('utf-8')).hexdigest()[:16]}"
        persona_id = base_id
        suffix = 2
        while persona_id in used_ids:
            persona_id = f"{base_id}-{suffix}"
            suffix += 1
        used_ids.add(persona_id)

        p = Persona(
            name=val('name') or val('id') or f"Person_{n:03d}",
            age=_parse_age(val('age')),
            gender=val('gender') or 'Unknown',
            occupation=val('occupation') or 'Not specified',
            background=val('background') or '',
            personality_traits=_split_list(val('personality_traits')),
            values=_split_list(val('values')),
            persona_id=persona_id,
            **{k: v for k in ('education', 'location', 'marital_status', 'ethnicity',
                              'political_affiliation', 'religion')
               if (v := val(k)) is not None}
        )
        for col in df.columns:
            if col not in _CSV_KNOWN and (v := val(col)):
                setattr(p, col, v)  # dynamic attribute -> _extra_attributes
        personas.append(p)
    return personas
