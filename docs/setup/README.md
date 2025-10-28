# Setup & Installation Files

This folder contains all the files needed to set up and install the LLM Simulation Survey System.

## 📦 Files

### `requirements.txt`
Main Python dependencies for running the application.

**Install with:**
```bash
pip install -r requirements.txt
```

**Key dependencies:**
- `streamlit` - Web UI framework
- `requests` - HTTP client for API calls
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `aiohttp` - Async HTTP client
- `nest-asyncio` - Nested event loop support

---

### `requirements-dev.txt`
Additional dependencies for development and testing.

**Install with:**
```bash
pip install -r requirements-dev.txt
```

**Includes:**
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `black` - Code formatter
- `flake8` - Linter
- `mypy` - Type checker
- `pre-commit` - Git hooks

---

### `env.example`
Environment variable template file.

**Usage:**
1. Copy to `.env`:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` with your settings:
   ```bash
   # LLM Configuration
   LLM_BASE_URL=http://127.0.0.1:1234/v1
   LLM_API_KEY=your-api-key-here
   LLM_MODEL=deepseek-chat
   
   # API Provider (lmstudio, deepseek, openai, custom)
   API_PROVIDER=lmstudio
   
   # Performance
   ENABLE_CACHE=true
   ENABLE_PARALLEL=false
   MAX_WORKERS=5
   ```

**Variables:**
- `LLM_BASE_URL` - API endpoint URL
- `LLM_API_KEY` - API authentication key
- `LLM_MODEL` - Model name to use
- `API_PROVIDER` - Provider type
- `ENABLE_CACHE` - Enable response caching
- `ENABLE_PARALLEL` - Enable parallel execution
- `MAX_WORKERS` - Number of parallel workers

---

### `setup.sh`
Automated setup script for Unix/Linux/macOS.

**Usage:**
```bash
chmod +x setup.sh
./setup.sh
```

**What it does:**
1. Checks Python version (requires 3.8+)
2. Creates virtual environment
3. Activates virtual environment
4. Installs dependencies
5. Creates `.env` from template
6. Sets up data directories

**Manual equivalent:**
```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env.example .env

# Create data directories
mkdir -p data/personas data/results data/cache data/checkpoints
```

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
./setup.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # Unix/macOS
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp env.example .env
# Edit .env with your settings

# 5. Run the application
streamlit run app.py
```

---

## 🔧 Development Setup

For contributors and developers:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black .

# Run linter
flake8 src/ tests/

# Type check
mypy src/
```

---

## 📋 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 2GB free space
- **Network**: Internet connection for cloud APIs (optional for local LLM)

---

## 🐳 Docker Setup (Optional)

If you prefer Docker:

```bash
# Build image
docker build -t llm-simulation .

# Run container
docker run -p 8501:8501 -v $(pwd)/data:/app/data llm-simulation
```

---

## 🆘 Troubleshooting

### Python version issues
```bash
# Check Python version
python3 --version

# If too old, install newer version
# macOS: brew install python@3.11
# Ubuntu: sudo apt install python3.11
```

### Permission errors
```bash
# Make setup.sh executable
chmod +x setup.sh

# Or run with bash
bash setup.sh
```

### Virtual environment issues
```bash
# Remove old venv
rm -rf venv

# Create new one
python3 -m venv venv
```

### Dependency conflicts
```bash
# Upgrade pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Related Documentation

- [Quickstart Guide](../quickstart/README.md) - Complete getting started guide
- [Contributing Guide](../contributing/README.md) - Development guidelines
- [API Guide](../api/README.md) - API documentation

---

**Last Updated**: October 28, 2024
