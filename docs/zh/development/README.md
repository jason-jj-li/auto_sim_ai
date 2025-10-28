# Development Configuration Files

This folder contains configuration files for development tools, testing, and code quality.

## 📦 Files Overview

- **`pyproject.toml`** - Python project metadata and build configuration
- **`pytest.ini`** - Pytest test runner configuration
- **`.pre-commit-config.yaml`** - Git pre-commit hooks
- **`.pylintrc`** - Pylint code quality rules
- **`env.example`** - Environment variables template

---

## 🔧 Environment Setup

### Setting up `.env` file

Copy `env.example` to the project root as `.env`:

```bash
cp docs/development/env.example .env
```

Then edit `.env` and add your API keys:

```env
# DeepSeek API (if using)
DEEPSEEK_API_KEY=your_key_here

# OpenAI API (if using)
OPENAI_API_KEY=your_key_here

# Other providers as needed
```

---

## 📦 Files

### `pyproject.toml`

Project metadata and build configuration following PEP 518.

**Purpose:**
- Package metadata (name, version, author)
- Build system configuration
- Tool-specific settings (Black, isort, etc.)

**Key sections:**

```toml
[project]
name = "llm-simulation-survey"
version = "1.0.0"
description = "LLM-powered survey simulation system"
requires-python = ">=3.8"

[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.isort]
profile = "black"
line_length = 100
```

---

### `pytest.ini`

Configuration for pytest testing framework.

**Purpose:**
- Test discovery settings
- Test execution options
- Coverage configuration
- Warning filters

**Key settings:**

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
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

**Usage:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_persona.py

# Run with coverage
pytest --cov=src

# Run only unit tests
pytest -m unit

# Run tests in parallel
pytest -n auto
```

---

### `.pre-commit-config.yaml`

Pre-commit hooks configuration for automated code quality checks.

**Purpose:**
- Automatic code formatting before commits
- Lint checking
- Import sorting
- Trailing whitespace removal
- YAML/JSON validation

**Hooks configured:**
- **Black** - Code formatter
- **Flake8** - Style guide enforcement
- **isort** - Import sorting
- **mypy** - Static type checking
- **trailing-whitespace** - Remove trailing spaces
- **end-of-file-fixer** - Ensure files end with newline
- **check-yaml** - YAML syntax validation
- **check-json** - JSON syntax validation

**Setup:**
```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

**Manual run:**
```bash
# Format code with Black
black src/ tests/

# Sort imports
isort src/ tests/

# Run flake8
flake8 src/ tests/

# Type check
mypy src/
```

---

### `.pylintrc`

Configuration for Pylint code analysis tool.

**Purpose:**
- Code quality checks
- Style enforcement
- Error detection
- Refactoring suggestions

**Key settings:**
- Max line length: 100
- Max function arguments: 8
- Max local variables: 20
- Disabled checks: C0111 (missing docstring for short functions)
- Good variable names: i, j, k, x, y, z, id, df, db

**Usage:**
```bash
# Run pylint on specific files
pylint src/persona.py

# Run on entire package
pylint src/

# Generate reports
pylint src/ --output-format=html > pylint_report.html

# Run with specific config
pylint --rcfile=.pylintrc src/
```

---

## 🔧 Development Workflow

### 1. Initial Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install
```

### 2. Before Coding

```bash
# Create feature branch
git checkout -b feature/my-feature

# Ensure environment is up to date
pip install -r requirements-dev.txt
```

### 3. During Development

```bash
# Auto-format on save (configure in IDE)
# Or manually:
black src/ tests/
isort src/ tests/

# Run tests frequently
pytest tests/test_my_module.py

# Type check
mypy src/my_module.py
```

### 4. Before Committing

Pre-commit hooks will automatically run. If they fail:

```bash
# Fix formatting issues
black src/ tests/

# Fix import order
isort src/ tests/

# Review and fix linting issues
flake8 src/ tests/

# Run tests
pytest
```

### 5. Before Push

```bash
# Run full test suite
pytest

# Run all pre-commit hooks
pre-commit run --all-files

# Check coverage
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

---

## 🧪 Testing Configuration

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_persona.py          # Persona tests
├── test_llm_client.py       # LLM client tests
├── test_simulation.py       # Simulation tests
├── test_storage.py          # Storage tests
└── test_validators.py       # Validator tests
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_persona.py

# Specific test function
pytest tests/test_persona.py::test_persona_creation

# With coverage
pytest --cov=src --cov-report=html

# Parallel execution
pytest -n auto

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

### Test Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

---

## 📊 Code Quality Tools

### Black (Code Formatter)

```bash
# Format all code
black .

# Check without modifying
black --check .

# Specific directories
black src/ tests/
```

**Configuration** (in `pyproject.toml`):
- Line length: 100
- Target Python: 3.8+

### isort (Import Sorter)

```bash
# Sort imports
isort .

# Check only
isort --check-only .

# Diff mode
isort --diff .
```

**Configuration**:
- Profile: black (compatible with Black)
- Line length: 100

### Flake8 (Linter)

```bash
# Check code
flake8 src/ tests/

# Ignore specific errors
flake8 --ignore=E501,W503 src/

# Generate report
flake8 --format=html --htmldir=flake-report src/
```

**Common error codes**:
- E501: Line too long
- W503: Line break before binary operator
- F401: Module imported but unused
- E302: Expected 2 blank lines

### Mypy (Type Checker)

```bash
# Type check
mypy src/

# Strict mode
mypy --strict src/

# Specific file
mypy src/persona.py
```

**Configuration**:
- Python version: 3.8
- Strict optional: True
- Warn unused ignores: True

---

## 🎯 Code Quality Standards

### Minimum Requirements

- ✅ All tests pass
- ✅ Coverage ≥ 80%
- ✅ No Flake8 errors
- ✅ Black formatting applied
- ✅ isort formatting applied
- ✅ Type hints on public functions
- ✅ Docstrings on public classes/functions

### Best Practices

- Write tests before code (TDD)
- Keep functions small (<50 lines)
- Use type hints
- Write descriptive docstrings
- Avoid global state
- Follow PEP 8 style guide
- Use meaningful variable names

---

## 🔄 Continuous Integration

When pushing to GitHub, CI will run:

1. **Linting**: Black, Flake8, isort
2. **Type Checking**: Mypy
3. **Tests**: Full test suite
4. **Coverage**: Ensure ≥ 80%

**Local CI simulation:**
```bash
# Run all checks locally
pre-commit run --all-files && pytest --cov=src
```

---

## 📚 Related Documentation

- [Contributing Guide](../contributing/README.md) - How to contribute
- [API Guide](../api/README.md) - API documentation
- [Architecture](../architecture/README.md) - System design

---

**Last Updated**: October 28, 2024
