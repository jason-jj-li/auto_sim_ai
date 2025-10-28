# Development Configuration

Development tools, testing, and code quality configuration for Auto Sim AI.

## 📦 Configuration Files

This folder contains:
- `pyproject.toml` - Project metadata and build configuration
- `pytest.ini` - Test runner configuration
- `.pre-commit-config.yaml` - Git pre-commit hooks
- `.pylintrc` - Code quality rules
- `env.example` - Environment variables template

---

## 🔧 Environment Setup

### Create `.env` File

```bash
# Copy template to project root
cp docs/development/env.example .env

# Edit with your API keys
nano .env
```

### Example `.env` Content

```env
# DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_key_here

# OpenAI API
OPENAI_API_KEY=your_openai_key_here

# LM Studio (local)
LLM_BASE_URL=http://127.0.0.1:1234/v1
LLM_MODEL=local-model

# Performance
ENABLE_CACHE=true
MAX_CONCURRENT=10
```

---

## 🧪 Testing

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

Installs:
- pytest - Testing framework
- pytest-asyncio - Async test support
- pytest-cov - Coverage reporting
- pytest-mock - Mocking support
- black - Code formatter
- pylint - Linter
- mypy - Type checker
- pre-commit - Git hooks

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_persona.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_simulation"
```

### Test Configuration (`pytest.ini`)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=html
    --cov-report=term-missing
```

---

## 🎨 Code Formatting

### Black

Auto-format Python code:

```bash
# Format all files
black src/ tests/

# Check without modifying
black --check src/

# Format specific file
black src/persona.py
```

### Configuration in `pyproject.toml`

```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
```

---

## 🔍 Code Quality

### Pylint

Check code quality:

```bash
# Lint all source code
pylint src/

# Lint specific file
pylint src/persona.py

# Generate report
pylint src/ --output-format=text > pylint_report.txt
```

### Configuration (`.pylintrc`)

Custom rules for:
- Line length limits
- Naming conventions
- Import order
- Complexity thresholds

---

## 🔖 Type Checking

### Mypy

Static type checking:

```bash
# Check all files
mypy src/

# Check specific file
mypy src/persona.py

# Strict mode
mypy --strict src/
```

---

## 🪝 Pre-commit Hooks

### Setup

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install
```

### Configuration (`.pre-commit-config.yaml`)

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

### Usage

```bash
# Run manually on all files
pre-commit run --all-files

# Run on staged files (automatic before commit)
git commit -m "Your message"
```

---

## 📦 Project Metadata (`pyproject.toml`)

```toml
[project]
name = "auto-sim-ai"
version = "2.0.0"
description = "LLM-powered survey simulation system"
requires-python = ">=3.8"
authors = [
    {name = "Jason JJ Li", email = "jason-jj-li@outlook.com"}
]

[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"
```

---

## 🔧 Development Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Write Code

Follow style guidelines:
- Use type hints
- Write docstrings
- Keep functions focused
- Follow PEP 8

### 4. Write Tests

```python
# tests/test_your_feature.py
import pytest
from src import YourFeature

def test_your_feature():
    feature = YourFeature()
    result = feature.do_something()
    assert result == expected_value
```

### 5. Run Quality Checks

```bash
# Format code
black src/ tests/

# Run linter
pylint src/

# Type checking
mypy src/

# Run tests
pytest --cov=src tests/
```

### 6. Commit

```bash
git add .
git commit -m "feat: add your feature description"
# Pre-commit hooks run automatically
```

### 7. Push and Create PR

```bash
git push origin feature/your-feature-name
# Create Pull Request on GitHub
```

---

## 📊 Coverage Reports

### Generate HTML Coverage Report

```bash
pytest --cov=src --cov-report=html tests/
```

View in browser:
```bash
open htmlcov/index.html
```

### Coverage Targets

- **Overall**: > 80%
- **Critical modules**: > 90%
- **New code**: 100%

---

## 🐛 Debugging

### Using Python Debugger

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint (Python 3.7+)
breakpoint()
```

### Debug in VS Code

Add to `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v", "tests/"]
    }
  ]
}
```

---

## 📚 Related Documentation

- [Contributing Guide](../contributing/README.md) - Contribution workflow
- [API Reference](../api/README.md) - API documentation
- [Quick Start](../quickstart/README.md) - Get started

---

**Development Tools Version**: 2.0  
**Last Updated**: 2025-01
