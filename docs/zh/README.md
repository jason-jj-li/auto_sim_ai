# Auto Sim AI 文档中心

**语言 / Language:** [中文](../zh/README.md) | [English](../en/README.md)

---

## 欢迎使用 Auto Sim AI

Auto Sim AI 是一个基于大语言模型的自动化问卷模拟系统，通过大语言模型模拟问卷受访者，帮助研究人员预测问卷结果并优化问卷设计。

## 📖 文档导航

### 🚀 新手入门
- **[快速开始指南](quickstart/README.md)** - 安装、配置和首次模拟
- **[AI智能虚拟人群生成教程](AI_PERSONA_GENERATION.md)** 🆕 - 使用AI生成虚拟人群的综合指南
- **[安装配置指南](setup/README.md)** - 环境搭建和配置

### 👥 贡献者指南
- **[贡献指南](contributing/README.md)** - 贡献流程和开发规范
- **[开发工具](development/README.md)** - 开发环境配置（pytest、pre-commit、代码检查）

### 🔧 开发者文档
- **[API 参考](api/README.md)** - 完整 API 文档
- **[架构指南](architecture/README.md)** - 系统设计和模块架构
- **[代码示例](examples/)** - 实用代码示例

### 📊 研究者指南
- **[纵向研究指南](longitudinal/README.md)** - 多波次纵向研究实现

## 🗂️ 完整文档结构

```
docs/
├── README.md                    # 本文件（文档索引）
├── zh/                          # 中文文档（当前）
├── en/                          # 英文文档
│
├── quickstart/                  # 快速开始
│   └── README.md               # 安装和基本使用
│
├── contributing/                # 贡献指南
│   └── README.md               # 如何贡献代码
│
├── api/                         # API 文档
│   └── README.md               # 完整 API 参考
│
├── architecture/                # 架构文档
│   └── README.md               # 系统设计和模块结构
│
├── longitudinal/                # 纵向研究指南
│   └── README.md               # 多波次研究实现
│
├── examples/                    # 代码示例
│   └── longitudinal_study_demo.py
│
├── development/                 # 开发配置
│   ├── README.md               # 开发工具指南
│   ├── pyproject.toml          # 项目元数据
│   ├── pytest.ini              # 测试配置
│   ├── .pre-commit-config.yaml # 预提交钩子
│   ├── .pylintrc               # 代码检查规则
│   └── env.example             # 环境变量模板
│
└── setup/                       # 安装指南
    └── README.md               # 安装步骤
```

## 🎯 快速访问

### 我是新用户，我想...
- **运行第一次模拟** → [快速开始指南](quickstart/README.md)
- **了解系统如何工作** → [架构指南](architecture/README.md)
- **查看可用的 API** → [API 参考](api/README.md)

### 我是开发者，我想...
- **搭建开发环境** → [开发工具](development/README.md)
- **贡献代码** → [贡献指南](contributing/README.md)
- **理解系统架构** → [架构指南](architecture/README.md)

### 我是研究者，我想...
- **进行纵向研究** → [纵向研究指南](longitudinal/README.md)
- **查看代码示例** → [代码示例](examples/)
- **理解 API** → [API 参考](api/README.md)

## 💡 小贴士

1. **第一次使用？** 从[快速开始指南](quickstart/README.md)开始
2. **需要 API 详情？** 查看 [API 参考](api/README.md)
3. **想要贡献？** 阅读[贡献指南](contributing/README.md)
4. **研究开发？** 浏览[代码示例](examples/)

## 📝 文档版本

本文档反映了 Auto Sim AI 的最新版本，包含：
- ✅ 纵向研究支持（多波次研究）
- ✅ 异步 LLM 客户端（高性能模拟）
- ✅ Survey/Message Testing/A/B Testing 三种模式
- ✅ 20 个核心模块，100% UI 覆盖
- ❌ 已移除未使用的功能（统计分析、导出、敏感性分析等）

---

**最后更新：** 2025-01

**项目仓库：** [GitHub](https://github.com/yourusername/auto_sim_ai)
