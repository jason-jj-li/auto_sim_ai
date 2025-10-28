# Setup & Installation

Installation files and setup guide for Auto Sim AI.

## 📦 Installation Files

- `requirements.txt` - Main dependencies
- `requirements-dev.txt` - Development dependencies
- `setup.sh` - Automated setup script
- `env.example` - Environment variables template

---

## 🚀 Quick Install

### Using Setup Script (Recommended)

```bash
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai
chmod +x setup.sh
./setup.sh
streamlit run app.py
```

### Manual Installation

```bash
# 1. Clone repository
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment file
cp env.example .env

# 5. Run application
streamlit run app.py
```

---

## 📋 Dependencies

### Main Dependencies (`requirements.txt`)

```txt
streamlit>=1.32.0          # Web UI framework
requests>=2.31.0           # HTTP client
pandas>=2.2.0              # Data manipulation
numpy>=1.26.4              # Numerical computing
aiohttp>=3.9.0             # Async HTTP client
nest-asyncio>=1.5.6        # Event loop support
openai>=1.30.0             # LLM API client
plotly>=5.18.0             # Interactive charts
matplotlib>=3.8.0          # Static charts
seaborn>=0.13.0            # Statistical visualization
scipy>=1.12.0              # Scientific computing
python-dotenv>=1.0.0       # Environment variables
```

### Development Dependencies (`requirements-dev.txt`)

```txt
pytest>=7.4.0              # Testing framework
pytest-asyncio>=0.21.0     # Async test support
pytest-cov>=4.1.0          # Coverage reporting
pytest-mock>=3.11.1        # Mocking support
black>=23.7.0              # Code formatter
pylint>=2.17.0             # Linter
mypy>=1.5.0                # Type checker
pre-commit>=3.3.3          # Git hooks
flake8>=6.1.0              # Additional linter
isort>=5.12.0              # Import sorting
```

---

## ⚙️ Environment Configuration

### Environment Variables

Create `.env` file from template:

```bash
cp env.example .env
```

### Example Configuration

```env
# LLM Provider Configuration
LLM_BASE_URL=http://127.0.0.1:1234/v1
LLM_API_KEY=your-api-key-here
LLM_MODEL=deepseek-chat

# Provider Type (lmstudio, deepseek, openai, custom)
API_PROVIDER=lmstudio

# Performance Settings
ENABLE_CACHE=true
ENABLE_PARALLEL=true
MAX_WORKERS=10
MAX_CONCURRENT=10

# Storage Settings
DATA_DIR=./data
CACHE_DIR=./data/cache
RESULTS_DIR=./data/results

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

### Variables Explained

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_BASE_URL` | API endpoint URL | `http://127.0.0.1:1234/v1` |
| `LLM_API_KEY` | API authentication key | `""` |
| `LLM_MODEL` | Model name | `local-model` |
| `API_PROVIDER` | Provider type | `lmstudio` |
| `ENABLE_CACHE` | Enable response caching | `true` |
| `ENABLE_PARALLEL` | Enable parallel processing | `true` |
| `MAX_WORKERS` | Number of parallel workers | `10` |
| `MAX_CONCURRENT` | Max concurrent API calls | `10` |

---

## 🖥️ System Requirements

### Minimum Requirements

- **OS**: Windows 10+, macOS 10.15+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4 GB
- **Disk**: 2 GB free space
- **Internet**: For API-based LLMs

### Recommended Requirements

- **OS**: macOS 12+ or Ubuntu 20.04+
- **Python**: 3.10 or higher
- **RAM**: 8 GB or more
- **Disk**: 5 GB free space
- **CPU**: 4+ cores for parallel processing

### For Local LLM (LM Studio)

- **RAM**: 8-16 GB (depends on model size)
- **Disk**: 10-20 GB (for model storage)
- **GPU**: Optional but recommended for faster inference

---

## 🔧 Setup Script Details

### What `setup.sh` Does

```bash
#!/bin/bash

# 1. Check Python version (requires 3.8+)
python3 --version

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create .env file if not exists
if [ ! -f .env ]; then
    cp env.example .env
    echo "Created .env file. Please edit with your API keys."
fi

# 7. Create data directories
mkdir -p data/personas
mkdir -p data/survey_configs
mkdir -p data/results
mkdir -p data/checkpoints
mkdir -p data/cache

# 8. Display success message
echo "✅ Setup complete! Run: streamlit run app.py"
```

### Manual Equivalent

```bash
# Run these commands if setup.sh fails

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
cp env.example .env
mkdir -p data/{personas,survey_configs,results,checkpoints,cache}
```

---

## 🐳 Docker Installation (Optional)

### Using Docker

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t auto-sim-ai .

# Run container
docker run -p 8501:8501 -v $(pwd)/data:/app/data auto-sim-ai
```

---

## 🔍 Troubleshooting

### Python Version Issues

```bash
# Check Python version
python3 --version

# If < 3.8, install newer version
# macOS
brew install python@3.10

# Ubuntu
sudo apt install python3.10

# Windows
# Download from python.org
```

### Virtual Environment Issues

```bash
# If venv creation fails
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
python3 -m virtualenv venv
```

### Dependency Installation Errors

```bash
# Clear pip cache
pip cache purge

# Reinstall
pip install --no-cache-dir -r requirements.txt

# Install specific versions
pip install streamlit==1.32.0
```

### Permission Issues (macOS/Linux)

```bash
# Make setup.sh executable
chmod +x setup.sh

# Fix data directory permissions
chmod -R 755 data/
```

### Streamlit Port Already in Use

```bash
# Run on different port
streamlit run app.py --server.port 8502

# Kill process using port 8501
lsof -ti:8501 | xargs kill -9
```

---

## 🔄 Updating

### Update Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade streamlit
```

### Pull Latest Code

```bash
# Fetch and merge latest changes
git pull origin main

# Reinstall dependencies (if changed)
pip install -r requirements.txt
```

---

## 🗑️ Uninstallation

### Remove Installation

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf auto_sim_ai
```

### Remove Data Only

```bash
# Remove data but keep code
rm -rf data/results/*
rm -rf data/cache/*
rm -rf data/checkpoints/*
```

---

## 📚 Related Documentation

- [Quick Start Guide](../quickstart/README.md) - First steps
- [Development Guide](../development/README.md) - Dev setup
- [Contributing](../contributing/README.md) - Contribute

---

## 💬 Support

Having installation issues?

- Check [GitHub Issues](https://github.com/jason-jj-li/auto_sim_ai/issues)
- Read the [Quick Start Guide](../quickstart/README.md)
- Contact: jason-jj-li@outlook.com

---

**Installation Guide Version**: 2.0  
**Last Updated**: 2025-01
