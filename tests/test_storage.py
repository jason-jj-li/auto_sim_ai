"""Tests for results storage."""
import pytest
import json
import os
from datetime import datetime
from src.storage import ResultsStorage
from src.simulation import SimulationResult


class TestResultsStorage:
    """Test ResultsStorage class."""
    
    def test_storage_initialization(self, temp_data_dir):
        """Test storage initialization."""
        storage = ResultsStorage(str(temp_data_dir / "results"))
        assert storage.results_dir == str(temp_data_dir / "results")
        assert os.path.exists(storage.results_dir)
    
    def test_save_and_load_result(self, temp_data_dir, sample_persona, sample_questions):
        """Test saving and loading a simulation result."""
        storage = ResultsStorage(str(temp_data_dir / "results"))
        
        # Create a result
        timestamp = datetime.now().isoformat()
        result = SimulationResult("survey", timestamp)
        result.questions = sample_questions
        
        # Add a response
        result.add_response(
            persona=sample_persona,
            question=sample_questions[0],
            response="I think technology is great!"
        )
        
        # Save result
        storage.save_result(result)
        
        # Load results
        results = storage.list_results()
        assert len(results) > 0
        
        # Load specific result
        loaded = storage.load_result(timestamp)
        assert loaded is not None
        assert loaded['simulation_type'] == 'survey'
        assert len(loaded['questions']) == len(sample_questions)
    
    def test_delete_result(self, temp_data_dir, sample_persona, sample_questions):
        """Test deleting a result."""
        storage = ResultsStorage(str(temp_data_dir / "results"))
        
        # Create and save a result
        timestamp = datetime.now().isoformat()
        result = SimulationResult("survey", timestamp)
        result.questions = sample_questions
        result.add_response(sample_persona, sample_questions[0], "Test response")
        
        storage.save_result(result)
        assert len(storage.list_results()) > 0
        
        # Delete result
        storage.delete_result(timestamp)
        assert len(storage.list_results()) == 0
    
    def test_list_results_empty(self, temp_data_dir):
        """Test listing results when directory is empty."""
        storage = ResultsStorage(str(temp_data_dir / "results"))
        results = storage.list_results()
        
        assert isinstance(results, list)
        assert len(results) == 0
    
    def test_list_results_multiple(self, temp_data_dir, sample_persona, sample_questions):
        """Test listing multiple results."""
        storage = ResultsStorage(str(temp_data_dir / "results"))
        
        # Create multiple results
        for i in range(3):
            timestamp = f"2024-01-{i+1:02d}T12:00:00"
            result = SimulationResult("survey", timestamp)
            result.questions = sample_questions
            result.add_response(sample_persona, sample_questions[0], f"Response {i}")
            storage.save_result(result)
        
        # List all
        results = storage.list_results()
        assert len(results) == 3
    
    def test_load_nonexistent_result(self, temp_data_dir):
        """Test loading a result that doesn't exist."""
        storage = ResultsStorage(str(temp_data_dir / "results"))
        
        # Try to load non-existent result
        result = storage.load_result("nonexistent-timestamp")
        assert result is None
    
    def test_result_file_naming(self, temp_data_dir, sample_persona):
        """Test that result files are named correctly."""
        storage = ResultsStorage(str(temp_data_dir / "results"))
        
        timestamp = "2024-01-15T10:30:00"
        result = SimulationResult("survey", timestamp)
        result.questions = ["Test question"]
        result.add_response(sample_persona, "Test question", "Test response")
        
        storage.save_result(result)
        
        # Check file exists with correct name
        expected_file = os.path.join(
            storage.results_dir,
            f"{timestamp.replace(':', '-')}.json"
        )
        assert os.path.exists(expected_file)
    
    def test_invalid_result_file(self, temp_data_dir):
        """Test handling of invalid result files."""
        storage = ResultsStorage(str(temp_data_dir / "results"))
        
        # Create an invalid JSON file
        invalid_file = os.path.join(storage.results_dir, "invalid.json")
        with open(invalid_file, 'w') as f:
            f.write("{ invalid json }")
        
        # Should not crash when listing
        results = storage.list_results()
        assert isinstance(results, list)


class TestSimulationResult:
    """Test SimulationResult class."""
    
    def test_result_creation(self):
        """Test creating a simulation result."""
        timestamp = datetime.now().isoformat()
        result = SimulationResult("survey", timestamp)
        
        assert result.simulation_type == "survey"
        assert result.timestamp == timestamp
        assert result.persona_responses == []
        assert result.questions == []
    
    def test_add_response(self, sample_persona):
        """Test adding a response to result."""
        result = SimulationResult("survey", datetime.now().isoformat())
        
        result.add_response(
            persona=sample_persona,
            question="How are you?",
            response="I'm doing well!"
        )
        
        assert len(result.persona_responses) == 1
        assert result.persona_responses[0]['persona_name'] == sample_persona.name
        assert result.persona_responses[0]['question'] == "How are you?"
        assert result.persona_responses[0]['response'] == "I'm doing well!"
    
    def test_result_to_dict(self, sample_persona, sample_questions):
        """Test converting result to dictionary."""
        timestamp = datetime.now().isoformat()
        result = SimulationResult("intervention", timestamp)
        result.questions = sample_questions
        result.intervention_text = "This is a test intervention"
        
        result.add_response(sample_persona, sample_questions[0], "Test response")
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict['simulation_type'] == 'intervention'
        assert result_dict['timestamp'] == timestamp
        assert result_dict['intervention_text'] == "This is a test intervention"
        assert len(result_dict['questions']) == len(sample_questions)
        assert len(result_dict['responses']) == 1
    
    def test_result_with_conversation_history(self, sample_persona):
        """Test result with conversation history."""
        result = SimulationResult("survey", datetime.now().isoformat())
        
        conversation = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        
        result.add_response(
            persona=sample_persona,
            question="How are you?",
            response="I'm great!",
            conversation_history=conversation
        )
        
        assert result.persona_responses[0]['conversation_history'] == conversation

