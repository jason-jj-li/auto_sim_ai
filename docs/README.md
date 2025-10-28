# 📚 Auto Sim AI Documentation / 文档中心

**Choose Your Language / 选择语言:**

- 📘 [**English Documentation**](en/README.md) - Complete documentation in English
- 📗 [**中文文档**](zh/README.md) - 完整的中文文档

---

## Quick Access / 快速访问

### 🚀 New Users / 新用户
- [Quick Start Guide (EN)](en/quickstart/README.md) | [快速开始指南 (中文)](zh/quickstart/README.md)
- [Installation Guide (EN)](en/setup/README.md) | [安装配置 (中文)](zh/setup/README.md)

### 👥 Contributors / 贡献者
- [Contributing Guide (EN)](en/contributing/README.md) | [贡献指南 (中文)](zh/contributing/README.md)
- [Development Tools (EN)](en/development/README.md) | [开发工具 (中文)](zh/development/README.md)

### 🔧 Developers / 开发者
- [API Reference (EN)](en/api/README.md) | [API 参考 (中文)](zh/api/README.md)
- [Architecture Guide (EN)](en/architecture/README.md) | [架构设计 (中文)](zh/architecture/README.md)

### 📊 Researchers / 研究者
- [Longitudinal Studies (EN)](en/longitudinal/README.md) | [纵向研究 (中文)](zh/longitudinal/README.md)
- [Code Examples (EN)](en/examples/) | [代码示例 (中文)](zh/examples/)

---

Welcome to the Auto Sim AI documentation! / 欢迎使用 Auto Sim AI 文档！

## 📖 Documentation Structure / 文档结构

### Getting Started

- **[Main README](../README.md)** - Project overview, features, and quick start
- **[Quickstart Guide](./quickstart/README.md)** - Step-by-step installation and first simulation
- **[Setup Files](./setup/README.md)** - Installation files and dependencies
- **[Contributing Guide](./contributing/README.md)** - How to contribute to this project

### Technical Documentation

- **[API Guide](./api/README.md)** - Complete API reference and usage examples
- **[Architecture](./architecture/README.md)** - System design and architecture overview
- **[Longitudinal Study Guide](./longitudinal/README.md)** - Advanced guide for multi-wave studies

### Development & Examples

- **[Examples](./examples/)** - Code examples and demos
- **[Development Configuration](./development/README.md)** - Development tools and configuration files

### Development

- **[Development Tools](./development/README.md)** - Configuration files and development workflow

## 🎯 Quick Navigation

### For New Users

1. Start with the [Main README](../README.md) to understand what this system does
2. Follow the [Quickstart Guide](./quickstart/README.md) to set up your environment
3. Run your first simulation using the UI

### For Developers

1. Read the [Architecture](./architecture/README.md) to understand the system design
2. Check the [API Guide](./api/README.md) for detailed API documentation
3. Review [Contributing Guide](./contributing/README.md) before making changes

### For Researchers

1. Understand the research designs supported in [Main README](../README.md#-research-designs)
2. Learn about longitudinal studies in [Longitudinal Study Guide](./longitudinal/README.md)
3. Explore advanced features in [API Guide](./api/README.md)

## 📂 File Organization

```
auto_sim_ai/
├── README.md                       # Project overview and main documentation
├── docs/                           # Documentation directory
│   ├── README.md                   # This file - documentation index
│   ├── quickstart/                 # Getting started guide
│   │   └── README.md
│   ├── setup/                      # Installation files
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── requirements-dev.txt
│   │   ├── env.example
│   │   └── setup.sh
│   ├── contributing/               # Contribution guidelines
│   │   └── README.md
│   ├── development/                # Development tools config
│   │   ├── README.md
│   │   ├── pyproject.toml
│   │   ├── pytest.ini
│   │   ├── .pre-commit-config.yaml
│   │   └── .pylintrc
│   ├── api/                        # API reference
│   │   └── README.md
│   ├── architecture/               # System architecture
│   │   └── README.md
│   └── longitudinal/               # Longitudinal study guide
│       └── README.md
├── src/                            # Source code
├── pages/                          # Streamlit UI pages
├── tests/                          # Test suite
└── data/                           # Data storage
```

## 🔍 What's in Each Document?

### Main README
- Project introduction and features
- Supported research designs (Survey, Message Testing, A/B Testing, Longitudinal)
- Installation instructions
- Basic usage examples
- Screenshots and demos

### Quickstart Guide
- Prerequisites and system requirements
- Step-by-step installation
- LLM setup (Local and Cloud options)
- Running your first simulation
- Troubleshooting common issues

### API Guide
- Complete API reference for all modules
- Code examples for programmatic usage
- LLM client configuration
- Persona management
- Simulation engines (Survey, Intervention, A/B Test, Longitudinal)
- Data export and analysis
- Advanced features

### Architecture
- System overview and design principles
- Module structure and dependencies
- Data flow and storage
- UI components and pages
- Extension points

### Longitudinal Study Guide
- Conversation memory system
- Multi-wave study design
- Wave configuration
- Intervention timing
- Real-world examples
- Best practices

### Contributing Guide
- Code of conduct
- Development setup
- Coding standards and style guide
- Testing requirements
- Pull request process
- Documentation guidelines

## 💡 Tips

- **Looking for a specific API?** Check [api/README.md](./api/README.md)
- **Want to understand the system?** Read [architecture/README.md](./architecture/README.md)
- **Need to run multi-wave studies?** See [longitudinal/README.md](./longitudinal/README.md)
- **Just getting started?** Follow [quickstart/README.md](./quickstart/README.md)
- **Want to contribute?** Read [contributing/README.md](./contributing/README.md)

## 🆘 Getting Help

If you can't find what you're looking for:

1. Check the [Main README](../README.md) FAQ section
2. Search through the [API Guide](./api/README.md)
3. Open an issue on GitHub
4. Review existing issues and discussions

## 📝 Documentation Standards

All documentation in this project follows these principles:
- ✅ Clear and concise language
- ✅ Code examples for every feature
- ✅ Up-to-date with current implementation
- ✅ Cross-referenced with related docs
- ✅ Includes practical use cases

---

**Last Updated**: October 28, 2024  
**Documentation Version**: 2.0  
**Project Version**: 1.0.0
