# 纵向研究功能更新说明

## 🎉 新功能：基于多轮对话的纵向研究

我们实现了一个全新的纵向研究模块，采用 DeepSeek 的多轮对话机制，让虚拟人物在不同波次之间保持完整的"记忆"和连贯性。

---

## 📦 包含的模块

### 1. **旧版** - `src/intervention_study.py`
- 基础的纵向研究实现
- 每个波次独立调用LLM
- 适合简单的前后测设计
- **状态**: 保留用于向后兼容

### 2. **新版** - `src/longitudinal_study.py` ⭐ **推荐**
- 使用多轮对话保持上下文
- 虚拟人物记住所有历史对话
- 更真实、更连贯的响应
- **状态**: 推荐用于所有新项目

---

## 🆚 核心区别

### 对话方式对比

#### 旧版（独立调用）

```python
# 波次1
messages = [
    {"role": "system", "content": "你是李明..."},
    {"role": "user", "content": "你的压力水平如何？"}
]
response1 = llm.generate(messages)

# 波次2（重新开始，没有记忆）
messages = [
    {"role": "system", "content": "你是李明..."},
    {"role": "user", "content": "7天后，你的压力水平如何？"}
]
response2 = llm.generate(messages)  # 不知道波次1说了什么
```

#### 新版（持续对话）

```python
# 波次1
messages = [
    {"role": "system", "content": "你是李明..."},
    {"role": "user", "content": "你的压力水平如何？"},
    {"role": "assistant", "content": "我会说是7分..."}  # 记住
]

# 波次2（继续对话）
messages.append({"role": "user", "content": "7天后，你的压力水平如何？"})
response2 = llm.generate(messages)  # 知道上次说了7分，会保持连贯
```

### 技术实现对比

| 特性 | 旧版 | 新版 |
|------|------|------|
| **对话历史** | ❌ 每次独立 | ✅ 完整保存 |
| **上下文连贯性** | ⭐⭐ 低 | ⭐⭐⭐⭐⭐ 高 |
| **干预记忆** | ❌ 容易忘记 | ✅ 持续记住 |
| **时间感知** | ⚠️ 有限 | ✅ 强 |
| **API调用次数** | 少（每次独立） | 多（累积上下文） |
| **响应一致性** | ⚠️ 可能矛盾 | ✅ 高度一致 |
| **真实感** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **实现复杂度** | 简单 | 中等 |
| **成本** | 低 | 中（上下文累积） |

---

## 💡 使用建议

### 什么时候用旧版？
- ✅ 快速原型和概念验证
- ✅ 波次间联系不重要的研究
- ✅ 成本敏感的场景
- ✅ 简单的前后测（2-3个波次）

### 什么时候用新版？
- ✅ **正式研究项目**（推荐）
- ✅ 需要高度真实感
- ✅ 多波次长期追踪（5+波次）
- ✅ 干预效果需要持续记忆
- ✅ 需要分析对话演变

---

## 🚀 快速开始

### 旧版示例

```python
from src import InterventionStudyBuilder, InterventionStudyManager

# 简单的前后测
study = InterventionStudyBuilder.create_pre_post_intervention_study(
    study_name="简单干预",
    baseline_questions=["你的压力如何？"],
    intervention_text="请每天冥想10分钟",
    total_waves=5
)

manager = InterventionStudyManager()
manager.save_config(study)
```

### 新版示例

```python
from src import (
    LongitudinalStudyEngine,
    LongitudinalStudyBuilder,
    LMStudioClient
)

# 创建研究
study = LongitudinalStudyBuilder.create_pre_post_study(
    study_name="冥想干预研究",
    baseline_questions=["请用1-10分评价你的压力水平"],
    intervention_text="每天冥想10分钟可以降低压力...",
    num_pre_waves=2,
    num_post_waves=4
)

# 运行研究
client = LMStudioClient(
    base_url="https://api.deepseek.com/v1",
    api_key="your-key"
)

engine = LongitudinalStudyEngine(llm_client=client)

result = engine.run_study(
    config=study,
    personas=personas,
    temperature=0.7
)

# 查看完整对话历史
engine.save_conversation_histories(study.study_id)
```

---

## 📚 文档资源

| 文档 | 用途 |
|------|------|
| `LONGITUDINAL_GUIDE.md` | 完整的使用指南和最佳实践 |
| `examples/longitudinal_study_demo.py` | 可运行的完整示例 |
| `API_GUIDE.md` | API参考文档 |
| `README.md` | 项目概览 |

---

## 🔄 迁移指南

如果你正在使用旧版，可以这样迁移到新版：

### 1. 导入更新

```python
# 旧版
from src import (
    InterventionStudyBuilder,
    InterventionStudyManager
)

# 新版
from src import (
    LongitudinalStudyEngine,      # 新
    LongitudinalStudyBuilder,      # 新
    LMStudioClient
)
```

### 2. 配置更新

