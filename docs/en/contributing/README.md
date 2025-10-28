# Contributing Guide

Thank you for your interest in contributing to Auto Sim AI! This guide will help you get started.

---

## 🌟 Ways to Contribute

- **Report Bugs** - Help us identify and fix issues
- **Suggest Features** - Share ideas for new functionality
- **Improve Documentation** - Fix typos, clarify instructions, add examples
- **Submit Code** - Fix bugs, add features, optimize performance
- **Share Research** - Tell us how you're using Auto Sim AI

---

## 🐛 Reporting Bugs

### Before Submitting

1. **Check existing issues** - Your bug might already be reported
2. **Test with latest version** - Update to the newest release
3. **Verify it's reproducible** - Can you consistently reproduce it?

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.10.5]
- Auto Sim AI version: [e.g., 2.0.0]
- LLM provider: [e.g., DeepSeek, LM Studio]

**Screenshots**
If applicable, add screenshots

**Error Messages**
```
Paste full error traceback here
```
```

---

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
What other approaches did you consider?

**Use Cases**
When would this be useful?

**Additional Context**
Any mockups, examples, or references
```

### Feature Evaluation Criteria

We prioritize features that:
- ✅ Solve common user problems
- ✅ Align with project goals (survey simulation research)
- ✅ Have clear use cases
- ✅ Can be implemented with UI support
- ❌ Don't significantly increase complexity without proportional value

---

## 🔧 Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tool (venv, conda)

### Setup Steps

```bash
# 1. Fork the repository on GitHub
# Click "Fork" button at https://github.com/jason-jj-li/auto_sim_ai

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/auto_sim_ai.git
cd auto_sim_ai

# 3. Add upstream remote
git remote add upstream https://github.com/jason-jj-li/auto_sim_ai.git

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development tools

# 6. Install pre-commit hooks
pre-commit install

# 7. Run tests to verify setup
pytest tests/
```

---

## 📝 Code Contribution Workflow

### 1. Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 2. Make Your Changes

#### Code Style

We use:
- **Black** for code formatting
- **Pylint** for linting
- **Type hints** for better code clarity

```python
# Good example
def generate_persona(
    age: int,
    gender: str,
    occupation: str
) -> Persona:
    """
    Generate a persona with specified attributes.
    
    Args:
        age: Person's age
        gender: Person's gender
        occupation: Person's occupation
        
    Returns:
        Persona: Generated persona object
    """
    return Persona(age=age, gender=gender, occupation=occupation)
```

#### Testing

- **Write tests** for new features
- **Update tests** when modifying existing code
- **Ensure all tests pass** before submitting

```python
# tests/test_persona.py
import pytest
from src import Persona

def test_persona_creation():
    """Test basic persona creation."""
    persona = Persona(
        name="Test User",
        age=30,
        gender="Male"
    )
    assert persona.name == "Test User"
    assert persona.age == 30
    
def test_persona_to_dict():
    """Test persona serialization."""
    persona = Persona(name="Test", age=25)
    persona_dict = persona.to_dict()
    assert isinstance(persona_dict, dict)
    assert persona_dict["name"] == "Test"
```

#### Documentation

- **Add docstrings** to all functions and classes
- **Update README** if adding user-facing features
- **Update API docs** for new APIs
- **Include examples** for complex features

### 3. Run Quality Checks

```bash
# Format code
black src/ tests/

# Run linter
pylint src/

# Type checking
mypy src/

# Run tests
pytest tests/

# Check test coverage
pytest --cov=src tests/
```

### 4. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add persona batch generation

- Implement PersonaGenerator.generate_batch() method
- Add tests for batch generation
- Update API documentation
- Closes #123"
```

#### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat: add async LLM client for parallel processing

- Implement AsyncLLMClient class
- Add generate_batch() method for concurrent requests
- Add tests and documentation
- Improves simulation speed by 5-10x

Closes #45
```

```
fix: resolve persona serialization error

- Fix JSON encoding for personality_traits list
- Add validation for required fields
- Add regression test

Fixes #67
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Go to GitHub and click "Create Pull Request"
```

#### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for new features
- [ ] Updated existing tests

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No linting errors

## Screenshots (if applicable)

## Related Issues
Closes #issue_number
```

---

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── conftest.py              # Pytest fixtures
├── test_llm_client.py       # LLM client tests
├── test_persona.py          # Persona tests
├── test_simulation.py       # Simulation engine tests
├── test_storage.py          # Storage tests
└── test_validators.py       # Validation tests
```

### Writing Tests

```python
import pytest
from src import SimulationEngine, Persona

@pytest.fixture
def sample_persona():
    """Fixture providing a sample persona."""
    return Persona(
        name="Test User",
        age=30,
        gender="Male",
        occupation="Engineer"
    )

@pytest.fixture
def mock_llm_client(mocker):
    """Fixture providing a mocked LLM client."""
    mock_client = mocker.Mock()
    mock_client.generate.return_value = "Sample response"
    return mock_client

def test_simulation_basic(sample_persona, mock_llm_client):
    """Test basic simulation functionality."""
    engine = SimulationEngine(llm_client=mock_llm_client)
    results = engine.run_simulation(personas=[sample_persona])
    
    assert len(results) == 1
    assert results[0]["persona_name"] == "Test User"
    
def test_simulation_error_handling(mock_llm_client):
    """Test simulation error handling."""
    mock_llm_client.generate.side_effect = Exception("LLM Error")
    engine = SimulationEngine(llm_client=mock_llm_client)
    
    with pytest.raises(SimulationError):
        engine.run_simulation(personas=[sample_persona])
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_persona.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v

# Run tests matching a pattern
pytest -k "test_simulation"
```

---

## 📚 Documentation Guidelines

### Code Documentation

