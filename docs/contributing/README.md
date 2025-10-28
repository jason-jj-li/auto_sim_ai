# 贡献指南

感谢你对 LLM Simulation Survey System 的关注！我们欢迎各种形式的贡献。

---

## 📋 目录

- [开发环境设置](#开发环境设置)
- [代码规范](#代码规范)
- [测试](#测试)
- [提交代码](#提交代码)
- [报告问题](#报告问题)
- [功能请求](#功能请求)
- [文档贡献](#文档贡献)

---

## 🛠️ 开发环境设置

### 1. Fork 和克隆仓库

```bash
# Fork 仓库到你的 GitHub 账号
# 然后克隆你的 fork

git clone https://github.com/YOUR_USERNAME/auto_sim_ai.git
cd auto_sim_ai

# 添加上游仓库
git remote add upstream https://github.com/jason-jj-li/auto_sim_ai.git
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 或使用 conda
conda create -n auto_sim python=3.10
conda activate auto_sim
```

### 3. 安装依赖

```bash
# 运行时依赖
pip install -r requirements.txt

# 开发依赖（包含测试、格式化工具等）
pip install -r requirements-dev.txt
```

### 4. 验证安装

```bash
# 运行测试确保环境正确
pytest

# 启动应用
streamlit run app.py
```

---

## 📏 代码规范

### Python 风格指南

我们遵循 PEP 8，但有以下调整：

- **行长度**: 100 字符（而非 79）
- **导入顺序**: 使用 `isort` 自动排序
- **代码格式**: 使用 `black` 自动格式化

### 代码格式化

提交前格式化代码：

```bash
# 使用 black 格式化
black src/ tests/ pages/ app.py

# 使用 isort 排序导入
isort src/ tests/ pages/ app.py

# 或一次性运行两者
black src/ tests/ pages/ app.py && isort src/ tests/ pages/ app.py
```

### 类型提示

**必须**为所有公共函数添加类型提示：

```python
from typing import List, Dict, Optional, Any

def process_personas(
    personas: List[Persona], 
    config: Optional[Dict[str, Any]] = None
) -> SimulationResult:
    """
    处理虚拟人物并返回结果。
    
    Args:
        personas: 虚拟人物列表
        config: 可选的配置字典
        
    Returns:
        模拟结果对象
    """
    pass
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def run_simulation(
    personas: List[Persona],
    questions: List[str],
    temperature: float = 0.7
) -> SimulationResult:
    """
    运行调查模拟。
    
    这个函数会使用 LLM 为每个虚拟人物生成问题的响应。
    
    Args:
        personas: 参与模拟的虚拟人物列表
        questions: 要问的问题列表
        temperature: LLM 温度参数，控制随机性 (0.0-1.0)
        
    Returns:
        包含所有响应的 SimulationResult 对象
        
    Raises:
        ValueError: 如果 personas 或 questions 为空
        ConnectionError: 如果无法连接到 LLM 服务
        
    Example:
        >>> personas = [Persona(...), Persona(...)]
        >>> questions = ["您的年龄是？", "您的职业是？"]
        >>> result = run_simulation(personas, questions)
        >>> print(len(result.responses))
        4
    """
    pass
```

### 命名规范

```python
# 类名：大驼峰
class PersonaManager:
    pass

# 函数和变量：小写下划线
def get_all_personas():
    persona_list = []
    
# 常量：大写下划线
MAX_RETRIES = 3
DEFAULT_TEMPERATURE = 0.7

# 私有成员：单下划线前缀
class MyClass:
    def _internal_method(self):
        pass
```

---

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/test_persona.py

# 运行特定测试
pytest tests/test_persona.py::test_persona_creation

# 显示详细输出
pytest -v

# 显示打印语句
pytest -s

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

### 编写测试

每个新功能都应该有相应的测试：

```python
# tests/test_my_feature.py
import pytest
from src import MyFeature

def test_my_feature_basic():
    """测试基本功能"""
    feature = MyFeature()
    result = feature.process("input")
    assert result == "expected_output"

def test_my_feature_edge_case():
    """测试边缘情况"""
    feature = MyFeature()
    with pytest.raises(ValueError):
        feature.process(None)

@pytest.mark.parametrize("input,expected", [
    ("a", "A"),
    ("b", "B"),
    ("c", "C"),
])
def test_my_feature_multiple_cases(input, expected):
    """参数化测试"""
    feature = MyFeature()
    assert feature.process(input) == expected
```

### 测试分类

使用 markers 标记测试：

```python
import pytest

@pytest.mark.integration
def test_llm_integration():
    """集成测试：需要真实 LLM 连接"""
    pass

@pytest.mark.slow
def test_large_simulation():
    """慢速测试：需要较长时间"""
    pass
```

运行特定类别的测试：

```bash
# 跳过集成测试
pytest -m "not integration"

# 只运行快速测试
pytest -m "not slow"
```

---

## 📝 提交代码

### 分支策略

```bash
# 从 main 创建新分支
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name

# 或修复 bug
git checkout -b fix/bug-description
```

### 提交信息

使用清晰的提交信息：

```bash
# 好的提交信息
git commit -m "feat: 添加 A/B 测试支持"
git commit -m "fix: 修复人物导入时的编码错误"
git commit -m "docs: 更新 API 文档"
git commit -m "test: 添加模拟引擎的单元测试"

# 提交类型
# feat: 新功能
# fix: 修复 bug
# docs: 文档更新
# test: 测试相关
# refactor: 重构代码
# style: 代码格式调整
# perf: 性能优化
# chore: 其他杂项
```

### 提交前检查

```bash
# 1. 运行测试
pytest

# 2. 格式化代码
black src/ tests/ pages/
isort src/ tests/ pages/

# 3. 类型检查（可选）
mypy src/

# 4. 检查代码质量
pylint src/
```

### 创建 Pull Request

1. **推送分支到你的 fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **在 GitHub 上创建 PR**
   - 访问你的 fork
   - 点击 "New Pull Request"
   - 填写 PR 描述

3. **PR 描述模板**
   ```markdown
   ## 变更说明
   简要描述这个 PR 做了什么
   
   ## 变更类型
   - [ ] 新功能
   - [ ] Bug 修复
   - [ ] 文档更新
   - [ ] 代码重构
   - [ ] 性能优化
   
   ## 测试
   - [ ] 添加了新的测试
   - [ ] 所有测试通过
   - [ ] 手动测试通过
   
   ## 相关 Issue
   Closes #123
   ```

4. **响应审查意见**
   - 及时回复审查评论
   - 根据反馈进行修改
   - 推送更新后的代码

---

## 🐛 报告问题

### 检查现有 Issues

在创建新 issue 前，请先搜索是否已有类似问题。

### 创建 Bug Report

使用以下模板：

```markdown
**问题描述**
清晰简洁地描述 bug

**复现步骤**
1. 进入 '...'
2. 点击 '...'
3. 滚动到 '...'
4. 看到错误

**期望行为**
应该发生什么

**实际行为**
实际发生了什么

**截图**
如果适用，添加截图

**环境信息**
- OS: [例如 macOS 13.0]
- Python版本: [例如 3.10.5]
- 应用版本: [例如 1.0.0]
- LLM提供商: [LM Studio / DeepSeek / OpenAI]

**额外信息**
任何其他相关信息
```

---

## 💡 功能请求

### 创建 Feature Request

```markdown
**功能描述**
清晰描述你想要的功能

**动机**
为什么需要这个功能？它解决什么问题？

**建议的解决方案**
你认为如何实现这个功能？

**替代方案**
还考虑过什么其他方法？

**额外信息**
其他相关信息、截图、示例等
```

---

## 📚 文档贡献

### 文档类型

- **README**: 项目概述和快速开始
- **QUICKSTART**: 详细的入门教程
- **API_GUIDE**: API 使用文档
- **代码注释**: 模块、类、函数的文档字符串

### 文档风格

- 使用清晰、简洁的语言
- 提供实际的代码示例
- 包含截图或图表（如适用）
- 保持格式一致

### 更新文档

```bash
# 文档在以下位置
docs/           # 详细文档
README.md       # 主文档
QUICKSTART.md   # 快速开始
CONTRIBUTING.md # 本文件
```

---

## 🎨 UI/UX 贡献

### Streamlit 组件

- 遵循现有的设计系统（参见 `src/styles.py`）
- 保持界面简洁直观
- 添加适当的帮助文本和提示
- 确保响应式设计

### 设计原则

- **简单性**: 减少认知负担
- **一致性**: 使用统一的样式和交互模式
- **反馈**: 提供清晰的操作反馈
- **容错性**: 优雅处理错误

---

## 🔍 代码审查

### 审查重点

- **功能**: 代码是否实现了预期功能？
- **测试**: 是否有足够的测试覆盖？
- **性能**: 是否有明显的性能问题？
- **可读性**: 代码是否易于理解？
- **文档**: 是否有适当的文档？

### 审查礼仪

- 保持友好和建设性
- 解释"为什么"而不只是"做什么"
- 提供具体的改进建议
- 认可好的代码

---

## 📜 许可证

贡献的代码将在 MIT 许可证下发布。

---

## 🙏 致谢

感谢所有贡献者！你们的努力让这个项目变得更好。

---

## 📞 需要帮助？

- 💬 **讨论**: [GitHub Discussions](https://github.com/jason-jj-li/auto_sim_ai/discussions)
- 🐛 **问题**: [GitHub Issues](https://github.com/jason-jj-li/auto_sim_ai/issues)
- 📧 **邮件**: 通过 GitHub 联系维护者

---

**再次感谢你的贡献！** 🎉
