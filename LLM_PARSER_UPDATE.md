# LLM Universal Parser Update

## 概述 (Overview)

本次更新添加了**LLM 通用解析器**功能，使系统能够自动解析提示词中的任意新变量，无需为每个新字段预先编写正则表达式解析器。

This update adds an **LLM Universal Parser** feature that enables the system to automatically parse any new variables in prompts without requiring pre-written regex parsers for each new field.

## 主要变更 (Main Changes)

### 1. 新增通用解析函数 (New Universal Parser Function)

**文件**: `src/persona_generator.py`

添加了 `parse_field_to_distribution()` 静态方法：

```python
@staticmethod
def parse_field_to_distribution(
    field_name: str,
    field_value: Any,
    llm_client: Optional[Any] = None,
    model: str = "gpt-4o-mini"
) -> Optional[Dict[str, Any]]:
```

**功能**:
- 使用 LLM 判断字段是否包含可提取的分类信息和百分比
- 如果可以，返回标准化的分布配置 `{variable_name, categories, probabilities}`
- 如果不可以（纯描述性文本），返回 `None`

**示例输入**:
```python
field_name = "exercise_habit"
field_value = "经常运动35%, 偶尔运动45%, 从不运动20%"
```

**示例输出**:
```python
{
    "variable_name": "exercise_habit",
    "categories": ["经常运动", "偶尔运动", "从不运动"],
    "probabilities": [0.35, 0.45, 0.20]
}
```

### 2. 更新 generate_personas_from_ai_extraction()

**新增参数**:
- `use_llm_parser: bool = False` - 是否启用 LLM 通用解析器
- `llm_client: Optional[Any] = None` - LLM 客户端
- `model: str = "gpt-4o-mini"` - 使用的模型

**工作流程**:
1. 先使用内置解析器处理已知字段（age, gender, education, occupation 等）
2. 对于未知字段：
   - 如果 `use_llm_parser=True`，调用 `parse_field_to_distribution()` 尝试解析
   - 如果解析成功，创建分类变量分布
   - 如果解析失败或 `use_llm_parser=False`，保持原有行为（添加到背景文本）

### 3. UI 集成 (UI Integration)

**文件**: `pages/1_Setup.py`

#### 3.1 高级选项 (Advanced Options)

添加了复选框控制 LLM 解析器：

```python
use_llm_parser = st.checkbox(
    "Enable LLM Universal Parser",
    value=True,
    help="..."
)
```

#### 3.2 调用更新

```python
persona_dicts = PersonaGenerator.generate_personas_from_ai_extraction(
    extracted_data=extracted_data,
    n=ai_n_personas,
    seed=ai_seed,
    use_llm_parser=use_llm_parser,  # 新增
    llm_client=st.session_state.llm_client if use_llm_parser else None,  # 新增
    model=st.session_state.selected_model if use_llm_parser else "gpt-4o-mini"  # 新增
)
```

#### 3.3 统计展示简化 (Simplified Statistics Display)

**删除**:
- 复杂的多列展示（Age Statistics, Gender Distribution, Education Levels 等）
- 分散的 Additional Demographics 展示
- Dynamic Variables 单独展示

**替换为**:
- 单一表格展示所有变量统计
- 三列格式：Variable Name, Type, Distribution
- 自动包含所有动态生成的变量

**表格示例**:
```
Variable Name           Type         Distribution
Age                     Continuous   Mean=40.6, Range=[18, 84]
Gender                  Categorical  Male (51.0%), Female (49.0%)
Education               Categorical  初中 (38.8%), 小学 (24.4%), ...
Health Status           Categorical  比较好 (42.0%), 一般 (31.0%), ...
Exercise Habit          Categorical  经常运动 (35%), 偶尔运动 (45%), ...
```

### 4. 内置解析器保留 (Built-in Parsers Retained)

以下字段的专用解析器仍然保留（性能更好，无需额外 LLM 调用）：

- age / age_range
- gender
- education
- occupation
- location
- marital_status
- ethnicity
- political_affiliation
- religion
- health_status
- income_range
- children
- social_insurance
- family_structure
- tech_usage

## 使用场景 (Use Cases)

### 场景 1: 使用内置解析器（默认）

```python
extracted_data = {
    "education": "文盲2.67%, 小学25%, 初中35%",
    "health_status": "非常好25.8%, 比较好37.5%"
}

personas = PersonaGenerator.generate_personas_from_ai_extraction(
    extracted_data=extracted_data,
    n=500,
    use_llm_parser=False  # 使用内置解析器
)
# ✅ 快速，无额外 LLM 调用
```

### 场景 2: 添加新变量（启用 LLM 解析器）

```python
extracted_data = {
    "education": "文盲2.67%, 小学25%, 初中35%",
    "exercise_habit": "经常运动35%, 偶尔运动45%, 从不运动20%",  # 新变量
    "diet_preference": "荤素均衡60%, 偏素食25%, 偏肉食15%",    # 新变量
    "lifestyle": "生活节奏较快，注重工作与生活平衡"            # 纯描述
}

personas = PersonaGenerator.generate_personas_from_ai_extraction(
    extracted_data=extracted_data,
    n=500,
    use_llm_parser=True,  # 启用 LLM 解析器
    llm_client=llm_client,
    model="gpt-4o-mini"
)
# ✅ education: 使用内置解析器
# ✅ exercise_habit: LLM 解析为分类变量
# ✅ diet_preference: LLM 解析为分类变量
# ✅ lifestyle: LLM 识别为纯描述，添加到背景
```

## 优势 (Benefits)

1. **灵活性** - 无需预先编写解析器，支持任意新变量
2. **智能识别** - LLM 可以理解各种表达方式和格式
3. **向后兼容** - 现有代码无需修改（`use_llm_parser` 默认为 False）
4. **性能优化** - 常用字段仍使用快速的内置解析器
5. **用户友好** - UI 中一键开关，无需代码修改

## 性能考虑 (Performance Considerations)

### LLM 调用次数

- **不启用**: 1 次 LLM 调用（仅用于初始人口描述提取）
- **启用**: 1 + N 次调用（N = 未知字段数量）

### 建议

- **小规模实验/快速原型**: 启用 LLM 解析器，快速测试新变量
- **大规模生产/已知变量**: 关闭 LLM 解析器，使用内置解析器
- **混合使用**: 
  - 先用 LLM 解析器测试新变量
  - 确认变量格式后，添加到内置解析器
  - 生产环境关闭 LLM 解析器

## 测试 (Testing)

### 测试脚本

- `test_all_parsers.py` - 测试所有内置解析器
- `test_llm_parser.py` - 测试 LLM 通用解析器
- `test_ui_summary.py` - 测试 UI 统计展示

### 运行测试

```bash
# 测试内置解析器（无需 LLM）
python3 test_all_parsers.py

# 测试 LLM 解析器（需要 LLM 连接）
python3 test_llm_parser.py

# 测试 UI 统计展示
python3 test_ui_summary.py
```

## 未来改进 (Future Improvements)

1. **缓存解析结果** - 避免重复解析相同字段
2. **批量解析** - 一次 LLM 调用处理多个字段
3. **解析器学习** - 自动将成功的 LLM 解析转换为内置解析器
4. **解析质量评估** - 验证 LLM 解析结果的准确性

## 文件变更列表 (Changed Files)

- ✅ `src/persona_generator.py` - 添加通用解析器
- ✅ `pages/1_Setup.py` - UI 集成和展示简化
- ✅ `test_llm_parser.py` - 新增测试脚本
- ✅ `test_ui_summary.py` - 新增测试脚本
- ✅ `LLM_PARSER_UPDATE.md` - 本文档
