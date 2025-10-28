# API 使用指南

详细的 API 文档和代码示例。

> ⚠️ **注意**: 本文档部分内容可能引用了已移除的高级功能模块（如 `StatisticalAnalyzer`, `ScriptGenerator`, `SensitivityAnalyzer`, `ProjectManager`, `ResponseValidator`, `SimulationEstimator`）。这些功能的代码已从项目中删除，因为它们没有UI支持。本文档将在后续版本中更新。当前版本的系统专注于核心仿真功能和已实现UI的特性。

---

## 📋 目录

- [核心模块](#核心模块)
  - [LLM 客户端](#llm-客户端)
  - [虚拟人物管理](#虚拟人物管理)
  - [模拟引擎](#模拟引擎)
  - [结果存储](#结果存储)
- [高级功能](#高级功能)
  - [A/B 测试](#ab-测试)
  - [~~敏感性分析~~](#敏感性分析) *(已移除)*
  - [纵向研究](#纵向研究)
  - [批量人物生成](#批量人物生成)
- [工具和辅助](#工具和辅助)
- [完整示例](#完整示例)

---

## 核心模块

### LLM 客户端

#### 同步客户端

```python
from src import LMStudioClient

# 初始化本地客户端
client = LMStudioClient(
    base_url="http://127.0.0.1:1234/v1",
    model="local-model"
)

# 或初始化 API 客户端
client = LMStudioClient(
    base_url="https://api.deepseek.com/v1",
    api_key="your-api-key",
    model="deepseek-chat"
)

# 生成响应
response = client.generate(
    prompt="您好，请介绍一下自己",
    temperature=0.7,
    max_tokens=300
)
print(response)

# 测试连接
is_connected = client.test_connection()
print(f"连接状态: {is_connected}")

# 获取可用模型
models = client.list_models()
print(f"可用模型: {models}")
```

#### 异步客户端

```python
import asyncio
from src import AsyncLLMClient

async def main():
    # 初始化异步客户端
    client = AsyncLLMClient(
        base_url="https://api.deepseek.com/v1",
        api_key="your-api-key",
        model="deepseek-chat"
    )
    
    # 单个请求
    response = await client.generate_async(
        prompt="您的年龄是？",
        temperature=0.7
    )
    
    # 批量请求
    prompts = ["问题1", "问题2", "问题3"]
    responses = await client.generate_batch(
        prompts=prompts,
        temperature=0.7,
        max_concurrent=5
    )
    
    for i, response in enumerate(responses):
        print(f"响应 {i+1}: {response}")

asyncio.run(main())
```

---

### 虚拟人物管理

#### Persona 类

```python
from src import Persona

# 创建虚拟人物
persona = Persona(
    name="李明",
    age=32,
    gender="男",
    occupation="软件工程师",
    background="在北京一家互联网公司工作，经常加班...",
    personality_traits=["内向", "完美主义", "责任心强"],
    values=["职业发展", "工作生活平衡"],
    education="本科计算机科学",
    location="北京"
)

# 转换为字典
persona_dict = persona.to_dict()

# 从字典创建
persona_from_dict = Persona.from_dict(persona_dict)

# 生成提示上下文
context = persona.to_prompt_context(use_json_format=True)
```

#### PersonaManager 类

```python
from src import PersonaManager

# 初始化管理器
manager = PersonaManager()

# 添加人物
manager.add_persona(persona)

# 批量添加
personas = [persona1, persona2, persona3]
for p in personas:
    manager.add_persona(p)

# 获取所有人物
all_personas = manager.get_all_personas()
print(f"总共 {len(all_personas)} 个人物")

# 获取单个人物
persona = manager.get_persona("李明")

# 删除人物
manager.remove_persona("李明")

# 按条件筛选
young_adults = manager.filter_personas(
    age_range=(18, 30)
)

engineers = manager.filter_personas(
    occupation="工程师"
)

female_doctors = manager.filter_personas(
    gender="女",
    occupation="医生"
)

# 保存和加载
manager.save_to_file("data/personas/my_personas.json")
manager.load_from_file("data/personas/my_personas.json")

# 导出为 CSV
manager.export_to_csv("data/personas/personas.csv")

# 从 CSV 导入
manager.import_from_csv("data/personas/personas.csv")

# 清空所有人物
manager.clear_all()
```

---

### 模拟引擎

#### 基础引擎（同步）

```python
from src import SimulationEngine, LMStudioClient

# 初始化
client = LMStudioClient(...)
engine = SimulationEngine(llm_client=client)

# 运行调查
questions = [
    "您的年龄是？",
    "您的职业是？",
    "您每周工作多少小时？"
]

result = engine.run_survey(
    personas=personas,
    questions=questions,
    temperature=0.7,
    max_tokens=200
)

# 访问结果
print(f"模拟类型: {result.simulation_type}")
print(f"完成时间: {result.timestamp}")
print(f"响应数量: {len(result.persona_responses)}")

# 遍历响应
for response in result.persona_responses:
    print(f"{response['persona_name']}: {response['response']}")

# 转换为字典
result_dict = result.to_dict()
```

#### 并行引擎（异步）

```python
import asyncio
from src import ParallelSimulationEngine, AsyncLLMClient

async def run_parallel_simulation():
    # 初始化
    client = AsyncLLMClient(...)
    engine = ParallelSimulationEngine(
        llm_client=client,
        max_concurrent=10  # 最大并发数
    )
    
    # 运行调查
    result = await engine.run_survey_async(
        personas=personas,
        questions=questions,
        temperature=0.7,
        max_tokens=200,
        progress_callback=lambda current, total: print(f"进度: {current}/{total}")
    )
    
    return result

# 执行
result = asyncio.run(run_parallel_simulation())
```

#### 干预模拟

```python
# 定义干预文本
intervention = """
研究表明，每天进行10分钟的正念冥想可以：
- 降低30%的压力水平
- 改善睡眠质量
- 提升专注力
"""

# 后续问题
followup_questions = [
    "您会尝试这个方法吗？为什么？",
    "什么因素可能阻止您尝试？",
    "如何调整这个建议能让您更愿意尝试？"
]

# 运行干预模拟
result = engine.run_intervention(
    personas=personas,
    intervention_text=intervention,
    questions=followup_questions,
    temperature=0.7
)
```

#### 使用缓存

```python
from src import ResponseCache, SimulationEngine

# 初始化缓存
cache = ResponseCache(cache_dir="data/cache")

# 创建带缓存的引擎
engine = SimulationEngine(
    llm_client=client,
    cache=cache
)

# 第一次运行（调用 LLM）
result1 = engine.run_survey(personas, questions)

# 第二次运行相同问题（使用缓存，快速返回）
result2 = engine.run_survey(personas, questions)

# 查看缓存统计
stats = cache.get_stats()
print(f"命中率: {stats['hit_rate']:.2%}")
print(f"总请求: {stats['total_requests']}")

# 清空缓存
cache.clear_cache()
```

#### 使用检查点

```python
from src import CheckpointManager, SimulationEngine

# 初始化检查点管理器
checkpoint_mgr = CheckpointManager(checkpoint_dir="data/checkpoints")

# 创建带检查点的引擎
engine = SimulationEngine(
    llm_client=client,
    checkpoint_manager=checkpoint_mgr
)

# 运行大规模模拟（自动保存检查点）
try:
    result = engine.run_survey(
        personas=large_persona_list,  # 100+ 人物
        questions=long_question_list,  # 20+ 问题
        save_checkpoints=True,
        checkpoint_interval=10  # 每10个响应保存一次
    )
except KeyboardInterrupt:
    print("模拟被中断")

# 恢复被中断的模拟
result = engine.resume_from_checkpoint(checkpoint_id="simulation_123")
```

---

### 结果存储

```python
from src import ResultsStorage

# 初始化存储
storage = ResultsStorage(results_dir="data/results")

# 保存结果
storage.save_result(result)

# 加载所有结果
all_results = storage.load_all_results()

# 加载特定结果
result = storage.load_result(result_id="20231028_123456")

# 导出为 CSV
storage.export_to_csv(
    result=result,
    output_path="output.csv",
    include_persona_details=True
)

# 导出为 JSON
storage.export_to_json(
    result=result,
    output_path="output.json",
    pretty=True
)

# 删除结果
storage.delete_result(result_id="20231028_123456")

# 列出所有结果
result_list = storage.list_results()
for r in result_list:
    print(f"{r['id']}: {r['timestamp']} - {r['type']}")
```

---

## 高级功能

### A/B 测试

```python
from src import ABTestManager, Condition, ABTestConfig

# 定义测试条件
condition_a = Condition(
    name="版本A - 简单信息",
    intervention_text="每天冥想10分钟可以降低压力。",
    questions=["您会尝试这个方法吗？", "为什么？"]
)

condition_b = Condition(
    name="版本B - 数据支持",
    intervention_text="研究表明，每天冥想10分钟可以降低30%的压力水平。",
    questions=["您会尝试这个方法吗？", "为什么？"]
)

# 配置测试
config = ABTestConfig(
    name="冥想信息 A/B 测试",
    description="测试不同信息框架的效果",
    randomize_assignment=True,  # 随机分配人物
    balance_demographics=True   # 平衡人口统计特征
)

# 运行测试
manager = ABTestManager(llm_client=client)
results = manager.run_test(
    conditions=[condition_a, condition_b],
    personas=personas,
    config=config
)

# 分析结果
analysis = manager.analyze_results(results)
print(f"版本A接受率: {analysis['condition_a']['acceptance_rate']:.2%}")
print(f"版本B接受率: {analysis['condition_b']['acceptance_rate']:.2%}")
print(f"统计显著性: p = {analysis['p_value']:.4f}")

# 导出报告
manager.export_report(results, "ab_test_report.html")
```

### 敏感性分析

```python
from src import SensitivityAnalyzer

analyzer = SensitivityAnalyzer(llm_client=client)

# 分析温度参数的影响
temp_results = analyzer.analyze_temperature(
    personas=personas,
    questions=questions,
    temperatures=[0.0, 0.3, 0.5, 0.7, 0.9, 1.0]
)

# 分析最大令牌数的影响
token_results = analyzer.analyze_max_tokens(
    personas=personas,
    questions=questions,
    max_tokens_values=[100, 200, 300, 500, 1000]
)

# 分析提示词变化的影响
prompt_variants = [
    "请回答以下问题：{question}",
    "作为 {name}，请回答：{question}",
    "根据你的背景和经历，回答：{question}"
]

prompt_results = analyzer.analyze_prompt_variants(
    personas=personas,
    questions=questions,
    prompt_templates=prompt_variants
)

# 可视化结果
analyzer.plot_sensitivity_results(temp_results, "temperature_sensitivity.png")
```

### 纵向研究

```python
from src import (
    InterventionStudyBuilder,
    InterventionWave,
    InterventionStudyManager
)

# 构建研究设计
study = (InterventionStudyBuilder()
    # 第一波：基线调查
    .add_wave(InterventionWave(
        name="基线",
        survey_config=baseline_survey,
        description="干预前的基线测量"
    ))
    
    # 第二波：干预
    .add_wave(InterventionWave(
        name="干预实施",
        intervention_text="请每天进行10分钟冥想，持续30天",
        description="干预措施介绍"
    ))
    
    # 第三波：1个月后随访
    .add_wave(InterventionWave(
        name="1个月随访",
        survey_config=followup_survey,
        description="干预后1个月的效果评估"
    ))
    
    # 第四波：3个月后随访
    .add_wave(InterventionWave(
        name="3个月随访",
        survey_config=followup_survey,
        description="干预后3个月的效果评估"
    ))
    
    .build()
)

# 运行研究
manager = InterventionStudyManager(
    study=study,
    llm_client=client
)

results = manager.run_study(
    personas=personas,
    save_checkpoints=True
)

# 分析纵向变化
analysis = manager.analyze_longitudinal_changes(results)
print(f"平均改善率: {analysis['mean_improvement']:.2%}")

# 可视化趋势
manager.plot_trends(results, "longitudinal_trends.png")
```

### 批量人物生成

```python
from src import PersonaGenerator, DistributionConfig

# 配置人口统计分布
distribution = DistributionConfig(
    age_distribution={
        "18-30": 0.25,
        "31-50": 0.40,
        "51-70": 0.30,
        "71+": 0.05
    },
    gender_distribution={
        "男": 0.48,
        "女": 0.51,
        "其他": 0.01
    },
    education_distribution={
        "高中": 0.30,
        "本科": 0.50,
        "研究生": 0.20
    },
    occupation_categories=[
        "学生", "教师", "医生", "护士", "工程师",
        "销售", "管理", "服务业", "退休", "其他"
    ]
)

# 初始化生成器
generator = PersonaGenerator(llm_client=client)

# 生成单个人物
persona = generator.generate_persona(
    age_range=(25, 35),
    gender="女",
    occupation="医生"
)

# 批量生成
personas = generator.generate_batch(
    count=100,
    distribution_config=distribution,
    diversity_factor=0.8  # 0-1，越高越多样化
)

# 生成具有特定特征的人物
personas = generator.generate_with_constraints(
    count=50,
    constraints={
        "chronic_condition": True,  # 有慢性疾病
        "income_level": "low",      # 低收入
        "urban": True               # 城市居民
    }
)

# 保存生成的人物
manager = PersonaManager()
for p in personas:
    manager.add_persona(p)
manager.save_to_file("generated_personas.json")
```

---

## 工具和辅助

### 问卷模板

```python
from src import SurveyTemplateLibrary, SurveyTemplate

# 获取模板库
library = SurveyTemplateLibrary()

# 列出所有模板
templates = library.list_templates()
for t in templates:
    print(f"{t['id']}: {t['name']}")

# 获取特定模板
phq9 = library.get_template("phq-9")

# 使用模板
questions = phq9.get_questions()
scoring_rules = phq9.get_scoring_rules()

# 创建自定义模板
custom_template = SurveyTemplate(
    id="my-survey",
    name="我的自定义问卷",
    sections=[
        {
            "name": "基本信息",
            "questions": ["年龄？", "职业？"]
        },
        {
            "name": "健康状况",
            "questions": ["您的整体健康状况如何？"]
        }
    ]
)

# 保存模板
library.add_template(custom_template)
library.save_to_file("data/survey_configs/custom_templates.json")
```

### 自动评分

```python
from src import SurveyScorer

# 初始化评分器
scorer = SurveyScorer()

# 加载评分规则
scorer.load_scoring_rules("phq-9")

# 评分单个响应
response = {
    "question": "过去两周，您有多少天感到心情低落？",
    "answer": "几乎每天"
}
score = scorer.score_response(response)

# 评分整个问卷
responses = [
    {"question": "...", "answer": "..."},
    # ... 更多响应
]
total_score = scorer.score_survey(responses)
print(f"PHQ-9 总分: {total_score}")

# 解释分数
interpretation = scorer.interpret_score(total_score, scale="phq-9")
print(f"解释: {interpretation}")
# 输出: "轻度抑郁" 或 "中度抑郁" 等
```

### 响应验证

```python
from src import ResponseValidator, ConsistencyChecker

# 验证器
validator = ResponseValidator()

# 验证单个响应
is_valid = validator.validate_response(
    response="我今年28岁",
    question_type="numeric",
    expected_range=(0, 120)
)

# 验证响应格式
is_valid_format = validator.validate_format(
    response="A",
    allowed_values=["A", "B", "C", "D"]
)

# 一致性检查
checker = ConsistencyChecker()

# 检查人物的所有响应是否一致
metrics = checker.check_consistency(persona_responses)
print(f"一致性得分: {metrics.consistency_score:.2f}")
print(f"矛盾点数量: {metrics.num_contradictions}")

# 检查逻辑一致性
is_consistent = checker.check_logical_consistency(
    responses={
        "age": "28岁",
        "has_children": "是",
        "num_children": "3个",
        "oldest_child_age": "35岁"  # 矛盾！
    }
)
```

### 统计分析

```python
from src import StatisticalAnalyzer

# 初始化分析器
analyzer = StatisticalAnalyzer()

# 描述统计
desc_stats = analyzer.describe(result)
print(f"响应数量: {desc_stats['count']}")
print(f"平均响应长度: {desc_stats['mean_length']:.1f} 字符")

# 组间比较
comparison = analyzer.compare_groups(
    result,
    group_by="gender",
    metric="score"
)
print(f"男性平均分: {comparison['male']['mean']:.2f}")
print(f"女性平均分: {comparison['female']['mean']:.2f}")
print(f"差异显著性: p = {comparison['p_value']:.4f}")

# 相关分析
correlation = analyzer.correlate(
    result,
    var1="age",
    var2="score"
)
print(f"相关系数: r = {correlation['r']:.3f}")

# 回归分析
regression = analyzer.regression(
    result,
    dependent_var="score",
    independent_vars=["age", "education", "income"]
)
print(f"R²: {regression['r_squared']:.3f}")
```

### 数据导出

```python
from src import ScriptGenerator

# 生成 Python 分析脚本
generator = ScriptGenerator()

python_script = generator.generate_python_script(
    result=result,
    include_visualization=True,
    include_statistics=True
)

# 保存脚本
with open("analyze_results.py", "w") as f:
    f.write(python_script)

# 生成 R 脚本
r_script = generator.generate_r_script(
    result=result,
    include_visualization=True
)

with open("analyze_results.R", "w") as f:
    f.write(r_script)

# 生成 Jupyter Notebook
notebook = generator.generate_notebook(
    result=result,
    format="ipynb"
)

with open("analysis.ipynb", "w") as f:
    f.write(notebook)
```

---

## 完整示例

### 端到端工作流

```python
import asyncio
from src import (
    AsyncLLMClient,
    PersonaManager,
    ParallelSimulationEngine,
    ResultsStorage,
    ResponseCache,
    StatisticalAnalyzer,
    SurveyTemplateLibrary
)

async def complete_workflow():
    # 1. 初始化组件
    client = AsyncLLMClient(
        base_url="https://api.deepseek.com/v1",
        api_key="your-api-key",
        model="deepseek-chat"
    )
    
    cache = ResponseCache()
    storage = ResultsStorage()
    
    engine = ParallelSimulationEngine(
        llm_client=client,
        cache=cache,
        max_concurrent=10
    )
    
    # 2. 创建或加载人物
    persona_manager = PersonaManager()
    persona_manager.load_from_file("data/personas/my_personas.json")
    personas = persona_manager.get_all_personas()
    
    # 3. 选择问卷模板
    library = SurveyTemplateLibrary()
    phq9 = library.get_template("phq-9")
    questions = phq9.get_questions()
    
    # 4. 运行模拟
    print("开始模拟...")
    result = await engine.run_survey_async(
        personas=personas,
        questions=questions,
        temperature=0.7,
        max_tokens=200,
        progress_callback=lambda c, t: print(f"进度: {c}/{t}")
    )
    
    # 5. 保存结果
    storage.save_result(result)
    print(f"结果已保存: {result.timestamp}")
    
    # 6. 分析结果
    analyzer = StatisticalAnalyzer()
    stats = analyzer.describe(result)
    print(f"\n统计摘要:")
    print(f"- 响应数量: {stats['count']}")
    print(f"- 平均长度: {stats['mean_length']:.1f} 字符")
    
    # 7. 导出数据
    storage.export_to_csv(result, "results.csv")
    storage.export_to_json(result, "results.json")
    
    print("\n工作流完成！")
    return result

# 运行
result = asyncio.run(complete_workflow())
```

### 项目管理器示例

```python
from src import ProjectManager

# 创建新项目
project = ProjectManager.create_project(
    name="健康干预研究",
    description="测试冥想干预对压力的影响",
    output_dir="projects/meditation_study"
)

# 配置项目
project.set_llm_config({
    "provider": "deepseek",
    "model": "deepseek-chat",
    "api_key": "your-api-key"
})

# 添加人物
project.add_personas_from_file("personas.json")

# 添加问卷配置
project.add_survey_config("baseline", baseline_questions)
project.add_survey_config("followup", followup_questions)

# 运行模拟
result = project.run_simulation(
    simulation_type="intervention",
    personas="all",
    intervention_text=intervention,
    questions="followup"
)

# 项目会自动保存所有配置、结果和分析

# 导出整个项目
project.export_project("meditation_study.zip")

# 加载已有项目
loaded_project = ProjectManager.load_project("projects/meditation_study")
```

---

## 📌 最佳实践

### 错误处理

```python
from src import SimulationEngine
from openai import APIError, RateLimitError

try:
    result = engine.run_survey(personas, questions)
except RateLimitError:
    print("API 速率限制，请稍后重试")
except APIError as e:
    print(f"API 错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

### 性能优化

```python
# 使用异步引擎处理大规模模拟
engine = ParallelSimulationEngine(
    llm_client=async_client,
    max_concurrent=15,  # 根据 API 限制调整
    retry_on_failure=True,
    max_retries=3
)

# 启用缓存
cache = ResponseCache(cache_dir="data/cache")
engine.set_cache(cache)

# 使用检查点保护长时间运行的任务
checkpoint_mgr = CheckpointManager()
engine.set_checkpoint_manager(checkpoint_mgr)
```

### 日志记录

```python
from src import setup_logging, get_logger

# 配置日志
setup_logging(
    level="INFO",
    log_file="logs/simulation.log",
    console=True
)

# 使用日志
logger = get_logger(__name__)
logger.info("开始模拟")
logger.warning("缓存未命中")
logger.error("API 调用失败")
```

---

## 📞 获取帮助

- 📖 查看 [README.md](README.md) 了解概述
- 🚀 查看 [QUICKSTART.md](QUICKSTART.md) 快速上手
- 🐛 [报告问题](https://github.com/jason-jj-li/auto_sim_ai/issues)

---

**Happy Coding! 🚀**
