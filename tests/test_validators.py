"""Tests for input validators."""
import pytest
from src.validators import InputValidator, ValidationError, validate_and_raise


class TestURLValidation:
    """Test URL validation."""
    
    def test_valid_http_url(self):
        """Test valid HTTP URL."""
        is_valid, msg = InputValidator.validate_url("http://localhost:1234")
        assert is_valid is True
        assert msg == ""
    
    def test_valid_https_url(self):
        """Test valid HTTPS URL."""
        is_valid, msg = InputValidator.validate_url("https://api.openai.com/v1")
        assert is_valid is True
    
    def test_empty_url(self):
        """Test empty URL."""
        is_valid, msg = InputValidator.validate_url("")
        assert is_valid is False
        assert "empty" in msg.lower()
    
    def test_invalid_scheme(self):
        """Test URL with invalid scheme."""
        is_valid, msg = InputValidator.validate_url("ftp://example.com")
        assert is_valid is False
        assert "scheme" in msg.lower()
    
    def test_url_without_host(self):
        """Test URL without host."""
        is_valid, msg = InputValidator.validate_url("http://")
        assert is_valid is False
        assert "host" in msg.lower()
    
    def test_custom_allowed_schemes(self):
        """Test URL validation with custom allowed schemes."""
        is_valid, msg = InputValidator.validate_url(
            "ws://localhost:8080",
            allowed_schemes=['ws', 'wss']
        )
        assert is_valid is True


class TestAPIKeyValidation:
    """Test API key validation."""
    
    def test_valid_openai_key(self):
        """Test valid OpenAI-style key."""
        is_valid, msg = InputValidator.validate_api_key("sk-1234567890abcdef")
        assert is_valid is True
    
    def test_valid_bearer_token(self):
        """Test valid Bearer token."""
        is_valid, msg = InputValidator.validate_api_key("Bearer abc123def456")
        assert is_valid is True
    
    def test_empty_api_key(self):
        """Test empty API key."""
        is_valid, msg = InputValidator.validate_api_key("")
        assert is_valid is False
        assert "empty" in msg.lower()
    
    def test_short_api_key(self):
        """Test API key that's too short."""
        is_valid, msg = InputValidator.validate_api_key("abc", min_length=10)
        assert is_valid is False
        assert "short" in msg.lower()
    
    def test_api_key_min_length(self):
        """Test API key with custom min length."""
        is_valid, msg = InputValidator.validate_api_key("12345", min_length=5)
        assert is_valid is True


class TestPersonaValidation:
    """Test persona data validation."""
    
    def test_valid_persona(self, sample_persona_dict):
        """Test valid persona data."""
        is_valid, msg = InputValidator.validate_persona_data(sample_persona_dict)
        assert is_valid is True
        assert msg == ""
    
    def test_missing_required_field(self):
        """Test persona missing required field."""
        persona_data = {
            "name": "Test",
            "age": 30,
            "gender": "Female"
            # Missing occupation
        }
        is_valid, msg = InputValidator.validate_persona_data(persona_data)
        assert is_valid is False
        assert "occupation" in msg.lower()
    
    def test_empty_required_field(self):
        """Test persona with empty required field."""
        persona_data = {
            "name": "",
            "age": 30,
            "gender": "Female",
            "occupation": "Teacher"
        }
        is_valid, msg = InputValidator.validate_persona_data(persona_data)
        assert is_valid is False
        assert "name" in msg.lower()
    
    def test_invalid_age(self):
        """Test persona with invalid age."""
        persona_data = {
            "name": "Test",
            "age": "not a number",
            "gender": "Female",
            "occupation": "Teacher"
        }
        is_valid, msg = InputValidator.validate_persona_data(persona_data)
        assert is_valid is False
        assert "age" in msg.lower()
    
    def test_age_out_of_range(self):
        """Test persona with age out of valid range."""
        persona_data = {
            "name": "Test",
            "age": 200,
            "gender": "Female",
            "occupation": "Teacher"
        }
        is_valid, msg = InputValidator.validate_persona_data(persona_data)
        assert is_valid is False
        assert "age" in msg.lower()
    
    def test_name_too_long(self):
        """Test persona with overly long name."""
        persona_data = {
            "name": "A" * 150,
            "age": 30,
            "gender": "Female",
            "occupation": "Teacher"
        }
        is_valid, msg = InputValidator.validate_persona_data(persona_data)
        assert is_valid is False
        assert "name" in msg.lower()
    
    def test_invalid_personality_traits_type(self):
        """Test persona with invalid personality_traits type."""
        persona_data = {
            "name": "Test",
            "age": 30,
            "gender": "Female",
            "occupation": "Teacher",
            "personality_traits": "not a list"
        }
        is_valid, msg = InputValidator.validate_persona_data(persona_data)
        assert is_valid is False
        assert "personality_traits" in msg.lower()


