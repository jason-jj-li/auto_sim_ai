"""Input validation utilities for the LLM Simulation Survey System."""
import re
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import urlparse


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class InputValidator:
    """Validates user inputs to prevent errors and security issues."""
    
    @staticmethod
    def validate_url(url: str, allowed_schemes: Optional[List[str]] = None) -> Tuple[bool, str]:
        """
        Validate a URL.
        
        Args:
            url: URL to validate
            allowed_schemes: List of allowed schemes (default: http, https)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url:
            return False, "URL cannot be empty"
        
        if allowed_schemes is None:
            allowed_schemes = ['http', 'https']
        
        try:
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in allowed_schemes:
                return False, f"Invalid URL scheme. Allowed: {', '.join(allowed_schemes)}"
            
            # Check netloc (host)
            if not parsed.netloc:
                return False, "URL must have a valid host"
            
            # Basic validation passed
            return True, ""
            
        except Exception as e:
            return False, f"Invalid URL format: {str(e)}"
    
    @staticmethod
    def validate_api_key(api_key: str, min_length: int = 10) -> Tuple[bool, str]:
        """
        Validate an API key.
        
        Args:
            api_key: API key to validate
            min_length: Minimum required length
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not api_key:
            return False, "API key cannot be empty"
        
        if len(api_key) < min_length:
            return False, f"API key too short (minimum {min_length} characters)"
        
        # Check for common patterns
        if api_key.startswith('sk-') or api_key.startswith('Bearer '):
            return True, ""
        
        # Generic validation - just check length
        if len(api_key) >= min_length:
            return True, ""
        
        return False, "Invalid API key format"
    
    @staticmethod
    def validate_persona_data(persona_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate persona data structure.
        
        Args:
            persona_data: Dictionary containing persona information
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['name', 'age', 'gender', 'occupation']
        
        # Check required fields
        for field in required_fields:
            if field not in persona_data:
                return False, f"Missing required field: {field}"
            
            if not persona_data[field]:
                return False, f"Field '{field}' cannot be empty"
        
        # Validate age
        try:
            age = int(persona_data['age'])
            if age < 0 or age > 150:
                return False, "Age must be between 0 and 150"
        except (ValueError, TypeError):
            return False, "Age must be a valid number"
        
        # Validate name (no special characters that could cause issues)
        name = persona_data['name']
        if len(name) > 100:
            return False, "Name too long (maximum 100 characters)"
        
        # Optional fields validation
        if 'personality_traits' in persona_data:
            traits = persona_data['personality_traits']
            if not isinstance(traits, list):
                return False, "personality_traits must be a list"
        
        if 'values' in persona_data:
            values = persona_data['values']
            if not isinstance(values, list):
                return False, "values must be a list"
        
        return True, ""
    
    @staticmethod
    def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize text input to prevent injection attacks.
        
        Args:
            text: Text to sanitize
            max_length: Maximum allowed length (optional)
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Remove null bytes
        text = text.replace('\0', '')
        
        # Limit length if specified
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        # Remove control characters except newlines and tabs
        text = ''.join(char for char in text if char == '\n' or char == '\t' or char.isprintable())
        
        return text.strip()
    
    @staticmethod
    def validate_temperature(temperature: float) -> Tuple[bool, str]:
        """
        Validate temperature parameter.
        
        Args:
            temperature: Temperature value
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            temp = float(temperature)
            if temp < 0.0 or temp > 2.0:
                return False, "Temperature must be between 0.0 and 2.0"
            return True, ""
        except (ValueError, TypeError):
            return False, "Temperature must be a valid number"
    
    @staticmethod
    def validate_max_tokens(max_tokens: int) -> Tuple[bool, str]:
        """
        Validate max_tokens parameter.
        
        Args:
            max_tokens: Maximum tokens value
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            tokens = int(max_tokens)
            if tokens < 1:
                return False, "max_tokens must be positive"
            if tokens > 32000:
                return False, "max_tokens too large (maximum 32000)"
            return True, ""
        except (ValueError, TypeError):
            return False, "max_tokens must be a valid integer"
    
    @staticmethod
    def validate_questions(questions: List[str]) -> Tuple[bool, str]:
        """
        Validate survey questions.
        
        Args:
            questions: List of question strings
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not questions:
            return False, "At least one question is required"
        
        if not isinstance(questions, list):
            return False, "Questions must be a list"
        
        for i, question in enumerate(questions, 1):
            if not question or not question.strip():
                return False, f"Question {i} is empty"
            
            if len(question) > 5000:
                return False, f"Question {i} is too long (maximum 5000 characters)"
        
        return True, ""
    
    @staticmethod
    def validate_model_name(model_name: str) -> Tuple[bool, str]:
        """
        Validate model name.
        
        Args:
            model_name: Model name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not model_name:
            return False, "Model name cannot be empty"
        
        if len(model_name) > 200:
            return False, "Model name too long (maximum 200 characters)"
        
        # Allow alphanumeric, hyphens, underscores, dots, slashes
        if not re.match(r'^[a-zA-Z0-9\-_.\/]+$', model_name):
            return False, "Model name contains invalid characters"
        
        return True, ""


# Convenience functions
def validate_and_raise(is_valid: bool, error_message: str) -> None:
    """
    Raise ValidationError if validation failed.
    
    Args:
        is_valid: Validation result
        error_message: Error message to raise
        
    Raises:
        ValidationError: If validation failed
    """
    if not is_valid:
        raise ValidationError(error_message)