```python
# 旧版
study = InterventionStudyBuilder.create_pre_post_intervention_study(
    study_name="研究名称",
    baseline_questions=[...],
    intervention_text="...",
    total_waves=10,
    intervention_wave_number=5
)

# 新版
study = LongitudinalStudyBuilder.create_pre_post_study(
    study_name="研究名称",
    baseline_questions=[...],
    intervention_text="...",
    num_pre_waves=4,        # 替代 intervention_wave_number
    num_post_waves=5,       # total - pre - 1
    days_between_waves=7
)
```

### 3. 运行更新

```python
# 旧版（没有专门的引擎，使用通用的SimulationEngine）
from src import SimulationEngine
engine = SimulationEngine(llm_client=client)
# 手动实现波次循环...

# 新版（专用引擎）
engine = LongitudinalStudyEngine(llm_client=client)
result = engine.run_study(
    config=study,
    personas=personas,
    progress_callback=lambda msg: print(msg)
)
```

### 4. 结果处理更新

```python
# 旧版
# 结果是多个SimulationResult对象

# 新版
# 结果是一个LongitudinalStudyResult对象
for persona_name, wave_results in result.persona_results.items():
    for wave_result in wave_results:
        print(f"波次 {wave_result.wave_number}")
        for response in wave_result.responses:
            print(f"Q: {response['question']}")
            print(f"A: {response['response']}")
```

---

## 💰 成本考虑

### DeepSeek API 成本估算

#### 旧版成本
```
人物数 × 波次数 × 问题数 × 平均响应tokens
= 5 × 9 × 3 × 200
= 27,000 tokens
≈ ¥0.027
```

#### 新版成本（含对话历史）
```
第1波: 5人 × 3问题 × 200 tokens = 3,000
第2波: 5人 × 3问题 × 300 tokens = 4,500 (含历史)
第3波: 5人 × 3问题 × 400 tokens = 6,000
...
总计约: 40,000-50,000 tokens
≈ ¥0.04-0.05
```

**结论**: 新版成本仅增加约50-80%，但真实感和一致性显著提升，值得！

---

## 🎯 最佳实践

### 1. 对话历史管理

```python
# 定期清理过长的历史（如果需要）
MAX_MESSAGES = 50

if len(history.messages) > MAX_MESSAGES:
    system_msgs = [m for m in history.messages if m['role'] == 'system']
    recent_msgs = history.messages[-MAX_MESSAGES:]
    history.messages = system_msgs + recent_msgs
```

### 2. 温度设置

```python
# 需要高一致性（量表评分）
result = engine.run_study(config, personas, temperature=0.3)

# 平衡模式（推荐）
result = engine.run_study(config, personas, temperature=0.7)

# 探索性研究
result = engine.run_study(config, personas, temperature=0.9)
```

### 3. 检查点使用

```python
# 启用检查点（长期研究必备）
result = engine.run_study(
    config=study,
    personas=personas,
    save_checkpoints=True  # 每波次后保存
)

# 如果中断，可以加载继续
engine.load_conversation_histories(study.study_id)
```

---

## 🐛 常见问题

### Q: 新版会不会太慢？
A: 由于需要处理更多上下文，每个请求可能慢10-20%，但整体研究时间几乎一样。

### Q: 对话历史会不会超出token限制？
A: DeepSeek支持32K上下文，正常的9波次研究不会超出。如果担心，可以手动清理旧消息。

### Q: 可以混用两个版本吗？
A: 可以，它们是独立的模块。但建议在同一个研究中只用一个版本。

### Q: 旧版会被废弃吗？
A: 不会。旧版会继续保留用于简单场景和向后兼容。

---

## 📊 实际案例对比

### 场景：压力干预研究

**旧版响应示例**:
```
波次1: "我的压力是7分，因为工作很忙"
波次2: "我的压力大约是6分吧"  # 没有参考前面的7分
波次3（干预）: "好的，我会试试冥想"
波次4: "我的压力是5分"  # 不记得干预内容
```

**新版响应示例**:
```
波次1: "我的压力是7分，因为项目deadline很紧"
波次2: "相比上周的7分，现在大约是6分，稍微好一点了"  # 记住了！
波次3（干预）: "我理解了，冥想可以降低压力，我会尝试的"
波次4: "我按照上次介绍的方法尝试了冥想，压力从之前的6分降到了5分"  # 完全连贯！
```

---

## 🎓 学习路径

1. **入门**: 阅读 `LONGITUDINAL_GUIDE.md`
2. **实践**: 运行 `examples/longitudinal_study_demo.py`
3. **定制**: 根据你的研究需求修改参数
4. **进阶**: 查看 `API_GUIDE.md` 了解所有选项

---

## 🤝 反馈和贡献

如果你有任何问题或建议：
- 📝 提交 Issue
- 💬 参与 Discussions  
- 🔧 提交 Pull Request

---

## 📅 更新日志

### 2023-10-28 - 重大更新

✅ 新增 `longitudinal_study.py` 模块  
✅ 实现多轮对话机制  
✅ 添加对话历史管理  
✅ 创建完整文档和示例  
✅ 更新导出配置  

---

**推荐所有新项目使用新版纵向研究功能！** 🚀

获得最真实、最连贯、最有价值的模拟研究结果！
