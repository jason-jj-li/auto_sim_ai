"""Tests for LLM client."""
import pytest
from src.llm_client import LMStudioClient


class TestLMStudioClient:
    """Test LMStudioClient class."""
    
    def test_client_initialization_local(self):
        """Test client initialization with local URL."""
        client = LMStudioClient(base_url="http://localhost:1234/v1")
        
        assert client.base_url == "http://localhost:1234/v1"
        assert client.is_local is True
        assert client.api_key is not None  # Should have default
    
    def test_client_initialization_online(self):
        """Test client initialization with online API."""
        client = LMStudioClient(
            base_url="https://api.openai.com/v1",
            api_key="sk-test-key"
        )
        
        assert client.base_url == "https://api.openai.com/v1"
        assert client.is_local is False
        assert client.api_key == "sk-test-key"
    
    def test_client_default_api_key(self):
        """Test that local client gets default API key."""
        client = LMStudioClient(base_url="http://localhost:1234/v1")
        
        # Should have default key for local
        assert client.api_key == "lm-studio"
    
    def test_client_custom_api_key(self):
        """Test client with custom API key."""
        custom_key = "custom-api-key-123"
        client = LMStudioClient(
            base_url="http://localhost:1234/v1",
            api_key=custom_key
        )
        
        assert client.api_key == custom_key
    
    def test_base_url_normalization(self):
        """Test that base URL is handled correctly."""
        # With /v1
        client1 = LMStudioClient(base_url="http://localhost:1234/v1")
        assert client1.base_url == "http://localhost:1234/v1"
        
        # Without /v1 - should still work
        client2 = LMStudioClient(base_url="http://localhost:1234")
        assert client2.base_url == "http://localhost:1234"


class TestLLMClientValidation:
    """Test LLM client input validation."""
    
    def test_empty_base_url(self):
        """Test handling of empty base URL."""
        # Should not crash, just set the value
        client = LMStudioClient(base_url="")
        assert client.base_url == ""
    
    def test_various_url_formats(self):
        """Test various URL formats."""
        urls = [
            "http://localhost:1234/v1",
            "http://127.0.0.1:1234/v1",
            "https://api.openai.com/v1",
            "https://api.deepseek.com/v1",
        ]
        
        for url in urls:
            client = LMStudioClient(base_url=url)
            assert client.base_url == url


# Note: These tests don't make actual API calls
# Integration tests with real API calls should be in a separate file
# and marked with @pytest.mark.integration

