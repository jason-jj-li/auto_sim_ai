# Auto Sim AI - LLM Survey Simulation System

<div align="center">

[![English](https://img.shields.io/badge/README-English-blue?style=for-the-badge)](./docs/en/README.md)
[![中文](https://img.shields.io/badge/README-中文-red?style=for-the-badge)](./docs/zh/README.md)

**Language / 语言:** [English](#english) | [中文](#中文)

---

## English

🔬 **AI-Powered Survey and Intervention Simulation System**

Simulate real survey research and intervention effects using LLM-driven virtual personas

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

📖 **[View Full English Documentation](./docs/en/README.md)**

[Quick Start](./docs/en/quickstart/README.md) •
[Features](#features-en) •
[API Reference](./docs/en/api/README.md) •
[Contributing](./docs/en/contributing/README.md)

### Features (EN)

- **Three Research Modes**: Survey Testing, Message Testing, A/B Testing
- **Longitudinal Studies**: Multi-wave research with persona memory
- **Async Processing**: High-performance parallel simulations
- **Flexible LLM Support**: Local (LM Studio) or API (DeepSeek, OpenAI)
- **Web Interface**: User-friendly Streamlit UI
- **Complete Data Export**: CSV, JSON formats for statistical analysis

### Quick Start (EN)

```bash
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai
./setup.sh
streamlit run app.py
```

📘 **[Complete English Documentation →](./docs/en/README.md)**

---

## 中文

🔬 **基于大语言模型的调查与干预模拟系统**

使用 AI 驱动的虚拟人物模拟真实的调查研究和干预效果

📗 **[查看完整中文文档](./docs/zh/README.md)**

[快速开始](./docs/zh/quickstart/README.md) •
[功能特性](#功能特性) •
[API 参考](./docs/zh/api/README.md) •
[贡献指南](./docs/zh/contributing/README.md)

</div>

---

## 📋 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [📚 完整文档](./docs/README.md)
  - [快速开始指南](./docs/quickstart/README.md)
  - [API文档](./docs/api/README.md)
  - [架构设计](./docs/architecture/README.md)
  - [纵向研究指南](./docs/longitudinal/README.md)
  - [贡献指南](./docs/contributing/README.md)
- [常见问题](#常见问题)
- [许可证](#许可证)

---

## 🎯 项目简介

**LLM Simulation Survey System** 是一个创新的研究工具，利用大语言模型（LLM）生成虚拟人物（Personas），模拟真实人群对调查问卷和干预措施的响应。

### 适用场景

- 🏥 **健康干预研究** - 测试健康信息对不同人群的影响
- 📊 **市场调研** - 快速评估产品或服务的用户反馈
- 🎓 **教育研究** - 评估教学方法对不同学习者的效果
- 💡 **政策分析** - 预测政策对多元群体的潜在影响
- 🧪 **A/B 测试** - 比较不同方案的效果差异
- 📈 **原型验证** - 在真实调研前快速迭代设计

### 核心优势

✅ **快速迭代** - 几分钟内完成数百人的调查模拟  
✅ **成本低廉** - 无需招募真实参与者  
✅ **可重复性** - 精确控制变量，确保实验可重复  
✅ **多样化** - 轻松创建不同背景、年龄、文化的虚拟人物  
✅ **深度洞察** - 获得详细的质性和量化数据  
✅ **灵活部署** - 支持本地运行和云端API

---

## 🚀 功能特性

### 核心功能

#### 1️⃣ 虚拟人物管理
- **丰富的人物属性**：年龄、性别、职业、教育背景、性格特征、价值观等
- **批量创建**：使用人口统计分布自动生成符合真实人口的虚拟样本
- **CSV 导入/导出**：支持从Excel或数据库批量导入人物
- **演示模板**：内置多种典型人物模板，即开即用

#### 2️⃣ 多种模拟模式
- **调查模式**：运行标准化问卷（PHQ-9、GAD-7 等）
- **干预模式**：测试健康信息、广告文案等对不同人群的影响
- **A/B 测试**：同时测试多个版本，比较效果差异
- **纵向研究**：模拟多波次调查，追踪变化趋势
- **敏感性分析**：系统性测试参数变化对结果的影响

#### 3️⃣ LLM 集成
- **本地部署**：LM Studio（免费，完全私密）
- **商业API**：
  - DeepSeek（高性价比，中文优化）
  - OpenAI（GPT-4、GPT-3.5）
  - 其他 OpenAI 兼容服务
- **灵活切换**：随时更换模型或提供商

#### 4️⃣ 高级分析
- **自动评分**：内置标准化量表的自动评分系统
- **统计分析**：描述统计、相关分析、组间比较
- **一致性检查**：验证响应的内部一致性和逻辑性
- **可视化**：交互式图表、词云、分布图
- **导出功能**：CSV、JSON、Python/R 分析脚本

#### 5️⃣ 性能优化
- **并行执行**：异步处理多个人物的响应
- **智能缓存**：避免重复调用 LLM，节省时间和成本
- **断点续传**：支持暂停和恢复大规模模拟
- **进度追踪**：实时显示模拟进度和预估完成时间

---

## ⚡ 快速开始

### 系统要求

- **Python**: 3.8 或更高版本
- **内存**: 建议 8GB 以上
- **LLM 提供商**（任选其一）：
  - LM Studio（本地运行，免费）
  - DeepSeek/OpenAI API 密钥

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai
```

#### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

或使用安装脚本：
```bash
chmod +x setup.sh
./setup.sh
```

#### 3. 配置 LLM

**方式 A：本地 LM Studio（推荐用于学习和开发）**

1. 下载 [LM Studio](https://lmstudio.ai/)
2. 在 LM Studio 中下载模型：
   - 推荐：`mistral-7b-instruct`、`llama-2-7b-chat`
   - 最低：7B 参数模型
3. 启动本地服务器：
   - 点击 "Local Server" 标签
   - 选择模型
   - 点击 "Start Server"
   - 确认地址为 `http://localhost:1234`

**方式 B：在线 API（推荐用于生产环境）**

```bash
# 复制环境变量模板
cp env.example .env

# 编辑 .env 文件，添加 API 密钥
# DEEPSEEK_API_KEY=your_api_key_here
# 或
# OPENAI_API_KEY=your_api_key_here
```

#### 4. 启动应用

```bash
streamlit run app.py
```

应用将在浏览器中自动打开：`http://localhost:8501`

### 首次使用指南

1. **连接 LLM**（首页）
   - 选择 LLM 提供商
   - 测试连接
   - 等待"系统就绪"提示

2. **创建虚拟人物**（Setup 页面）
   - 点击 "Create Demo Personas" 快速创建
   - 或手动创建自定义人物
   - 或上传 CSV 批量导入

3. **运行模拟**（Simulation 页面）
   - 选择模拟类型（调查/干预）
   - 选择要参与的人物
   - 选择问卷模板或输入自定义问题
   - 点击 "Run Simulation"

4. **查看结果**（Results 页面）
   - 浏览响应数据
   - 查看统计分析
   - 导出结果用于进一步分析

---

## 📖 使用指南

### 虚拟人物设计最佳实践

#### 创建高质量人物

```python
# 好的例子：具体、详细、真实
{
    "name": "李明",
    "age": 32,
    "gender": "男",
    "occupation": "初创公司软件工程师",
    "education": "本科计算机科学",
    "location": "北京",
    "background": "在一家快速成长的科技公司工作，经常加班。最近感到工作压力大，睡眠质量下降。喜欢通过运动缓解压力，但工作繁忙常常没时间。",
    "personality_traits": ["完美主义", "责任心强", "有些焦虑"],
    "values": ["职业发展", "工作生活平衡", "家庭健康"]
}

# 不好的例子：模糊、一般化
{
    "name": "张三",
    "age": 30,
    "gender": "男",
    "occupation": "工程师",
    "background": "普通人",
    "personality_traits": ["正常"],
    "values": ["幸福"]
}
```

#### 人物多样性

确保虚拟样本反映真实人口的多样性：

- **年龄**：覆盖不同年龄段（18-80岁）
- **性别**：男、女、非二元性别
- **职业**：不同行业和职位层级
- **教育**：从高中到研究生
- **地域**：城市、农村、不同地区
- **文化背景**：不同种族、宗教、文化传统

### 问卷设计技巧

#### 好的问题特征

✅ **清晰具体**
```
好：在过去两周内，您有多少天感到情绪低落或沮丧？
差：您最近心情怎么样？
```

✅ **避免复合问题**
```
好：您每周锻炼多少次？您每次锻炼多长时间？
差：您多久锻炼一次，每次多长时间，什么强度？
```

✅ **使用标准化量表**
```
从不(0) - 偶尔(1) - 经常(2) - 总是(3)
```

#### 使用内置模板

系统内置多个验证过的标准化量表：

- **PHQ-9**：抑郁症筛查量表
- **GAD-7**：焦虑症筛查量表
- **PSS-10**：压力感知量表
- 更多模板持续添加中...

### 模拟设置优化

#### 温度参数（Temperature）

控制响应的随机性和创造性：

- **0.0 - 0.3**：高度一致，适合需要标准化响应的场景
- **0.5 - 0.7**：平衡模式，推荐用于大多数调查（默认）
- **0.8 - 1.0**：更多样化，适合探索性研究和创意测试

#### 最大令牌数（Max Tokens）

- **150-300**：简短答案（选择题、量表评分）
- **300-500**：中等长度（简答题）
- **500-1000**：详细回答（开放式问题、深度访谈）

#### 并行设置

- **小规模**（<10人）：并发数 2-3
- **中等规模**（10-50人）：并发数 5-10
- **大规模**（50+人）：并发数 10-15（注意API速率限制）

---

## 🏗️ 架构设计

详细的架构文档请查看 **[Architecture Guide](./docs/architecture/README.md)**

### 项目结构

```
auto_sim_ai/
├── app.py                      # Streamlit 主应用
├── pages/                      # 多页面应用
│   ├── 1_Setup.py             # 人物管理页面
│   ├── 2_Simulation.py        # 模拟运行页面
│   └── 3_Results.py           # 结果分析页面
├── src/                        # 核心模块
│   ├── llm_client.py          # LLM 客户端（同步/异步）
│   ├── persona.py             # 人物管理
│   ├── simulation.py          # 模拟引擎（单线程/并行）
│   ├── storage.py             # 结果存储
│   ├── cache.py               # 响应缓存
│   ├── checkpoint.py          # 断点管理
│   ├── scoring.py             # 自动评分
│   ├── ab_testing.py          # A/B测试
│   ├── intervention_study.py  # 干预研究（旧版）
│   ├── longitudinal_study.py  # 纵向研究（新版，推荐）
│   ├── persona_generator.py   # 人物生成器
│   ├── survey_templates.py    # 问卷模板库
│   ├── survey_config.py       # 问卷配置
│   ├── tools.py               # 工具注册系统
│   ├── ui_components.py       # UI 组件
│   ├── styles.py              # 设计系统
│   └── validators.py          # 输入验证
├── tests/                      # 测试套件
├── data/                       # 数据目录
│   ├── personas/              # 人物数据
│   ├── results/               # 模拟结果
│   ├── cache/                 # 缓存数据
│   ├── checkpoints/           # 检查点
│   └── survey_configs/        # 问卷配置
├── docs/                       # 文档
├── requirements.txt            # 依赖列表
└── pytest.ini                 # 测试配置
```

### 核心模块说明

#### LLM 客户端 (`llm_client.py`)

支持同步和异步两种模式：

- **LMStudioClient**：同步客户端，适合简单场景
- **AsyncLLMClient**：异步客户端，支持高并发

兼容 OpenAI API 格式，可无缝切换不同提供商。

#### 模拟引擎 (`simulation.py`)

- **SimulationEngine**：基础引擎，顺序执行
- **ParallelSimulationEngine**：并行引擎，支持异步批处理

自动处理错误重试、进度追踪、结果聚合。

#### 缓存系统 (`cache.py`)

基于内容哈希的智能缓存：
- 相同人物 + 相同问题 = 直接返回缓存结果
- 支持缓存导出和导入
- 显著降低 LLM API 调用成本

#### 评分系统 (`scoring.py`)

自动化评分功能：
- 支持多种标准化量表
- 可配置自定义评分规则
- 自动计算总分和子量表分数

---

## 🔬 高级功能

> 💡 **提示**: 详细的API文档和高级功能请查看 [API Guide](./docs/api/README.md)

### 1. A/B 测试

比较不同版本的干预效果：

```python
from src import ABTestManager, Condition

# 定义测试条件
condition_a = Condition(
    name="版本A",
    intervention_text="每天冥想10分钟可以降低压力。",
    questions=["您会尝试这个方法吗？"]
)

condition_b = Condition(
    name="版本B", 
    intervention_text="研究表明，每天冥想10分钟可以降低30%的压力水平。",
    questions=["您会尝试这个方法吗？"]
)

# 运行A/B测试
ab_manager = ABTestManager()
results = ab_manager.run_test([condition_a, condition_b], personas)
```

### 2. 纵向研究（多波次追踪）

使用对话记忆实现真实的纵向追踪：

```python
from src import LongitudinalStudyEngine, WaveConfig, LongitudinalStudyConfig

# 配置研究波次
waves = [
    WaveConfig(
        wave_number=1,
        wave_name="基线",
        questions=["您目前的压力水平如何？(1-10)"],
        days_from_baseline=0
    ),
    WaveConfig(
        wave_number=2,
        wave_name="1个月后",
        questions=["您现在的压力水平如何？(1-10)"],
        days_from_baseline=30,
        intervention_text="每天练习10分钟冥想"
    )
]

# 运行纵向研究
config = LongitudinalStudyConfig(
    study_id="stress_study",
    study_name="压力干预研究",
    waves=waves
)

engine = LongitudinalStudyEngine(llm_client)
results = engine.run_study(personas, config)
```

详细的纵向研究指南请查看 **[Longitudinal Study Guide](./docs/longitudinal/README.md)**

### 3. 批量人物生成

基于真实人口统计分布生成虚拟样本：

```python
from src import PersonaGenerator, DistributionConfig

# 配置分布
config = DistributionConfig(
    age_distribution={
        "18-30": 0.3,
        "31-50": 0.4,
        "51-70": 0.3
    },
    gender_distribution={
        "男": 0.48,
        "女": 0.52
    }
)

# 生成100个人物
generator = PersonaGenerator()
personas = generator.generate_batch(
    count=100,
    distribution_config=config,
    llm_client=client
)
```

### 5. 响应验证

自动检查响应质量和一致性：

```python
from src import ResponseValidator, ConsistencyChecker

validator = ResponseValidator()
checker = ConsistencyChecker()

# 验证响应格式
is_valid = validator.validate_response(response, question_type)

# 检查一致性
metrics = checker.check_consistency(persona_responses)
print(f"一致性得分: {metrics.consistency_score}")
```

---

## 📚 API 文档

### PersonaManager

```python
from src import PersonaManager

manager = PersonaManager()

# 添加人物
manager.add_persona(persona)

# 获取所有人物
personas = manager.get_all_personas()

# 按条件筛选
young_adults = manager.filter_personas(
    age_range=(18, 30),
    gender="女"
)

# 保存/加载
manager.save_to_file("personas.json")
manager.load_from_file("personas.json")
```

### SimulationEngine

```python
from src import SimulationEngine

engine = SimulationEngine(
    llm_client=client,
    cache=cache,
    checkpoint_manager=checkpoint_mgr
)

# 运行调查
result = engine.run_survey(
    personas=personas,
    questions=questions,
    temperature=0.7,
    max_tokens=300
)

# 运行干预
result = engine.run_intervention(
    personas=personas,
    intervention_text="健康干预文本",
    questions=followup_questions
)
```

### ResultsStorage

```python
from src import ResultsStorage

storage = ResultsStorage()

# 保存结果
storage.save_result(simulation_result)

# 加载结果
results = storage.load_all_results()

# 导出为CSV
storage.export_to_csv(result, "output.csv")

# 导出分析脚本
storage.export_analysis_script(result, "analysis.py", language="python")
```

---

## ❓ 常见问题

### Q: 需要多少 LLM API 调用？

A: 调用次数 = 人物数量 × 问题数量。例如：
- 10个人物 × 9个问题 = 90次调用
- 使用缓存可大幅减少重复调用

### Q: 模拟需要多长时间？

A: 取决于：
- **本地模型**：约 5-15 秒/响应
- **在线API**：约 1-3 秒/响应
- **并行执行**：可缩短 50-80% 时间

### Q: 结果的可靠性如何？

A: LLM模拟是探索性研究工具，适合：
- ✅ 快速原型测试
- ✅ 假设生成
- ✅ 问卷预测试
- ❌ **不能**替代真实人类研究

### Q: 如何提高响应质量？

1. 创建详细、真实的人物背景
2. 使用清晰、具体的问题
3. 选择合适的温度参数
4. 使用更强大的模型（如 GPT-4）
5. 启用响应验证和一致性检查

### Q: 成本如何？

- **本地LM Studio**：完全免费（需要GPU）
- **DeepSeek API**：~0.001元/千token，极低成本
- **OpenAI GPT-3.5**：~0.015元/千token
- **OpenAI GPT-4**：~0.3元/千token

### Q: 数据安全吗？

- 本地模式：数据完全不出本地
- API模式：遵循各提供商的隐私政策
- 建议：敏感数据使用本地模式

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 开发设置

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest

# 代码格式化
black src/ tests/
isort src/ tests/

# 类型检查
mypy src/
```

### 报告问题

发现 Bug 或有功能建议？请[创建 Issue](https://github.com/jason-jj-li/auto_sim_ai/issues)。

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 优秀的Python Web框架
- [LM Studio](https://lmstudio.ai/) - 本地LLM运行环境
- [OpenAI](https://openai.com/) - API标准
- [DeepSeek](https://www.deepseek.com/) - 高性价比LLM服务

---

## 📞 联系方式

- **维护者**: Jason Li
- **GitHub**: [@jason-jj-li](https://github.com/jason-jj-li)
- **Email**: [通过GitHub Issues联系]

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给一个星标！**

Made with ❤️ by Jason Li

</div>
