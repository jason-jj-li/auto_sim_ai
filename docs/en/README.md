# Auto Sim AI Documentation

**Language / 语言:** [English](../en/README.md) | [中文](../zh/README.md)

---

## Welcome to Auto Sim AI

Auto Sim AI is an LLM-based automated survey simulation system that uses large language models to simulate survey respondents, helping researchers predict survey results and optimize survey design.

## 📖 Documentation Navigation

### 🚀 Getting Started
- **[Quick Start Guide](quickstart/README.md)** - Installation, configuration, and first simulation
- **[Setup Guide](setup/README.md)** - Environment setup and configuration

### 👥 For Contributors
- **[Contributing Guide](contributing/README.md)** - Contribution guidelines and development workflow
- **[Development Tools](development/README.md)** - Development environment configuration (pytest, pre-commit, linting)

### 🔧 For Developers
- **[API Reference](api/README.md)** - Complete API documentation
- **[Architecture Guide](architecture/README.md)** - System design and module architecture
- **[Code Examples](examples/)** - Practical code examples

### 📊 For Researchers
- **[Longitudinal Study Guide](longitudinal/README.md)** - Multi-wave longitudinal study implementation

## 🗂️ Complete Documentation Structure

```
docs/
├── README.md                    # This file (Documentation index)
├── zh/                          # Chinese documentation
├── en/                          # English documentation (current)
│
├── quickstart/                  # Quick start guide
│   └── README.md               # Installation and basic usage
│
├── contributing/                # Contribution guidelines
│   └── README.md               # How to contribute
│
├── api/                         # API documentation
│   └── README.md               # Complete API reference
│
├── architecture/                # Architecture documentation
│   └── README.md               # System design and module structure
│
├── longitudinal/                # Longitudinal study guide
│   └── README.md               # Multi-wave study implementation
│
├── examples/                    # Code examples
│   └── longitudinal_study_demo.py
│
├── development/                 # Development configuration
│   ├── README.md               # Development tools guide
│   ├── pyproject.toml          # Project metadata
│   ├── pytest.ini              # Test configuration
│   ├── .pre-commit-config.yaml # Pre-commit hooks
│   ├── .pylintrc               # Linting rules
│   └── env.example             # Environment variables template
│
└── setup/                       # Installation guide
    └── README.md               # Installation steps
```

## 🎯 Quick Access

### I'm a new user, I want to...
- **Run my first simulation** → [Quick Start Guide](quickstart/README.md)
- **Understand how the system works** → [Architecture Guide](architecture/README.md)
- **Check available APIs** → [API Reference](api/README.md)

### I'm a developer, I want to...
- **Set up development environment** → [Development Tools](development/README.md)
- **Contribute code** → [Contributing Guide](contributing/README.md)
- **Understand the architecture** → [Architecture Guide](architecture/README.md)

### I'm a researcher, I want to...
- **Conduct longitudinal studies** → [Longitudinal Study Guide](longitudinal/README.md)
- **View code examples** → [Code Examples](examples/)
- **Understand the API** → [API Reference](api/README.md)

## 💡 Tips

1. **First time?** Start with the [Quick Start Guide](quickstart/README.md)
2. **Need API details?** Check the [API Reference](api/README.md)
3. **Want to contribute?** Read the [Contributing Guide](contributing/README.md)
4. **Studying development?** Browse the [Code Examples](examples/)

## 📝 Documentation Version

This documentation reflects the latest version of Auto Sim AI with:
- ✅ Longitudinal study support (multi-wave studies)
- ✅ Async LLM client for high-performance simulations
- ✅ Survey/Message Testing/A/B Testing modes
- ✅ 20 core modules with 100% UI coverage
- ❌ Removed unused features (statistical analysis, export, sensitivity analysis, etc.)

---

**Last Updated:** 2025-01

**Project Repository:** [GitHub](https://github.com/yourusername/auto_sim_ai)
