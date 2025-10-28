# 项目架构文档

LLM Simulation Survey System 的详细架构设计和技术说明。

---

## 📋 目录

- [系统概览](#系统概览)
- [技术栈](#技术栈)
- [核心架构](#核心架构)
- [模块设计](#模块设计)
- [数据流](#数据流)
- [性能优化](#性能优化)
- [扩展性](#扩展性)

---

## 🏛️ 系统概览

### 设计理念

本系统采用**模块化、可扩展、异步优先**的架构设计，核心目标：

1. **易用性** - Streamlit UI，零配置启动
2. **灵活性** - 支持多种 LLM 提供商，可插拔组件
3. **性能** - 异步并发，智能缓存
4. **可靠性** - 检查点恢复，错误重试
5. **可扩展** - 工具系统，插件架构

### 系统分层

```
┌─────────────────────────────────────┐
│     Presentation Layer (UI)         │  Streamlit Web App
├─────────────────────────────────────┤
│     Application Layer               │  Business Logic
│  - Simulation Engine                │
│  - Analysis & Scoring               │
│  - A/B Testing                      │
├─────────────────────────────────────┤
│     Domain Layer                    │  Core Models
│  - Persona                          │
│  - Survey Config                    │
│  - Results                          │
├─────────────────────────────────────┤
│     Infrastructure Layer            │  External Services
│  - LLM Client                       │
│  - Storage                          │
│  - Cache                            │
└─────────────────────────────────────┘
```

---

## 🔧 技术栈

### 前端

- **Streamlit** 1.32.0 - Web UI 框架
- **Plotly** 5.18.0 - 交互式可视化
- **Matplotlib/Seaborn** - 静态图表

### 后端

- **Python** 3.8+ - 主语言
- **asyncio** - 异步编程
- **aiohttp** - 异步 HTTP 客户端

### 数据处理

- **Pandas** 2.2.0 - 数据分析
- **NumPy** 1.26.4 - 数值计算
- **SciPy** 1.12.0 - 科学计算

### LLM 集成

- **OpenAI SDK** 1.30.0 - API 客户端（兼容多提供商）
- **httpx** 0.25.0 - HTTP 支持

### 存储

- **JSON** - 配置和结果存储
- **CSV** - 数据导出
- **SQLite** - 缓存存储（可选）

### 测试

- **pytest** - 测试框架
- **pytest-asyncio** - 异步测试
- **pytest-cov** - 覆盖率报告

### 代码质量

- **black** - 代码格式化
- **isort** - 导入排序
- **mypy** - 类型检查
- **pylint** - 代码检查

---

## 🏗️ 核心架构

### 目录结构详解

```
auto_sim_ai/
│
├── app.py                          # 主应用入口
│
├── pages/                          # Streamlit 多页面
│   ├── 1_Setup.py                 # 人物管理页面
│   ├── 2_Simulation.py            # 模拟执行页面
│   └── 3_Results.py               # 结果分析页面
│
├── src/                            # 核心源代码
│   │
│   ├── __init__.py                # 模块导出
│   │
│   ├── llm_client.py              # LLM 客户端
│   │   ├── LMStudioClient         # 同步客户端
│   │   └── AsyncLLMClient         # 异步客户端
│   │
│   ├── persona.py                 # 人物模型
│   │   ├── Persona                # 人物数据类
│   │   └── PersonaManager         # 人物管理器
│   │
│   ├── simulation.py              # 模拟引擎
│   │   ├── SimulationResult       # 结果容器
│   │   ├── SimulationEngine       # 同步引擎
│   │   └── ParallelSimulationEngine # 异步并行引擎
│   │
│   ├── storage.py                 # 数据存储
│   │   └── ResultsStorage         # 结果存储管理
│   │
│   ├── cache.py                   # 缓存系统
│   │   └── ResponseCache          # 响应缓存
│   │
│   ├── checkpoint.py              # 检查点
│   │   ├── Checkpoint             # 检查点数据
│   │   └── CheckpointManager      # 检查点管理
│   │
│   ├── survey_config.py           # 问卷配置
│   │   ├── SurveyConfig           # 配置模型
│   │   └── SurveyConfigManager    # 配置管理
│   │
│   ├── survey_templates.py        # 问卷模板
│   │   ├── QuestionMetadata       # 问题元数据
│   │   ├── SurveySection          # 问卷分节
│   │   ├── SurveyTemplate         # 模板类
│   │   └── SurveyTemplateLibrary  # 模板库
│   │
│   ├── scoring.py                 # 自动评分
│   │   └── SurveyScorer           # 评分引擎
│   │
│   ├── validation.py              # 响应验证
│   │   ├── ResponseValidator      # 格式验证
│   │   ├── ConsistencyChecker     # 一致性检查
│   │   └── ConsistencyMetrics     # 一致性指标
│   │
│   ├── analysis.py                # 统计分析
│   │   ├── StatisticalAnalyzer    # 分析器
│   │   └── StatisticalResult      # 分析结果
│   │
│   ├── export.py                  # 数据导出
│   │   └── ScriptGenerator        # 分析脚本生成
│   │
│   ├── ab_testing.py              # A/B 测试
│   │   ├── Condition              # 测试条件
│   │   ├── ABTestConfig           # 测试配置
│   │   └── ABTestManager          # 测试管理器
│   │
│   ├── sensitivity.py             # 敏感性分析
│   │   └── SensitivityAnalyzer    # 分析器
│   │
│   ├── intervention_study.py      # 纵向研究
│   │   ├── InterventionWave       # 研究波次
│   │   ├── InterventionStudyConfig # 研究配置
│   │   ├── InterventionStudyBuilder # 构建器
│   │   └── InterventionStudyManager # 管理器
│   │
│   ├── persona_generator.py       # 人物生成
│   │   ├── DistributionConfig     # 分布配置
│   │   └── PersonaGenerator       # 生成器
│   │
│   ├── estimation.py              # 时间估算
│   │   ├── SimulationEstimate     # 估算结果
│   │   └── SimulationEstimator    # 估算器
│   │
│   ├── project.py                 # 项目管理
│   │   └── ProjectManager         # 项目管理器
│   │
│   ├── tools.py                   # 工具系统
│   │   └── ToolRegistry           # 工具注册
│   │
│   ├── ui_components.py           # UI 组件
│   │   ├── render_navigation      # 导航栏
│   │   ├── render_page_header     # 页面头部
│   │   └── render_system_status   # 系统状态
│   │
│   ├── styles.py                  # 样式系统
│   │   └── apply_global_styles    # 全局样式
│   │
│   ├── validators.py              # 输入验证
│   │   ├── InputValidator         # 验证器
│   │   └── ValidationError        # 验证异常
│   │
│   ├── connection_manager.py      # 连接管理
│   │   └── ConnectionManager      # 连接管理器
│   │
│   └── logging_config.py          # 日志配置
│       ├── setup_logging          # 日志设置
│       └── get_logger             # 获取日志器
│
├── tests/                          # 测试套件
│   ├── conftest.py                # pytest 配置
│   ├── test_llm_client.py         # LLM 客户端测试
│   ├── test_persona.py            # 人物测试
│   ├── test_storage.py            # 存储测试
│   └── test_validators.py         # 验证器测试
│
├── data/                           # 数据目录
│   ├── personas/                  # 人物数据
│   ├── results/                   # 模拟结果
│   ├── cache/                     # 缓存数据
│   ├── checkpoints/               # 检查点
│   ├── survey_configs/            # 问卷配置
│   ├── calibration_targets/       # 校准目标（预留）
│   └── samples/                   # 示例数据
│
├── docs/                           # 文档
│
├── requirements.txt                # 运行时依赖
├── requirements-dev.txt            # 开发依赖
├── pyproject.toml                 # 项目配置
├── pytest.ini                     # pytest 配置
└── setup.sh                       # 安装脚本
```

---

## 🎯 模块设计

### LLM 客户端 (`llm_client.py`)

#### 设计模式

- **适配器模式** - 统一不同 LLM 提供商的接口
- **单例模式** - 复用连接池

#### 核心功能

```python
class LMStudioClient:
    """同步 LLM 客户端"""
    
    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成响应"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content

class AsyncLLMClient:
    """异步 LLM 客户端"""
    
    async def generate_async(self, prompt: str, **kwargs) -> str:
        """异步生成单个响应"""
        
    async def generate_batch(self, prompts: List[str], **kwargs) -> List[str]:
        """批量异步生成"""
        tasks = [self.generate_async(p, **kwargs) for p in prompts]
        return await asyncio.gather(*tasks)
```

#### 错误处理

- **自动重试** - 网络错误、超时
- **速率限制** - 遵守 API 限制
- **降级策略** - 失败时降低并发数

---

### 模拟引擎 (`simulation.py`)

#### 架构

```
SimulationEngine (基础)
    ├── run_survey()        # 运行调查
    ├── run_intervention()  # 运行干预
    └── _generate_response() # 生成单个响应

ParallelSimulationEngine (高级)
    ├── run_survey_async()       # 异步调查
    ├── run_intervention_async() # 异步干预
    └── _batch_generate()        # 批量生成
```

#### 执行流程

```
1. 准备阶段
   ├── 验证输入
   ├── 加载缓存
   └── 初始化检查点

2. 执行阶段
   ├── 遍历人物
   │   ├── 构建提示词
   │   ├── 检查缓存
   │   ├── 调用 LLM (如需要)
   │   └── 保存响应
   └── 更新进度

3. 完成阶段
   ├── 聚合结果
   ├── 保存检查点
   └── 返回 SimulationResult
```

#### 并行策略

```python
async def run_survey_async(self, personas, questions, max_concurrent=10):
    """并行执行模拟"""
    
    # 创建任务队列
    tasks = []
    for persona in personas:
        for question in questions:
            task = self._generate_response_async(persona, question)
            tasks.append(task)
    
    # 使用 Semaphore 控制并发
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def bounded_task(task):
        async with semaphore:
            return await task
    
    # 执行所有任务
    results = await asyncio.gather(*[bounded_task(t) for t in tasks])
    
    return results
```

---

### 缓存系统 (`cache.py`)

#### 缓存键生成

```python
def _generate_cache_key(self, persona: Persona, question: str) -> str:
    """基于内容的哈希键"""
    content = {
        "persona": persona.to_dict(),
        "question": question,
        "model": self.model_name,
        "temperature": self.temperature
    }
    content_str = json.dumps(content, sort_keys=True)
    return hashlib.sha256(content_str.encode()).hexdigest()
```

#### 存储结构

```
data/cache/
├── 00/
│   ├── 00a1b2c3...json  # 缓存条目
│   └── 00d4e5f6...json
├── 01/
├── 02/
...
└── ff/
```

#### 缓存策略

- **LRU** - 最近最少使用淘汰
- **TTL** - 可配置过期时间
- **大小限制** - 自动清理旧缓存

---

### 检查点系统 (`checkpoint.py`)

#### 检查点数据

```python
@dataclass
class Checkpoint:
    simulation_id: str
    timestamp: str
    completed_count: int
    total_count: int
    partial_result: SimulationResult
    state: Dict[str, Any]
```

#### 恢复机制

```python
def resume_from_checkpoint(self, checkpoint_id: str) -> SimulationResult:
    """从检查点恢复"""
    checkpoint = self.checkpoint_mgr.load(checkpoint_id)
    
    # 恢复状态
    remaining_tasks = checkpoint.state['remaining_tasks']
    partial_result = checkpoint.partial_result
    
    # 继续执行
    for task in remaining_tasks:
        response = self._execute_task(task)
        partial_result.add_response(response)
        
    return partial_result
```

---

### 问卷模板系统 (`survey_templates.py`)

#### 模板结构

```python
class SurveyTemplate:
    id: str
    name: str
    description: str
    sections: List[SurveySection]
    scoring_rules: Optional[Dict]
    metadata: Dict

class SurveySection:
    name: str
    questions: List[QuestionMetadata]

class QuestionMetadata:
    text: str
    type: str  # "multiple_choice", "scale", "open_ended"
    options: Optional[List[str]]
    required: bool
```

#### 模板示例

```json
{
    "id": "phq-9",
    "name": "PHQ-9 Depression Screening",
    "sections": [
        {
            "name": "症状评估",
            "questions": [
                {
                    "text": "过去两周，您有多少天感到心情低落？",
                    "type": "scale",
                    "options": ["从不", "几天", "一半以上", "几乎每天"],
                    "score_map": [0, 1, 2, 3]
                }
            ]
        }
    ],
    "scoring_rules": {
        "total": "sum",
        "interpretation": {
            "0-4": "无抑郁",
            "5-9": "轻度",
            "10-14": "中度",
            "15-27": "重度"
        }
    }
}
```

---

## 🔄 数据流

### 调查模拟流程

```
用户输入
  ↓
UI 验证 (validators.py)
  ↓
模拟配置 (survey_config.py)
  ↓
模拟引擎 (simulation.py)
  ├→ 人物管理器 (persona.py)
  ├→ 缓存系统 (cache.py)
  ├→ LLM 客户端 (llm_client.py)
  │   ↓
  │   外部 LLM API
  │   ↓
  ├← 响应数据
  ├→ 验证器 (validation.py)
  └→ 评分器 (scoring.py)
  ↓
结果对象 (SimulationResult)
  ↓
存储系统 (storage.py)
  ├→ JSON 文件
  └→ CSV 导出
  ↓
分析模块 (analysis.py)
  ↓
UI 展示
```

### 数据格式

#### 人物 JSON

```json
{
    "name": "李明",
    "age": 32,
    "gender": "男",
    "occupation": "软件工程师",
    "background": "...",
    "personality_traits": ["内向", "完美主义"],
    "values": ["职业发展", "健康"],
    "education": "本科",
    "location": "北京"
}
```

#### 结果 JSON

```json
{
    "simulation_type": "survey",
    "timestamp": "2023-10-28T10:30:00",
    "persona_responses": [
        {
            "persona_name": "李明",
            "persona_age": 32,
            "question": "您的年龄是？",
            "response": "我今年32岁",
            "conversation_history": [...]
        }
    ],
    "metadata": {
        "model": "deepseek-chat",
        "temperature": 0.7,
        "total_tokens": 1500
    }
}
```

---

## ⚡ 性能优化

### 1. 异步并发

```python
# 同步：顺序执行
for persona in personas:
    for question in questions:
        response = llm.generate(...)  # 等待
# 时间：N × M × T

# 异步：并发执行
tasks = [llm.generate_async(...) for p in personas for q in questions]
responses = await asyncio.gather(*tasks, return_exceptions=True)
# 时间：≈ T (如果并发数足够)
```

### 2. 智能缓存

```python
# 第一次运行
result1 = engine.run_survey(personas, questions)
# API 调用：100 次
# 时间：5 分钟

# 第二次运行相同内容
result2 = engine.run_survey(personas, questions)
# API 调用：0 次（全部命中缓存）
# 时间：2 秒
```

### 3. 批处理

```python
# 分批处理，避免内存溢出
batch_size = 50
for i in range(0, len(tasks), batch_size):
    batch = tasks[i:i+batch_size]
    results = await process_batch(batch)
    save_checkpoint(results)
```

### 4. 连接池

```python
# 复用 HTTP 连接
client = AsyncLLMClient(
    connection_pool_size=20,
    keep_alive=True
)
```

---

## 🔌 扩展性

### 插件架构

#### 工具注册系统

```python
from src import ToolRegistry

registry = ToolRegistry()

# 注册自定义工具
@registry.register_tool("my_analyzer")
class MyAnalyzer:
    def analyze(self, data):
        return custom_analysis(data)

# 使用工具
tool = registry.get_tool("my_analyzer")
result = tool.analyze(data)
```

#### 自定义 LLM 提供商

```python
from src.llm_client import BaseLLMClient

class MyLLMProvider(BaseLLMClient):
    def generate(self, prompt: str, **kwargs) -> str:
        # 实现自定义逻辑
        return my_api_call(prompt, **kwargs)

# 使用自定义提供商
client = MyLLMProvider(...)
engine = SimulationEngine(llm_client=client)
```

#### 自定义评分规则

```python
from src import SurveyScorer

scorer = SurveyScorer()

# 添加自定义规则
scorer.add_scoring_rule(
    scale_id="my-scale",
    rules={
        "questions": [...],
        "scoring": lambda responses: custom_score(responses)
    }
)
```

### 多语言支持

```python
# 配置语言
config = {
    "language": "zh-CN",  # 或 "en-US", "es-ES"
    "translations": load_translations("zh-CN")
}

# 使用翻译
ui_text = config["translations"]["welcome_message"]
```

---

## 🔐 安全性

### API 密钥管理

```python
# 环境变量（推荐）
import os
api_key = os.getenv("DEEPSEEK_API_KEY")

# .env 文件
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# 不要硬编码！
# api_key = "sk-xxx"  # ❌ 永远不要这样做
```

### 数据隐私

- 本地模式：数据完全不离开本地
- API 模式：遵循提供商隐私政策
- 敏感数据：使用本地 LM Studio

### 输入验证

```python
from src import InputValidator, ValidationError

validator = InputValidator()

try:
    validated_age = validator.validate_age(user_input)
except ValidationError as e:
    st.error(f"无效输入: {e}")
```

---

## 📊 监控和日志

### 日志系统

```python
from src import setup_logging, get_logger

# 配置日志
setup_logging(
    level="INFO",
    log_file="logs/app.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 使用日志
logger = get_logger(__name__)
logger.info("模拟开始")
logger.warning("缓存未命中")
logger.error("API 调用失败", exc_info=True)
```

### 性能监控

```python
import time

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def track(self, operation_name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start
                
                self.metrics[operation_name] = {
                    "duration": duration,
                    "timestamp": time.time()
                }
                return result
            return wrapper
        return decorator

monitor = PerformanceMonitor()

@monitor.track("run_simulation")
def run_simulation(...):
    ...
```

---

## 🧪 测试策略

### 测试金字塔

```
      /\
     /  \    E2E Tests (少量)
    /────\
   /      \  Integration Tests (中等)
  /────────\
 /          \ Unit Tests (大量)
/────────────\
```

### 测试类型

#### 单元测试

```python
# tests/test_persona.py
def test_persona_creation():
    persona = Persona(name="Test", age=25, ...)
    assert persona.name == "Test"
    assert persona.age == 25

def test_persona_to_dict():
    persona = Persona(...)
    data = persona.to_dict()
    assert isinstance(data, dict)
    assert "name" in data
```

#### 集成测试

```python
# tests/test_simulation.py
@pytest.mark.integration
async def test_full_simulation(mock_llm_client):
    engine = SimulationEngine(llm_client=mock_llm_client)
    result = await engine.run_survey_async(personas, questions)
    assert len(result.persona_responses) == len(personas) * len(questions)
```

#### Mock 策略

```python
# tests/conftest.py
@pytest.fixture
def mock_llm_client():
    client = Mock(spec=LMStudioClient)
    client.generate.return_value = "Mock response"
    return client
```

---

## 🚀 部署

### 本地部署

```bash
streamlit run app.py
```

### Docker 部署（规划中）

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### 云部署

- **Streamlit Cloud** - 一键部署
- **AWS/Azure** - 容器部署
- **Heroku** - PaaS 部署

---

## 📈 未来路线图

### 短期（1-3个月）

- [ ] 增强数据可视化
- [ ] 支持更多问卷模板
- [ ] 改进错误处理
- [ ] 性能优化

### 中期（3-6个月）

- [ ] 数据库后端支持
- [ ] 多用户系统
- [ ] API 服务化
- [ ] 更多 LLM 提供商

### 长期（6-12个月）

- [ ] 机器学习模型集成
- [ ] 实时协作功能
- [ ] 移动端支持
- [ ] 企业版功能

---

## 📚 参考资源

- [Streamlit 文档](https://docs.streamlit.io)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Python asyncio 文档](https://docs.python.org/3/library/asyncio.html)
- [pytest 文档](https://docs.pytest.org)

---

**文档版本**: 1.0.0  
**最后更新**: 2025-10-28  
**维护者**: Jason Li
