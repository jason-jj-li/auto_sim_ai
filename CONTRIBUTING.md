# Contributing to LLM Simulation Survey System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Setting Up Your Development Environment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auto_sim
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # Install runtime dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Run tests to verify setup**
   ```bash
   pytest
   ```

## Code Standards

### Style Guide

We follow PEP 8 with some modifications:
- Line length: 100 characters (not 79)
- Use `black` for code formatting
- Use `isort` for import sorting

### Code Formatting

Before committing, format your code:

```bash
# Format with black
black src/ tests/ pages/ app.py

# Sort imports
isort src/ tests/ pages/ app.py
```

Or simply commit and let pre-commit hooks handle it automatically.

### Type Hints

- Use type hints for function arguments and return values
- Use `typing` module for complex types
- Example:
  ```python
  from typing import List, Dict, Optional
  
  def process_personas(personas: List[Persona]) -> Dict[str, Any]:
      """Process a list of personas and return results."""
      ...
  ```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description of function.
    
    Longer description if needed, explaining the function's purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
    """
    ...
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_persona.py

# Run specific test
pytest tests/test_persona.py::TestPersona::test_persona_creation

# Run only fast tests (exclude integration)
pytest -m "not integration"
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files as `test_<module>.py`
- Name test classes as `Test<Feature>`
- Name test functions as `test_<what_is_being_tested>`
- Use fixtures from `conftest.py` for common setups
- Aim for >80% code coverage for new code

Example test structure:

```python
"""Tests for new feature."""
import pytest
from src.module import Feature


class TestFeature:
    """Test Feature class."""
    
    def test_feature_creation(self):
        """Test creating a feature instance."""
        feature = Feature(param="value")
        assert feature.param == "value"
    
    def test_feature_method(self, sample_fixture):
        """Test feature method with fixture."""
        result = sample_fixture.method()
        assert result is not None
```

## Project Structure

```
auto_sim/
├── src/                    # Core backend modules
│   ├── __init__.py
│   ├── llm_client.py      # LLM API client
│   ├── persona.py         # Persona management
│   ├── simulation.py      # Simulation engine
│   ├── storage.py         # Results storage
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── pages/                 # Streamlit UI pages
│   ├── 1_Setup.py
│   ├── 2_Simulation.py
│   └── 3_Results.py
├── tests/                 # Test suite
├── data/                  # Data storage
│   ├── personas/
│   ├── results/
│   └── cache/
├── docs/                  # Documentation
├── app.py                 # Main application entry point
└── requirements.txt       # Dependencies
```

## Making Changes

### Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes**
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Run tests and linters**
   ```bash
   pytest
   black src/ tests/ pages/
   pylint src/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```
   
   Use conventional commits:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `test:` Adding/updating tests
   - `refactor:` Code refactoring
   - `style:` Formatting changes
   - `chore:` Maintenance tasks

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Guidelines

- Provide a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Keep PRs focused (one feature/fix per PR)

## Adding New Features

### Adding a New Module

1. Create the module in `src/`
2. Export it in `src/__init__.py`
3. Add tests in `tests/test_<module>.py`
4. Update documentation

### Adding a New UI Page

1. Create page in `pages/` as `N_PageName.py` (N = order number)
2. Add navigation button in `app.py`
3. Follow existing page structure
4. Test UI functionality manually

### Adding a New Survey Template

1. Add template to `src/survey_templates.py`
2. Add to `SurveyTemplateLibrary`
3. Add scoring method to `src/scoring.py` if applicable
4. Test with sample personas

## Code Review Process

All contributions go through code review:

1. Automated checks run on PR
   - Tests must pass
   - Code must be formatted
   - Coverage shouldn't decrease

2. Manual review by maintainers
   - Code quality
   - Design decisions
   - Documentation completeness

3. Address review feedback
   - Make requested changes
   - Discuss design decisions if needed

4. Merge after approval

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version, etc.)
- Error messages or logs
- Screenshots if relevant

### Feature Requests

Include:
- Clear description of the feature
- Use case / motivation
- Proposed implementation (if any)
- Examples of similar features elsewhere

## Getting Help

- Check existing documentation
- Search existing issues
- Ask questions in discussions
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Git commit history

Thank you for contributing! 🎉

