# 高级功能指南

本文档详细介绍了项目中已实现但在主文档中未充分说明的高级功能。

---

## 📑 目录

1. [项目导出与导入](#项目导出与导入)
2. [样式系统与UI定制](#样式系统与ui定制)
3. [响应验证与质量控制](#响应验证与质量控制)
4. [敏感性分析详解](#敏感性分析详解)
5. [人物生成器高级用法](#人物生成器高级用法)
6. [A/B测试进阶](#ab测试进阶)
7. [会话管理与临时人物](#会话管理与临时人物)

---

## 1. 项目导出与导入

### 功能概述

`ProjectManager` 允许您将整个研究项目（包括人物、调查配置、结果）打包为 `.zip` 文件，方便分享、备份和版本控制。

### 核心类

**位置**: `src/project.py`

```python
from src import ProjectManager
```

### 使用示例

#### 1.1 导出项目

```python
from pathlib import Path
from src import ProjectManager

# 初始化项目管理器
project_manager = ProjectManager(
    workspace_dir=".",           # 工作空间根目录
    export_dir="exports"         # 导出目录
)

# 导出完整项目
export_path = project_manager.export_project(
    project_name="health_intervention_study",
    include_personas=True,        # 包含人物数据
    include_survey_configs=True,  # 包含调查配置
    include_results=True,         # 包含结果数据
    description="研究正念冥想对压力的影响"
)

print(f"项目已导出至: {export_path}")
# 输出: 项目已导出至: exports/health_intervention_study_20231028_143022.zip
```

#### 1.2 导入项目

```python
# 导入已导出的项目
import_dir = project_manager.import_project(
    zip_path="exports/health_intervention_study_20231028_143022.zip",
    target_dir="imported_projects/health_study"
)

print(f"项目已导入至: {import_dir}")

# 查看项目元数据
metadata_path = Path(import_dir) / "project_metadata.json"
import json
with open(metadata_path, 'r') as f:
    metadata = json.load(f)

print(f"项目名称: {metadata['project_name']}")
print(f"导出日期: {metadata['export_date']}")
print(f"描述: {metadata['description']}")
```

#### 1.3 选择性导出

```python
# 仅导出人物和配置，不包含结果（用于分享研究设计）
export_path = project_manager.export_project(
    project_name="meditation_study_design",
    include_personas=True,
    include_survey_configs=True,
    include_results=False,  # 不包含结果
    description="冥想干预研究设计模板"
)
```

### 导出包结构

```
project_name_timestamp.zip
├── project_metadata.json    # 项目元数据
├── personas/                # 人物数据
│   ├── persona_001.json
│   ├── persona_002.json
│   └── ...
├── survey_configs/          # 调查配置
│   ├── phq9_config.json
│   └── ...
└── results/                 # 结果数据（可选）
    ├── simulation_001.json
    ├── simulation_001.csv
    └── ...
```

### 使用场景

- ✅ **团队协作**: 分享研究设计给同事
- ✅ **版本控制**: 保存研究的不同版本
- ✅ **备份**: 定期备份重要项目
- ✅ **发布**: 与论文一起发布可重复的研究数据
- ✅ **迁移**: 在不同计算机间转移项目

---

## 2. 样式系统与UI定制

### 功能概述

项目使用统一的设计系统 (`src/styles.py`) 来确保所有 Streamlit 页面的一致性和专业外观。

### 核心模块

**位置**: `src/styles.py`

```python
from src.styles import apply_global_styles, GLOBAL_STYLES
```

### 设计系统变量

```python
# 主色调
--primary: #3b82f6          # 蓝色
--primary-hover: #2563eb    
--primary-light: #eff6ff    

# 语义色彩
--success: #22c55e          # 绿色（成功）
--warning: #f59e0b          # 橙色（警告）
--error: #ef4444            # 红色（错误）
--info: #3b82f6             # 蓝色（信息）

# 灰度色彩
--gray-50 到 --gray-900     # 渐变灰度

# 阴影
--shadow-xs 到 --shadow-xl  # 不同层级阴影

# 圆角
--radius-sm: 4px
--radius-md: 8px
--radius-lg: 12px
```

### 使用示例

#### 2.1 应用全局样式

```python
import streamlit as st
from src.styles import apply_global_styles

st.set_page_config(page_title="My Page", layout="wide")

# 应用全局样式
apply_global_styles()

# 之后的所有组件自动应用统一样式
st.title("标题会使用设计系统样式")
st.button("Primary Button", type="primary")
```

#### 2.2 自定义卡片组件

```python
st.markdown(f"""
<div style="
    background: white;
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    margin-bottom: 1rem;
">
    <h3 style="color: var(--primary); margin-top: 0;">卡片标题</h3>
    <p style="color: var(--gray-700);">卡片内容</p>
</div>
""", unsafe_allow_html=True)
```

#### 2.3 状态指示器

```python
# 成功状态
st.markdown("""
<div style="
    background: var(--success-light);
    color: var(--success);
    padding: 1rem;
    border-radius: var(--radius-md);
    border-left: 4px solid var(--success);
">
    ✅ 操作成功！
</div>
""", unsafe_allow_html=True)

# 警告状态
st.markdown("""
<div style="
    background: var(--warning-light);
    color: var(--warning);
    padding: 1rem;
    border-radius: var(--radius-md);
    border-left: 4px solid var(--warning);
">
    ⚠️ 请注意这个问题
</div>
""", unsafe_allow_html=True)
```

### 可用组件样式

系统已预定义以下组件样式：
- 按钮（主要、次要、禁用）
- 卡片和容器
- 输入框和表单元素
- 表格和数据显示
- 侧边栏和导航
- 状态指示器（成功、警告、错误、信息）
- 加载动画和进度条

### 定制建议

如需定制UI，修改 `src/styles.py` 中的 CSS 变量即可影响整个应用：

```python
# 例如：更改主色调为紫色
:root {
    --primary: #8b5cf6;
    --primary-hover: #7c3aed;
    --primary-light: #f3e8ff;
}
```

---

## 3. 响应验证与质量控制

### 功能概述

`ResponseValidator` 和 `ConsistencyChecker` 提供全面的响应质量验证，确保 LLM 生成的响应符合预期。

### 核心类

**位置**: `src/validation.py`

```python
from src import ResponseValidator, ConsistencyChecker, ConsistencyMetrics
```

### 3.1 响应验证器 (ResponseValidator)

#### 检测无效响应

```python
validator = ResponseValidator()

# 检测单个响应
response = "I don't know"
is_valid = validator.is_valid_response(response)
print(f"响应是否有效: {is_valid}")  # False

# 检测无回答模式
response = "N/A"
is_non_responsive = validator.is_non_responsive(response)
print(f"是否为无回答: {is_non_responsive}")  # True
```

#### 提取数值

```python
# 从文本中提取数值
response = "我的压力水平是 8 分（满分10分）"
value = validator.extract_numeric_value(response)
print(f"提取的数值: {value}")  # 8.0

# 从量表响应中提取
response = "我选择 '非常同意'，这对应分数 5"
value = validator.extract_scale_value(response, scale_type="likert_5")
print(f"量表得分: {value}")  # 5.0
```

#### 验证响应长度

```python
response = "好的"
is_sufficient = validator.is_sufficient_length(
    response, 
    min_length=10,      # 最少10个字符
    min_words=3         # 最少3个词
)
print(f"长度是否充分: {is_sufficient}")  # False
```

#### 检测矛盾响应

```python
response = "我非常同意，但我完全不赞成这个观点"
is_contradictory = validator.has_contradictions(response)
print(f"是否存在矛盾: {is_contradictory}")  # True
```

### 3.2 一致性检查器 (ConsistencyChecker)

#### 检查重复测试的一致性

```python
checker = ConsistencyChecker()

# 同一问题的多次响应
persona_name = "张三"
question = "你的压力水平（1-10）"
responses = ["7", "8", "7", "6", "7"]

metrics = checker.check_consistency(
    persona_name=persona_name,
    question=question,
    responses=responses,
    threshold=0.8  # 一致性阈值
)

print(f"平均值: {metrics.mean_value}")           # 7.0
print(f"标准差: {metrics.std_dev}")               # 0.71
print(f"变异系数: {metrics.coefficient_variation}")  # 0.10
print(f"一致性得分: {metrics.consistency_score}")    # 0.93
print(f"是否一致: {metrics.is_consistent}")          # True
```

#### 批量检查多个人物

```python
# 检查所有人物对某问题的一致性
results = [
    {"persona": "张三", "question": "Q1", "response": "7"},
    {"persona": "张三", "question": "Q1", "response": "8"},
    {"persona": "李四", "question": "Q1", "response": "3"},
    {"persona": "李四", "question": "Q1", "response": "3"},
]

all_metrics = checker.check_multiple_personas(results)

for metrics in all_metrics:
    print(f"{metrics.persona_name} - {metrics.question}: "
          f"一致性得分 {metrics.consistency_score:.2f}")
```

#### 生成一致性报告

```python
# 生成详细报告
report = checker.generate_consistency_report(all_metrics)

print(report['summary'])
# 输出:
# {
#   'total_personas': 2,
#   'total_questions': 1,
#   'overall_consistency': 0.95,
#   'highly_consistent': 2,
#   'inconsistent': 0
# }
```

### 3.3 实战案例：质量控制流程

```python
from src import SimulationEngine, ResponseValidator, ConsistencyChecker

# 1. 运行模拟
engine = SimulationEngine(llm_client=client)
results = engine.run_simulation(personas=personas, questions=questions)

# 2. 验证响应质量
validator = ResponseValidator()
valid_results = []
invalid_count = 0

for result in results:
    response = result['response']
    
    # 检查是否有效
    if validator.is_valid_response(response):
        # 检查是否足够详细
        if validator.is_sufficient_length(response, min_words=5):
            valid_results.append(result)
        else:
            print(f"响应过短: {result['persona_name']} - {response}")
            invalid_count += 1
    else:
        print(f"无效响应: {result['persona_name']} - {response}")
        invalid_count += 1

print(f"有效响应: {len(valid_results)} / {len(results)}")
print(f"无效响应: {invalid_count}")

# 3. 检查一致性（重复测试）
if '第二轮' in results:
    checker = ConsistencyChecker()
    consistency_metrics = checker.check_consistency(
        persona_name="张三",
        question="Q1",
        responses=[r['response'] for r in results if r['persona_name']=='张三']
    )
    
    if not consistency_metrics.is_consistent:
        print(f"警告: {consistency_metrics.persona_name} 的响应不一致!")
```

### 验证最佳实践

1. **预过滤**: 运行小规模测试，调整 prompt 直到无效响应率 < 5%
2. **重试机制**: 对无效响应自动重新生成
3. **阈值调整**: 根据研究需求调整一致性阈值（宽松：0.6，严格：0.9）
4. **日志记录**: 保存所有验证结果用于质量审计

---

## 4. 敏感性分析详解

### 功能概述

`SensitivityAnalyzer` 用于测试模拟结果对参数变化的敏感性，评估发现的稳健性。

### 核心类

**位置**: `src/sensitivity.py`

```python
from src import SensitivityAnalyzer
```

### 4.1 温度参数敏感性

```python
from src import SensitivityAnalyzer, SimulationEngine, LMStudioClient

analyzer = SensitivityAnalyzer()
client = LMStudioClient(base_url="http://localhost:1234/v1")
engine = SimulationEngine(llm_client=client)

# 定义模拟函数
def run_simulation(personas, questions, temperature, **kwargs):
    client.temperature = temperature
    return engine.run_simulation(personas=personas, questions=questions)

# 测试不同温度
temp_results = analyzer.temperature_sensitivity(
    simulation_func=run_simulation,
    personas=personas,
    questions=questions,
    temperature_range=[0.1, 0.3, 0.5, 0.7, 0.9],
)

print(f"温度敏感性: {temp_results['variance']}")
print(f"最稳定温度: {temp_results['most_stable_temp']}")
```

### 4.2 Prompt 措辞敏感性

```python
# 测试不同 prompt 措辞
prompt_variants = [
    "请评估你的压力水平（1-10）",
    "在1到10的范围内，你的压力有多大？",
    "用1-10的数字描述你目前的压力程度",
]

prompt_results = analyzer.prompt_sensitivity(
    simulation_func=run_simulation,
    personas=personas,
    prompt_variants=prompt_variants
)

# 查看不同措辞的响应分布
for i, prompt in enumerate(prompt_variants):
    print(f"Prompt {i+1}: 平均得分 {prompt_results['means'][i]:.2f}")
```

### 4.3 人物样本敏感性

```python
# 测试不同人物子集
subset_results = analyzer.persona_subset_sensitivity(
    simulation_func=run_simulation,
    personas=personas,
    questions=questions,
    subset_sizes=[10, 20, 50, 100],  # 不同样本量
    num_iterations=5  # 每个样本量重复5次
)

print(f"样本稳定性: {subset_results['stability_score']}")
```

### 4.4 自定义参数敏感性

```python
# 测试任意参数
custom_results = analyzer.parameter_sensitivity(
    simulation_func=run_simulation,
    personas=personas,
    questions=questions,
    parameter_name="max_tokens",
    parameter_values=[100, 300, 500, 1000],
)

print(f"Token限制对响应的影响: {custom_results['effect_size']}")
```

### 4.5 综合敏感性报告

```python
# 生成完整敏感性报告
comprehensive_report = analyzer.comprehensive_sensitivity_analysis(
    simulation_func=run_simulation,
    personas=personas,
    questions=questions,
    test_temperature=True,
    test_prompts=True,
    test_subsets=True,
    output_file="sensitivity_report.json"
)

print(f"总体稳健性得分: {comprehensive_report['overall_robustness']:.2f}")
# 0-1 分数，越高表示发现越稳健
```

### 使用场景

- 🔬 **研究验证**: 确保发现不依赖于特定参数选择
- 📊 **报告补充**: 在论文中报告敏感性分析结果
- ⚙️ **参数优化**: 找到最佳温度、token限制等
- 🎯 **置信度评估**: 量化结果的可靠性

---

## 5. 人物生成器高级用法

### 功能概述

`PersonaGenerator` 可以根据统计分布自动生成大量符合人口学特征的虚拟人物。

### 核心类

**位置**: `src/persona_generator.py`

```python
from src import PersonaGenerator, DistributionConfig
```

### 5.1 基于分布生成人物

#### 正态分布

```python
from src import PersonaGenerator, DistributionConfig

generator = PersonaGenerator()

# 定义年龄分布（正态分布）
age_dist = DistributionConfig(
    variable_name="age",
    distribution_type="normal",
    parameters={
        'mean': 35,      # 平均年龄35岁
        'std': 10,       # 标准差10
        'integer': True  # 取整
    }
)

# 生成100个人物
personas = generator.generate_from_distributions(
    distributions=[age_dist],
    n_personas=100
)

# 验证分布
ages = [p.demographics.get('age') for p in personas]
print(f"平均年龄: {sum(ages)/len(ages):.1f}")  # ~35
```

#### 分类分布

```python
# 性别分布（60% 女性，40% 男性）
gender_dist = DistributionConfig(
    variable_name="gender",
    distribution_type="categorical",
    parameters={
        'categories': ['女', '男'],
        'probabilities': [0.6, 0.4]
    }
)

# 职业分布
occupation_dist = DistributionConfig(
    variable_name="occupation",
    distribution_type="categorical",
    parameters={
        'categories': ['教师', '工程师', '医生', '销售', '学生'],
        'probabilities': [0.2, 0.25, 0.15, 0.2, 0.2]
    }
)

# 组合多个分布
personas = generator.generate_from_distributions(
    distributions=[age_dist, gender_dist, occupation_dist],
    n_personas=200
)
```

#### 均匀分布

```python
# 收入均匀分布在50k-150k之间
income_dist = DistributionConfig(
    variable_name="income",
    distribution_type="uniform",
    parameters={
        'low': 50000,
        'high': 150000,
        'integer': True
    }
)
```

### 5.2 复杂人口模拟

```python
# 模拟真实城市人口
city_population = generator.generate_from_distributions(
    distributions=[
        # 年龄：正态分布，均值38，标准差15
        DistributionConfig("age", "normal", 
            {'mean': 38, 'std': 15, 'integer': True}),
        
        # 性别：51% 女性
        DistributionConfig("gender", "categorical",
            {'categories': ['女', '男'], 'probabilities': [0.51, 0.49]}),
        
        # 教育：多类别分布
        DistributionConfig("education", "categorical", {
            'categories': ['高中', '大专', '本科', '研究生'],
            'probabilities': [0.3, 0.25, 0.35, 0.1]
        }),
        
        # 收入：对数正态分布（偏态）
        DistributionConfig("income", "custom", {
            'values': [30000, 50000, 70000, 90000, 120000, 150000, 200000],
        }),
    ],
    n_personas=500
)

print(f"生成了 {len(city_population)} 个城市居民人物")
```

### 5.3 条件生成

```python
# 生成特定条件的人物
def generate_high_stress_workers(n=50):
    """生成高压力职业人群"""
    
    personas = generator.generate_from_distributions(
        distributions=[
            DistributionConfig("age", "normal", 
                {'mean': 32, 'std': 8, 'integer': True}),
            DistributionConfig("occupation", "categorical", {
                'categories': ['医生', '律师', '投资银行家', '创业者'],
                'probabilities': [0.3, 0.3, 0.2, 0.2]
            }),
            DistributionConfig("stress_level", "normal",
                {'mean': 7.5, 'std': 1.0}),  # 高压力
        ],
        n_personas=n
    )
    
    return personas

stressed_workers = generate_high_stress_workers(100)
```

### 5.4 从真实数据匹配分布

```python
import pandas as pd
import numpy as np

# 从真实调查数据提取分布
real_data = pd.read_csv("real_survey_data.csv")

# 拟合年龄分布
age_mean = real_data['age'].mean()
age_std = real_data['age'].std()

# 拟合职业分布
occupation_counts = real_data['occupation'].value_counts(normalize=True)

# 使用提取的分布生成虚拟人物
synthetic_personas = generator.generate_from_distributions(
    distributions=[
        DistributionConfig("age", "normal", 
            {'mean': age_mean, 'std': age_std, 'integer': True}),
        DistributionConfig("occupation", "categorical", {
            'categories': occupation_counts.index.tolist(),
            'probabilities': occupation_counts.values.tolist()
        }),
    ],
    n_personas=len(real_data)  # 生成相同数量
)

print("✅ 已生成与真实数据分布匹配的虚拟人物")
```

### 5.5 分层抽样生成

```python
def generate_stratified_sample():
    """生成分层样本：每个年龄段各50人"""
    
    age_groups = [
        (18, 30, 50),  # 18-30岁，50人
        (31, 45, 50),  # 31-45岁，50人
        (46, 60, 50),  # 46-60岁，50人
        (61, 75, 50),  # 61-75岁，50人
    ]
    
    all_personas = []
    
    for min_age, max_age, n in age_groups:
        personas = generator.generate_from_distributions(
            distributions=[
                DistributionConfig("age", "uniform", {
                    'low': min_age,
                    'high': max_age,
                    'integer': True
                }),
            ],
            n_personas=n
        )
        all_personas.extend(personas)
    
    return all_personas

stratified_sample = generate_stratified_sample()
print(f"分层样本总数: {len(stratified_sample)}")
```

---

## 6. A/B测试进阶

### 功能概述

`ABTestManager` 提供完整的随机分配、效果比较和统计检验功能。

### 核心类

**位置**: `src/ab_testing.py`

```python
from src import ABTestManager, Condition, ABTestConfig
```

### 6.1 基础 A/B 测试

```python
from src import ABTestManager, Condition, Persona

# 定义测试条件
condition_a = Condition(
    condition_id="control",
    condition_name="对照组（无干预）",
    intervention_text="",
    allocation_weight=1.0
)

condition_b = Condition(
    condition_id="treatment",
    condition_name="干预组（正念冥想）",
    intervention_text="每天练习10分钟正念冥想可以帮助减轻压力...",
    allocation_weight=1.0
)

# 创建 AB 测试管理器
ab_manager = ABTestManager(seed=42)  # 设置随机种子以确保可重复

# 分配人物到条件
assignments = ab_manager.assign_personas(
    personas=personas,
    conditions=[condition_a, condition_b]
)

print(f"对照组: {sum(1 for c in assignments.values() if c=='control')}")
print(f"干预组: {sum(1 for c in assignments.values() if c=='treatment')}")
```

### 6.2 多臂测试（A/B/C/D）

```python
# 测试4个不同的干预方案
conditions = [
    Condition("control", "对照组", ""),
    Condition("mindfulness", "正念冥想", "练习正念冥想..."),
    Condition("exercise", "运动", "每天运动30分钟..."),
    Condition("socializing", "社交", "多与朋友聚会..."),
]

# 运行多臂测试
assignments = ab_manager.assign_personas(personas, conditions)

# 按条件分组运行模拟
from src import SimulationEngine

engine = SimulationEngine(llm_client=client)
results_by_condition = {}

for condition in conditions:
    # 获取该条件的人物
    condition_personas = [
        p for p in personas 
        if assignments[p.id] == condition.condition_id
    ]
    
    # 运行模拟（包含干预文本）
    results = engine.run_intervention_simulation(
        personas=condition_personas,
        questions=questions,
        intervention_text=condition.intervention_text
    )
    
    results_by_condition[condition.condition_id] = results

# 比较结果
comparison = ab_manager.compare_conditions(results_by_condition)
print(comparison)
```

### 6.3 分层随机化

```python
# 按性别分层，确保每组性别比例相同
stratified_assignments = ab_manager.assign_personas(
    personas=personas,
    conditions=[condition_a, condition_b],
    stratify_by="gender"  # 按性别分层
)

# 验证分层效果
for condition_id in ["control", "treatment"]:
    condition_personas = [
        p for p in personas 
        if stratified_assignments[p.id] == condition_id
    ]
    females = sum(1 for p in condition_personas if p.demographics['gender']=='女')
    print(f"{condition_id}: 女性比例 {females/len(condition_personas):.2%}")
```

### 6.4 不等分配权重

```python
# 2:1 分配（干预组2份，对照组1份）
condition_a.allocation_weight = 1.0
condition_b.allocation_weight = 2.0

assignments = ab_manager.assign_personas(
    personas=personas,
    conditions=[condition_a, condition_b]
)

# 验证分配比例
control_count = sum(1 for c in assignments.values() if c=='control')
treatment_count = sum(1 for c in assignments.values() if c=='treatment')
print(f"分配比例: {treatment_count}:{control_count} ≈ 2:1")
```

### 6.5 统计检验

```python
# 运行统计检验
from scipy import stats
import pandas as pd

# 假设我们有数值型结果（如压力得分）
df = pd.DataFrame([
    {'persona_id': p.id, 'condition': assignments[p.id], 
     'stress_score': result['score']}
    for p, result in zip(personas, results)
])

# t 检验
control_scores = df[df['condition']=='control']['stress_score']
treatment_scores = df[df['condition']=='treatment']['stress_score']

t_stat, p_value = stats.ttest_ind(control_scores, treatment_scores)

print(f"t统计量: {t_stat:.3f}")
print(f"p值: {p_value:.4f}")
print(f"显著性: {'显著' if p_value < 0.05 else '不显著'}")

# 效应量（Cohen's d）
mean_diff = treatment_scores.mean() - control_scores.mean()
pooled_std = np.sqrt(
    (control_scores.std()**2 + treatment_scores.std()**2) / 2
)
cohens_d = mean_diff / pooled_std
print(f"Cohen's d: {cohens_d:.3f}")
```

### 6.6 完整 A/B 测试工作流

```python
from src import ABTestManager, ABTestConfig, SimulationEngine

# 1. 定义测试配置
config = ABTestConfig(
    test_name="meditation_stress_reduction",
    conditions=[
        Condition("control", "对照组", ""),
        Condition("treatment", "冥想干预", "每天练习10分钟正念冥想...")
    ],
    questions=[
        "你目前的压力水平是多少？（1-10）",
        "你睡眠质量如何？（1-10）"
    ],
    random_assignment=True,
    stratify_by="gender"
)

# 2. 初始化管理器
ab_manager = ABTestManager(seed=42)

# 3. 分配人物
assignments = ab_manager.assign_personas(
    personas=personas,
    conditions=config.conditions,
    stratify_by=config.stratify_by
)

# 4. 运行实验
engine = SimulationEngine(llm_client=client)
results = ab_manager.run_ab_test(
    config=config,
    personas=personas,
    assignments=assignments,
    engine=engine
)

# 5. 分析结果
analysis = ab_manager.analyze_results(results)

print(f"对照组平均压力: {analysis['control']['mean_stress']:.2f}")
print(f"干预组平均压力: {analysis['treatment']['mean_stress']:.2f}")
print(f"差异: {analysis['difference']:.2f}")
print(f"p值: {analysis['p_value']:.4f}")
print(f"效应量: {analysis['effect_size']:.3f}")

# 6. 导出报告
ab_manager.export_report(analysis, "ab_test_report.pdf")
```

---

## 7. 会话管理与临时人物

### 功能概述

系统支持三种人物存储模式，适应不同使用场景。

### 7.1 三种人物类型

```python
# 1. 磁盘人物（永久保存）
from src import PersonaManager

manager = PersonaManager()
persona = Persona(name="张三", age=30, gender="男")
manager.save_persona(persona)  # 保存到 data/personas/

# 2. 会话人物（浏览器会话期间有效）
st.session_state.session_personas.append(persona)
# 关闭浏览器后消失

# 3. 生成人物（临时生成，未保存）
from src import PersonaGenerator
generator = PersonaGenerator()
temp_personas = generator.generate_from_distributions(...)
st.session_state.generated_personas = temp_personas
# 可选择性保存到磁盘
```

### 7.2 批量上传临时人物

在 Setup 页面：

1. 上传 CSV 文件
2. 人物被加载到 `session_personas`
3. 可以在当前会话中使用
4. 可选择保存到磁盘（永久化）

### 7.3 人物生命周期管理

```python
# 获取所有可用人物
def get_all_personas():
    disk_personas = st.session_state.persona_manager.load_all_personas()
    session_personas = st.session_state.get('session_personas', [])
    generated_personas = st.session_state.get('generated_personas', [])
    
    return disk_personas + session_personas + generated_personas

# 清理临时人物
def clear_temporary_personas():
    st.session_state.session_personas = []
    st.session_state.generated_personas = []
    st.success("已清除所有临时人物")

# 永久化临时人物
def save_temporary_personas_to_disk():
    temp_personas = (
        st.session_state.get('session_personas', []) + 
        st.session_state.get('generated_personas', [])
    )
    
    for persona in temp_personas:
        st.session_state.persona_manager.save_persona(persona)
    
    # 清空临时存储
    clear_temporary_personas()
    
    st.success(f"已保存 {len(temp_personas)} 个人物到磁盘")
```

### 7.4 使用场景建议

| 人物类型 | 适用场景 | 优点 | 缺点 |
|---------|---------|------|------|
| **磁盘人物** | 长期项目、重复使用 | 永久保存、可共享 | 占用存储空间 |
| **会话人物** | 快速测试、一次性任务 | 无需清理 | 关闭浏览器后丢失 |
| **生成人物** | 大规模模拟、参数探索 | 快速生成大量样本 | 需手动保存 |

**最佳实践**:
- 开发/测试阶段：使用会话人物或生成人物
- 正式研究：将确定的人物保存到磁盘
- 大规模模拟：生成临时人物，仅保存结果
- 团队协作：使用磁盘人物 + 项目导出功能

---

## 总结

本文档涵盖了以下高级功能：

1. ✅ **项目管理** - 导出/导入完整项目
2. ✅ **样式系统** - 统一的UI设计系统
3. ✅ **质量控制** - 响应验证与一致性检查
4. ✅ **敏感性分析** - 评估结果稳健性
5. ✅ **人物生成** - 基于统计分布的批量生成
6. ✅ **A/B测试** - 完整的随机对照试验流程
7. ✅ **会话管理** - 灵活的人物生命周期管理

这些功能在主文档中提及但缺乏详细示例，本指南提供了完整的使用方法和最佳实践。

---

**相关文档**:
- [README.md](README.md) - 项目概览
- [API_GUIDE.md](API_GUIDE.md) - API参考
- [ARCHITECTURE.md](ARCHITECTURE.md) - 架构设计
- [LONGITUDINAL_GUIDE.md](LONGITUDINAL_GUIDE.md) - 纵向研究指南