```python
def calculate_intervention_effect(
    baseline_scores: list[float],
    followup_scores: list[float],
    alpha: float = 0.05
) -> dict:
    """
    Calculate the effect of an intervention using paired t-test.
    
    This function compares baseline and follow-up scores to determine
    if there is a statistically significant change after an intervention.
    
    Args:
        baseline_scores: List of scores at baseline (T0)
        followup_scores: List of scores at follow-up (T1)
        alpha: Significance level for hypothesis testing (default: 0.05)
        
    Returns:
        dict: Dictionary containing:
            - mean_change: Average change from baseline to follow-up
            - effect_size: Cohen's d effect size
            - p_value: Statistical significance
            - significant: Boolean indicating if result is significant
            
    Raises:
        ValueError: If baseline and followup lengths don't match
        
    Example:
        >>> baseline = [3.2, 3.5, 3.1, 3.8]
        >>> followup = [4.1, 4.3, 3.9, 4.5]
        >>> result = calculate_intervention_effect(baseline, followup)
        >>> print(result['mean_change'])
        0.875
        >>> print(result['significant'])
        True
    """
    if len(baseline_scores) != len(followup_scores):
        raise ValueError("Baseline and followup must have same length")
    
    # Implementation...
```

### README Updates

When adding features, update:
- Feature list
- Usage examples
- Screenshots (if UI changed)
- Configuration options

### API Documentation

Update `docs/en/api/README.md` and `docs/zh/api/README.md` with:
- New classes and methods
- Parameters and return types
- Usage examples
- Best practices

---

## 🎯 Project Structure

```
auto_sim_ai/
├── app.py                      # Streamlit main app
├── pages/                      # Streamlit pages
│   ├── 1_Setup.py             # LLM setup
│   ├── 2_Simulation.py        # Run simulations
│   └── 3_Results.py           # View results
├── src/                        # Core modules
│   ├── llm_client.py          # LLM communication
│   ├── persona.py             # Persona management
│   ├── simulation.py          # Simulation engine
│   ├── longitudinal_study.py  # Longitudinal studies
│   ├── ab_testing.py          # A/B testing
│   ├── storage.py             # Data persistence
│   └── ...
├── tests/                      # Test suite
├── data/                       # Data storage
│   ├── personas/              # Persona definitions
│   ├── survey_configs/        # Survey configurations
│   ├── results/               # Simulation results
│   └── checkpoints/           # Saved states
├── docs/                       # Documentation
│   ├── en/                    # English docs
│   └── zh/                    # Chinese docs
└── requirements.txt           # Dependencies
```

---

## 🔍 Code Review Process

### What We Look For

1. **Functionality**
   - Does it work as intended?
   - Does it solve the stated problem?
   - Are edge cases handled?

2. **Code Quality**
   - Is the code readable and well-organized?
   - Are variable/function names clear?
   - Is there appropriate error handling?

3. **Testing**
   - Are there adequate tests?
   - Do tests cover edge cases?
   - Is test coverage maintained/improved?

4. **Documentation**
   - Are docstrings complete?
   - Is the README updated if needed?
   - Are complex sections commented?

5. **Performance**
   - Is the implementation efficient?
   - Are there any obvious bottlenecks?
   - Could it scale to larger datasets?

### Review Timeline

- **Small fixes**: Usually reviewed within 1-2 days
- **New features**: May take 3-5 days for thorough review
- **Major changes**: May require discussion before acceptance

---

## 🌐 Community Guidelines

### Code of Conduct

- **Be respectful** - Treat everyone with respect
- **Be collaborative** - Work together constructively
- **Be patient** - Remember that everyone has different experience levels
- **Be inclusive** - Welcome newcomers and diverse perspectives

### Getting Help

- **Documentation** - Check docs first
- **GitHub Issues** - Search existing issues
- **Discussions** - Ask questions in GitHub Discussions
- **Email** - Contact maintainers: jason-jj-li@outlook.com

---

## 📊 Development Tools

### Installed with requirements-dev.txt

```txt
pytest>=7.0.0              # Testing framework
pytest-cov>=4.0.0          # Coverage reporting
pytest-mock>=3.10.0        # Mocking for tests
black>=22.0.0              # Code formatting
pylint>=2.15.0             # Linting
mypy>=0.990                # Type checking
pre-commit>=2.20.0         # Git hooks
```

### Pre-commit Hooks

Configured in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        
  - repo: https://github.com/pycqa/pylint
    rev: v2.15.5
    hooks:
      - id: pylint
        
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

---

## 🏆 Recognition

Contributors will be:
- Listed in the project README
- Mentioned in release notes
- Credited in documentation (for significant contributions)

---

## 📋 Checklist for First Contribution

- [ ] Fork the repository
- [ ] Clone your fork locally
- [ ] Create a new branch
- [ ] Make your changes
- [ ] Write/update tests
- [ ] Run tests locally
- [ ] Update documentation
- [ ] Commit with clear message
- [ ] Push to your fork
- [ ] Create pull request
- [ ] Respond to review feedback

---

## 🎓 Learning Resources

### Python
- [Python Official Documentation](https://docs.python.org/3/)
- [Real Python Tutorials](https://realpython.com/)

### Testing
- [Pytest Documentation](https://docs.pytest.org/)
- [Test-Driven Development](https://testdriven.io/)

### Git
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

### Streamlit
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)

---

## 📞 Contact

- **Project Maintainer**: Jason JJ Li
- **Email**: jason-jj-li@outlook.com
- **GitHub**: [@jason-jj-li](https://github.com/jason-jj-li)
- **Issues**: [GitHub Issues](https://github.com/jason-jj-li/auto_sim_ai/issues)

---

**Thank you for contributing to Auto Sim AI! 🙏**

Every contribution, no matter how small, helps make this project better for the research community.
