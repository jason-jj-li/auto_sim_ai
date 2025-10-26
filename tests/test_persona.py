"""Tests for persona management."""
import pytest
import json
import os
from src.persona import Persona, PersonaManager


class TestPersona:
    """Test Persona class."""
    
    def test_persona_creation(self, sample_persona):
        """Test creating a persona."""
        assert sample_persona.name == "Test Person"
        assert sample_persona.age == 30
        assert sample_persona.gender == "Female"
        assert sample_persona.occupation == "Software Engineer"
    
    def test_persona_to_dict(self, sample_persona):
        """Test converting persona to dictionary."""
        persona_dict = sample_persona.to_dict()
        
        assert isinstance(persona_dict, dict)
        assert persona_dict['name'] == "Test Person"
        assert persona_dict['age'] == 30
        assert 'personality_traits' in persona_dict
        assert isinstance(persona_dict['personality_traits'], list)
    
    def test_persona_from_dict(self, sample_persona_dict):
        """Test creating persona from dictionary."""
        persona = Persona.from_dict(sample_persona_dict)
        
        assert persona.name == sample_persona_dict['name']
        assert persona.age == sample_persona_dict['age']
        assert persona.occupation == sample_persona_dict['occupation']
    
    def test_persona_get_context(self, sample_persona):
        """Test getting persona context string."""
        context = sample_persona.get_context()
        
        assert isinstance(context, str)
        assert sample_persona.name in context
        assert str(sample_persona.age) in context
        assert sample_persona.occupation in context
    
    def test_persona_equality(self, sample_persona_dict):
        """Test persona equality comparison."""
        persona1 = Persona.from_dict(sample_persona_dict)
        persona2 = Persona.from_dict(sample_persona_dict)
        
        # Same data should create equal personas
        assert persona1.name == persona2.name
        assert persona1.age == persona2.age


class TestPersonaManager:
    """Test PersonaManager class."""
    
    def test_manager_initialization(self, temp_data_dir):
        """Test PersonaManager initialization."""
        manager = PersonaManager(str(temp_data_dir / "personas"))
        assert manager.personas_dir == str(temp_data_dir / "personas")
    
    def test_save_and_load_persona(self, temp_data_dir, sample_persona):
        """Test saving and loading a persona."""
        manager = PersonaManager(str(temp_data_dir / "personas"))
        
        # Save persona
        manager.save_persona(sample_persona)
        
        # Check file exists
        filename = f"{sample_persona.name.lower().replace(' ', '_')}.json"
        filepath = temp_data_dir / "personas" / filename
        assert filepath.exists()
        
        # Load persona
        loaded_personas = manager.load_all_personas()
        assert len(loaded_personas) == 1
        assert loaded_personas[0].name == sample_persona.name
    
    def test_delete_persona(self, temp_data_dir, sample_persona):
        """Test deleting a persona."""
        manager = PersonaManager(str(temp_data_dir / "personas"))
        
        # Save and then delete
        manager.save_persona(sample_persona)
        assert len(manager.load_all_personas()) == 1
        
        manager.delete_persona(sample_persona.name)
        assert len(manager.load_all_personas()) == 0
    
    def test_load_all_personas(self, temp_data_dir, sample_personas):
        """Test loading multiple personas."""
        manager = PersonaManager(str(temp_data_dir / "personas"))
        
        # Save multiple personas
        for persona in sample_personas:
            manager.save_persona(persona)
        
        # Load all
        loaded = manager.load_all_personas()
        assert len(loaded) == len(sample_personas)
    
    def test_persona_exists(self, temp_data_dir, sample_persona):
        """Test checking if persona exists."""
        manager = PersonaManager(str(temp_data_dir / "personas"))
        
        # Initially doesn't exist
        assert not manager.persona_exists(sample_persona.name)
        
        # After saving, exists
        manager.save_persona(sample_persona)
        assert manager.persona_exists(sample_persona.name)
    
    def test_invalid_persona_file(self, temp_data_dir):
        """Test handling invalid persona JSON files."""
        manager = PersonaManager(str(temp_data_dir / "personas"))
        
        # Create invalid JSON file
        invalid_file = temp_data_dir / "personas" / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("{ invalid json }")
        
        # Should not crash, just skip invalid file
        personas = manager.load_all_personas()
        assert isinstance(personas, list)