class TestTextSanitization:
    """Test text sanitization."""
    
    def test_sanitize_normal_text(self):
        """Test sanitizing normal text."""
        result = InputValidator.sanitize_text("Hello, world!")
        assert result == "Hello, world!"
    
    def test_sanitize_empty_text(self):
        """Test sanitizing empty text."""
        result = InputValidator.sanitize_text("")
        assert result == ""
    
    def test_remove_null_bytes(self):
        """Test removing null bytes."""
        result = InputValidator.sanitize_text("Hello\x00World")
        assert "\x00" not in result
    
    def test_limit_length(self):
        """Test limiting text length."""
        long_text = "A" * 1000
        result = InputValidator.sanitize_text(long_text, max_length=100)
        assert len(result) == 100
    
    def test_preserve_newlines(self):
        """Test preserving newlines."""
        text = "Line 1\nLine 2\nLine 3"
        result = InputValidator.sanitize_text(text)
        assert "\n" in result
    
    def test_preserve_tabs(self):
        """Test preserving tabs."""
        text = "Col1\tCol2\tCol3"
        result = InputValidator.sanitize_text(text)
        assert "\t" in result


class TestParameterValidation:
    """Test parameter validation."""
    
    def test_valid_temperature(self):
        """Test valid temperature value."""
        is_valid, msg = InputValidator.validate_temperature(0.7)
        assert is_valid is True
    
    def test_temperature_out_of_range_low(self):
        """Test temperature below valid range."""
        is_valid, msg = InputValidator.validate_temperature(-0.1)
        assert is_valid is False
    
    def test_temperature_out_of_range_high(self):
        """Test temperature above valid range."""
        is_valid, msg = InputValidator.validate_temperature(2.5)
        assert is_valid is False
    
    def test_invalid_temperature_type(self):
        """Test invalid temperature type."""
        is_valid, msg = InputValidator.validate_temperature("not a number")
        assert is_valid is False
    
    def test_valid_max_tokens(self):
        """Test valid max_tokens value."""
        is_valid, msg = InputValidator.validate_max_tokens(500)
        assert is_valid is True
    
    def test_max_tokens_negative(self):
        """Test negative max_tokens."""
        is_valid, msg = InputValidator.validate_max_tokens(-10)
        assert is_valid is False
    
    def test_max_tokens_too_large(self):
        """Test max_tokens exceeding limit."""
        is_valid, msg = InputValidator.validate_max_tokens(50000)
        assert is_valid is False


class TestQuestionValidation:
    """Test question validation."""
    
    def test_valid_questions(self, sample_questions):
        """Test valid questions list."""
        is_valid, msg = InputValidator.validate_questions(sample_questions)
        assert is_valid is True
    
    def test_empty_questions_list(self):
        """Test empty questions list."""
        is_valid, msg = InputValidator.validate_questions([])
        assert is_valid is False
        assert "required" in msg.lower()
    
    def test_questions_not_list(self):
        """Test questions that's not a list."""
        is_valid, msg = InputValidator.validate_questions("not a list")
        assert is_valid is False
        assert "list" in msg.lower()
    
    def test_empty_question_in_list(self):
        """Test list containing empty question."""
        is_valid, msg = InputValidator.validate_questions(["Valid question", ""])
        assert is_valid is False
        assert "empty" in msg.lower()
    
    def test_question_too_long(self):
        """Test question exceeding max length."""
        long_question = "A" * 6000
        is_valid, msg = InputValidator.validate_questions([long_question])
        assert is_valid is False
        assert "long" in msg.lower()


class TestModelNameValidation:
    """Test model name validation."""
    
    def test_valid_model_name(self):
        """Test valid model name."""
        is_valid, msg = InputValidator.validate_model_name("gpt-4")
        assert is_valid is True
    
    def test_valid_model_with_slash(self):
        """Test model name with slash."""
        is_valid, msg = InputValidator.validate_model_name("meta/llama-2-7b")
        assert is_valid is True
    
    def test_empty_model_name(self):
        """Test empty model name."""
        is_valid, msg = InputValidator.validate_model_name("")
        assert is_valid is False
    
    def test_model_name_too_long(self):
        """Test model name exceeding max length."""
        long_name = "A" * 250
        is_valid, msg = InputValidator.validate_model_name(long_name)
        assert is_valid is False
    
    def test_model_name_invalid_chars(self):
        """Test model name with invalid characters."""
        is_valid, msg = InputValidator.validate_model_name("model@#$%")
        assert is_valid is False


class TestValidateAndRaise:
    """Test validate_and_raise utility."""
    
    def test_valid_no_exception(self):
        """Test that valid input doesn't raise."""
        # Should not raise
        validate_and_raise(True, "")
    
    def test_invalid_raises_exception(self):
        """Test that invalid input raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_and_raise(False, "Test error message")
        
        assert "Test error message" in str(exc_info.value)

