"""Shared pytest fixtures for tests."""
import pytest
from datetime import datetime
from src.persona import Persona
from src.llm_client import LMStudioClient


@pytest.fixture
def sample_persona():
    """Create a sample persona for testing."""
    return Persona(
        name="Test Person",
        age=30,
        gender="Female",
        occupation="Software Engineer",
        background="A passionate developer with 5 years of experience",
        personality_traits=["Analytical", "Creative", "Curious"],
        values=["Innovation", "Learning", "Collaboration"],
        education="Bachelor's in Computer Science",
        location="San Francisco, CA"
    )


@pytest.fixture
def sample_personas():
    """Create multiple sample personas for testing."""
    return [
        Persona(
            name="Alice Johnson",
            age=28,
            gender="Female",
            occupation="Teacher",
            background="Elementary school teacher",
            personality_traits=["Patient", "Caring"],
            values=["Education", "Empathy"]
        ),
        Persona(
            name="Bob Smith",
            age=45,
            gender="Male",
            occupation="Engineer",
            background="Mechanical engineer",
            personality_traits=["Analytical", "Practical"],
            values=["Efficiency", "Quality"]
        ),
        Persona(
            name="Carol Davis",
            age=35,
            gender="Female",
            occupation="Doctor",
            background="Emergency room physician",
            personality_traits=["Decisive", "Compassionate"],
            values=["Health", "Service"]
        )
    ]


@pytest.fixture
def sample_persona_dict():
    """Create a sample persona dictionary for testing."""
    return {
        "name": "Test Person",
        "age": 30,
        "gender": "Female",
        "occupation": "Software Engineer",
        "background": "A passionate developer with 5 years of experience",
        "personality_traits": ["Analytical", "Creative", "Curious"],
        "values": ["Innovation", "Learning", "Collaboration"],
        "education": "Bachelor's in Computer Science",
        "location": "San Francisco, CA"
    }


@pytest.fixture
def sample_questions():
    """Create sample survey questions for testing."""
    return [
        "How do you feel about technology?",
        "What are your career goals?",
        "How do you handle stress?"
    ]


@pytest.fixture
def mock_llm_client(monkeypatch):
    """Create a mock LLM client for testing."""
    class MockLLMClient:
        def __init__(self, base_url="http://localhost:1234/v1", api_key=None):
            self.base_url = base_url
            self.api_key = api_key
            
        def test_connection(self):
            return True, "Mock connection successful"
        
        def get_available_models(self):
            return ["mock-model-1", "mock-model-2"]
        
        def chat_completion(self, messages, model=None, temperature=0.7, max_tokens=500, tools=None):
            # Return a mock response
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": "This is a mock response for testing purposes."
                    }
                }]
            }
    
    return MockLLMClient()


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory for testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create subdirectories
    (data_dir / "personas").mkdir()
    (data_dir / "results").mkdir()
    
    return data_dir

