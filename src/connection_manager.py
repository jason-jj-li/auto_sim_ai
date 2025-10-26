"""Connection management for LLM providers."""
from typing import Dict, List, Optional, Tuple
from .llm_client import LMStudioClient
from .validators import InputValidator
from .logging_config import get_logger

logger = get_logger("connection_manager")


class ConnectionManager:
    """Manages connections to LLM providers."""
    
    PROVIDERS = {
        "Local (LM Studio)": {
            "default_url": "http://127.0.0.1:1234/v1",
            "requires_api_key": False,
            "info": "LM Studio runs models locally on your machine."
        },
        "DeepSeek": {
            "default_url": "https://api.deepseek.com/v1",
            "requires_api_key": True,
            "info": "💡 DeepSeek offers affordable API access. Get your API key at: https://platform.deepseek.com"
        },
        "OpenAI": {
            "default_url": "https://api.openai.com/v1",
            "requires_api_key": True,
            "info": "💡 Using OpenAI API. Get your API key at: https://platform.openai.com/api-keys"
        },
        "Custom OpenAI-Compatible": {
            "default_url": "https://api.example.com/v1",
            "requires_api_key": False,
            "info": "Enter your custom OpenAI-compatible API endpoint."
        }
    }
    
    @staticmethod
    def get_provider_info(provider: str) -> Dict[str, str]:
        """Get information about a provider."""
        return ConnectionManager.PROVIDERS.get(provider, {})
    
    @staticmethod
    def validate_connection_params(
        provider: str,
        base_url: str,
        api_key: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Validate connection parameters.
        
        Args:
            provider: Provider name
            base_url: API base URL
            api_key: Optional API key
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate URL
        is_valid, error = InputValidator.validate_url(base_url)
        if not is_valid:
            return False, error
        
        # Check if API key is required
        provider_info = ConnectionManager.get_provider_info(provider)
        if provider_info.get("requires_api_key", False):
            if not api_key:
                return False, f"API key is required for {provider}"
            
            is_valid, error = InputValidator.validate_api_key(api_key)
            if not is_valid:
                return False, error
        
        return True, ""
    
    @staticmethod
    def test_connection(
        base_url: str,
        api_key: Optional[str] = None,
        provider: str = "Local (LM Studio)"
    ) -> Tuple[bool, str, Optional[LMStudioClient], List[str]]:
        """
        Test connection to LLM provider.
        
        Args:
            base_url: API base URL
            api_key: Optional API key
            provider: Provider name for logging
            
        Returns:
            Tuple of (success, message, client, models)
        """
        logger.info(f"Testing connection to {provider} at {base_url}")
        
        try:
            # Create client
            client = LMStudioClient(
                base_url=base_url,
                api_key=api_key if api_key else None
            )
            
            # Test connection
            success, message = client.test_connection()
            
            if not success:
                logger.warning(f"Connection failed: {message}")
                return False, message, None, []
            
            # Get models
            models = client.get_available_models()
            
            if not models:
                logger.warning("Connected but no models found")
                return False, "Connected but no models loaded", client, []
            
            logger.info(f"Connection successful. Found {len(models)} models")
            return True, message, client, models
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Connection error: {error_msg}", exc_info=True)
            return False, f"Connection failed: {error_msg}", None, []
    
    @staticmethod
    def select_model(
        models: List[str],
        manual_model: Optional[str] = None
    ) -> Optional[str]:
        """
        Select a model from available models.
        
        Args:
            models: List of available models
            manual_model: Manually specified model name (takes priority)
            
        Returns:
            Selected model name or None
        """
        if manual_model:
            # Validate manual model name
            is_valid, _ = InputValidator.validate_model_name(manual_model)
            if is_valid:
                logger.info(f"Using manually specified model: {manual_model}")
                return manual_model
        
        # Auto-select first available model
        if models:
            logger.info(f"Auto-selected model: {models[0]}")
            return models[0]
        
        return None
    
    @staticmethod
    def get_troubleshooting_message(error_msg: str, provider: str) -> str:
        """
        Get troubleshooting guidance based on error message.
        
        Args:
            error_msg: Error message
            provider: Provider name
            
        Returns:
            Troubleshooting message
        """
        error_lower = error_msg.lower()
        
        if "502" in error_msg or "bad gateway" in error_lower:
            return """
**🔴 502 Error - Server Not Running**

**Fix:**
1. ✅ Open LM Studio application
2. ✅ Click the **"Local Server"** tab (↔️ icon on left)
3. ✅ Click **"Start Server"** button
4. ✅ Wait for "Server running on http://localhost:1234"
5. ✅ Make sure a model is loaded
6. ✅ Test connection again
"""
        
        elif "connection refused" in error_lower or "failed to connect" in error_lower:
            if provider == "Local (LM Studio)":
                return """
**Connection Refused**

**Fix:**
1. ✅ Is LM Studio running?
2. ✅ Is the server started in "Local Server" tab?
3. ✅ Using the right port? (default: 1234)
"""
            else:
                return """
**Connection Refused**

**Fix:**
1. ✅ Check your internet connection
2. ✅ Verify the API URL is correct
3. ✅ Check if API key is valid
"""
        
        elif "timeout" in error_lower:
            return """
**Connection Timeout**

**Fix:**
1. ✅ Wait for service to fully start
2. ✅ Check firewall settings
3. ✅ Verify the URL is correct
4. ✅ Check your internet connection
"""
        
        elif "unauthorized" in error_lower or "401" in error_msg:
            return """
**Unauthorized - Invalid API Key**

**Fix:**
1. ✅ Check your API key is correct
2. ✅ Ensure no extra spaces in the key
3. ✅ Verify the key hasn't expired
4. ✅ Check you have access to the API
"""
        
        else:
            if provider == "Local (LM Studio)":
                return """
**Troubleshooting Steps:**

1. Open LM Studio application
2. Load a model from the library
3. Go to "Local Server" tab
4. Click "Start Server"
5. Wait for server to fully start
6. Test connection again
"""
            else:
                return """
**Troubleshooting Steps:**

1. Verify API URL is correct
2. Check API key is valid
3. Ensure you have internet access
4. Try again in a few moments
"""
    
    @staticmethod
    def get_model_placeholder(provider: str) -> str:
        """Get placeholder text for model input based on provider."""
        placeholders = {
            "DeepSeek": "e.g., deepseek-chat, deepseek-coder",
            "OpenAI": "e.g., gpt-4, gpt-3.5-turbo, gpt-4o",
            "Local (LM Studio)": "e.g., llama-2-7b-chat, mistral-7b-instruct",
            "Custom OpenAI-Compatible": "e.g., model-name"
        }
        return placeholders.get(provider, "e.g., model-name")

