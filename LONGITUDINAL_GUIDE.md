# 纵向研究功能使用指南

## 概述

本项目提供了两种纵向研究实现：

1. **旧版 (`intervention_study.py`)** - 基础版本，每个波次独立
2. **新版 (`longitudinal_study.py`)** - ⭐ **推荐使用** - 使用多轮对话保持记忆

## 🆕 新版纵向研究 - 带对话记忆

新版本采用 DeepSeek 的多轮对话机制，让虚拟人物在不同波次之间保持连贯的"记忆"。

### 核心特性

✅ **对话记忆** - 人物记住之前的所有对话  
✅ **时间感知** - 模拟时间流逝和变化  
✅ **上下文连贯** - 响应更真实、一致  
✅ **检查点保存** - 每波次后自动保存  
✅ **对话历史追踪** - 完整保存所有对话

### 工作原理

#### 多轮对话机制

每个虚拟人物维护一个完整的对话历史：

```python
# 第一波（基线）
messages = [
    {"role": "system", "content": "你是李明，32岁软件工程师..."},
    {"role": "user", "content": "你的压力水平如何（1-10分）？"},
    {"role": "assistant", "content": "我会说是7分。工作很忙..."}
]

# 第二波（7天后）
messages.append({"role": "user", "content": "已经过去7天了，你的压力水平现在如何？"})
# 模型会参考之前的7分和原因，给出连贯的回答

# 第三波（干预）
messages.append({"role": "user", "content": "请阅读这个冥想干预信息..."})
messages.append({"role": "assistant", "content": "我理解了这个冥想方法..."})

# 第四波（干预后）
messages.append({"role": "user", "content": "干预后一周，你的压力水平如何？"})
# 模型会参考干预内容和之前的压力水平
```

### 快速开始

#### 1. 导入模块

```python
from src import (
    LMStudioClient,
    PersonaManager,
    LongitudinalStudyEngine,
    LongitudinalStudyBuilder
)
```

#### 2. 创建研究设计

```python
# 创建前后测设计
study_config = LongitudinalStudyBuilder.create_pre_post_study(
    study_name="冥想干预纵向研究",
    
    # 基线问题（所有波次都问）
    baseline_questions=[
        "请用1-10分评价你当前的压力水平？",
        "你的睡眠质量如何？",
        "你的整体幸福感如何？"
    ],
    
    # 干预内容
    intervention_text="""
研究表明，每天进行10分钟的正念冥想可以：
• 降低30%的压力水平
• 改善睡眠质量50%
• 提升整体幸福感

我们邀请你在接下来的30天内，每天早晨或睡前进行10分钟冥想练习。
你可以使用手机上的冥想APP（如Calm、Headspace等）。

请尝试坚持至少21天，以形成习惯。
    """,
    
    # 干预后额外问题
    followup_questions=[
        "请用1-10分评价你当前的压力水平？",
        "你的睡眠质量如何？",
        "你的整体幸福感如何？",
        "你是否尝试了冥想练习？",  # 额外问题
        "如果尝试了，有什么感受和变化？"  # 额外问题
    ],
    
    # 研究参数
    num_pre_waves=3,      # 干预前3个波次（基线）
    num_post_waves=5,     # 干预后5个波次（随访）
    days_between_waves=7  # 每周一次测量
)

print(f"研究设计: {len(study_config.waves)} 个波次")
for wave in study_config.waves:
    print(f"  波次 {wave.wave_number}: {wave.wave_name} (第{wave.days_from_baseline}天)")
```

#### 3. 准备虚拟人物

```python
# 加载或创建虚拟人物
persona_manager = PersonaManager()
persona_manager.load_from_file("data/personas/my_personas.json")
personas = persona_manager.get_all_personas()[:5]  # 使用前5个
```

#### 4. 运行研究

```python
# 初始化LLM客户端
client = LMStudioClient(
    base_url="https://api.deepseek.com/v1",
    api_key="your-api-key"
)

# 创建纵向研究引擎
engine = LongitudinalStudyEngine(
    llm_client=client,
    storage_dir="data/longitudinal_studies"
)

# 进度回调
def on_progress(message):
    print(f"📊 {message}")

# 运行完整研究
result = engine.run_study(
    config=study_config,
    personas=personas,
    temperature=0.7,
    max_tokens=300,
    progress_callback=on_progress,
    save_checkpoints=True  # 每波次后保存
)

print(f"\n✅ 研究完成！")
print(f"研究ID: {result.study_id}")
print(f"参与人数: {len(result.persona_results)}")
print(f"总波次: {len(study_config.waves)}")
```

#### 5. 查看结果

```python
# 查看某个人物的所有波次响应
persona_name = "李明"
if persona_name in result.persona_results:
    waves = result.persona_results[persona_name]
    
    for wave_result in waves:
        print(f"\n{'='*50}")
        print(f"波次 {wave_result.wave_number}: {wave_result.wave_name}")
        print(f"{'='*50}")
        
        for response_data in wave_result.responses:
            print(f"\nQ: {response_data['question']}")
            print(f"A: {response_data['response']}")
            print(f"时间: {response_data['timestamp']}")

# 查看对话历史（完整的multi-turn记录）
if persona_name in engine.conversation_histories:
    history = engine.conversation_histories[persona_name]
    print(f"\n完整对话历史 ({len(history.messages)} 条消息):")
    for msg in history.messages[:10]:  # 显示前10条
        print(f"[{msg['role']}] {msg['content'][:100]}...")
```

### 完整示例

```python
from src import (
    LMStudioClient,
    PersonaManager,
    LongitudinalStudyEngine,
    LongitudinalStudyBuilder,
    Persona
)

# 1. 创建虚拟人物
personas = [
    Persona(
        name="张伟",
        age=28,
        gender="男",
        occupation="软件工程师",
        background="在互联网公司工作，经常加班到深夜，感觉压力很大，睡眠质量不好",
        personality_traits=["内向", "完美主义", "焦虑"],
        values=["职业发展", "健康", "工作生活平衡"],
        education="本科",
        location="北京"
    ),
    Persona(
        name="李娜",
        age=35,
        gender="女",
        occupation="护士",
        background="在医院工作，轮班制，经常需要照顾病人到深夜，同时还要照顾家里的孩子",
        personality_traits=["外向", "有责任心", "容易焦虑"],
        values=["家庭", "帮助他人", "健康"],
        education="本科",
        location="上海"
    )
]

# 2. 初始化LLM
client = LMStudioClient(
    base_url="https://api.deepseek.com/v1",
    api_key="your-deepseek-api-key"
)

# 3. 创建研究设计
study = LongitudinalStudyBuilder.create_pre_post_study(
    study_name="冥想压力干预研究",
    baseline_questions=[
        "请用1-10分评价你当前的压力水平，并简单说明原因",
        "你最近的睡眠质量如何（1-10分）？",
    ],
    intervention_text="""
我们向你介绍一个简单的压力管理方法：正念冥想。

研究显示，每天10分钟的冥想可以：
• 显著降低压力激素水平
• 改善睡眠质量
• 提升注意力和工作效率

方法很简单：
1. 找一个安静的地方坐下
2. 闭上眼睛，专注于呼吸
3. 当思绪飘走时，轻轻拉回到呼吸上
4. 持续10分钟

请在接下来的4周内，每天尝试练习10分钟。
    """,
    followup_questions=[
        "请用1-10分评价你当前的压力水平",
        "你的睡眠质量如何（1-10分）？",
        "你尝试冥想练习了吗？感觉如何？"
    ],
    num_pre_waves=2,
    num_post_waves=4,
    days_between_waves=7
)

# 4. 运行研究
engine = LongitudinalStudyEngine(llm_client=client)

result = engine.run_study(
    config=study,
    personas=personas,
    temperature=0.7,
    max_tokens=300,
    progress_callback=lambda msg: print(f"📊 {msg}"),
    save_checkpoints=True
)

# 5. 保存对话历史
engine.save_conversation_histories(study.study_id)

# 6. 分析结果
print(f"\n{'='*60}")
print(f"研究完成分析")
print(f"{'='*60}")

for persona_name, waves in result.persona_results.items():
    print(f"\n👤 {persona_name}")
    print(f"   完成波次: {len(waves)}")
    
    # 提取压力分数变化
    stress_scores = []
    for wave in waves:
        for resp in wave.responses:
            if "压力" in resp['question']:
                # 简单提取数字（实际应用中需要更robust的解析）
                import re
                numbers = re.findall(r'\d+', resp['response'])
                if numbers:
                    stress_scores.append(int(numbers[0]))
                break
    
    if stress_scores:
        print(f"   压力水平变化: {stress_scores}")
        print(f"   基线平均: {sum(stress_scores[:2])/2:.1f}")
        print(f"   随访平均: {sum(stress_scores[2:])/len(stress_scores[2:]):.1f}")

print(f"\n✅ 结果已保存到: data/longitudinal_studies/{study.study_id}_final.json")
```

### 高级功能

#### 多点干预设计

```python
# 创建有多个干预点的研究
study = LongitudinalStudyBuilder.create_multiple_intervention_study(
    study_name="多阶段健康干预",
    baseline_questions=["你的健康状况如何？"],
    interventions=[
        {
            "wave_number": 3,
            "text": "第一阶段：开始每天步行30分钟",
            "questions": ["你会尝试这个运动计划吗？"]
        },
        {
            "wave_number": 6,
            "text": "第二阶段：在运动基础上，增加健康饮食",
            "questions": ["你觉得饮食调整可行吗？"]
        },
        {
            "wave_number": 9,
            "text": "第三阶段：加入冥想和睡眠管理",
            "questions": ["综合干预对你有帮助吗？"]
        }
    ],
    total_waves=12,
    days_between_waves=7
)
```

#### 恢复中断的研究

```python
# 如果研究中断，可以加载对话历史继续
engine = LongitudinalStudyEngine(llm_client=client)
engine.load_conversation_histories("study_id_20231028")

# 然后继续从某个波次开始
# (需要手动实现波次跳过逻辑)
```

#### 导出和分析

```python
import json

# 导出完整结果
with open("study_results.json", "w", encoding="utf-8") as f:
    json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

# 导出对话历史
engine.save_conversation_histories(study.study_id)

# 分析对话历史
for persona_name, history in engine.conversation_histories.items():
    print(f"\n{persona_name} 的对话统计:")
    print(f"  总消息数: {len(history.messages)}")
    print(f"  用户消息: {sum(1 for m in history.messages if m['role'] == 'user')}")
    print(f"  助手回复: {sum(1 for m in history.messages if m['role'] == 'assistant')}")
```

## 对比：新版 vs 旧版

| 特性 | 旧版 (intervention_study.py) | 新版 (longitudinal_study.py) |
|------|---------------------------|---------------------------|
| 对话记忆 | ❌ 每波次独立 | ✅ 完整的多轮对话历史 |
| 响应一致性 | ⚠️ 可能不一致 | ✅ 高度一致 |
| 时间感知 | ⚠️ 有限 | ✅ 强时间进程感知 |
| 干预记忆 | ❌ 容易忘记 | ✅ 持续记住干预内容 |
| API调用 | 每次独立调用 | 完整上下文调用 |
| 真实感 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 复杂度 | 简单 | 中等 |
| 推荐使用 | 简单测试 | ✅ **生产环境** |

## 最佳实践

### 1. 波次设计

- **基线波次**: 至少2-3个波次建立稳定基线
- **干预波次**: 通常在研究中点实施
- **随访波次**: 至少3-5个波次观察效果持续性
- **间隔时间**: 根据研究目标设置（通常7-14天）

### 2. 问题设计

```python
# ✅ 好的问题：具体、可量化、便于追踪
baseline_questions = [
    "请用1-10分评价你当前的压力水平",
    "你每周锻炼多少次？",
    "你的睡眠时长平均是多少小时？"
]

# ❌ 不好的问题：模糊、难以追踪变化
bad_questions = [
    "你感觉怎么样？",
    "最近还好吗？",
    "有什么想说的？"
]
```

### 3. 干预设计

```python
# ✅ 好的干预：清晰、可操作、有理论支持
intervention = """
【压力管理训练】

理论基础：正念减压疗法（MBSR）

具体方法：
1. 每天早晨做10分钟正念冥想
2. 使用4-7-8呼吸法缓解急性压力
3. 睡前写感恩日记

科学证据：
• 8周练习可降低皮质醇水平30%
• 改善睡眠质量50%
• 提升情绪调节能力

请尝试坚持21天培养习惯。
"""

# ❌ 不好的干预：模糊、难以执行
bad_intervention = "请多放松，注意减压。"
```

### 4. 温度设置

```python
# 根据研究目标调整temperature

# 高一致性（适合量表评分）
engine.run_study(config, personas, temperature=0.3)

# 平衡模式（推荐）
engine.run_study(config, personas, temperature=0.7)

# 高多样性（适合开放式探索）
engine.run_study(config, personas, temperature=0.9)
```

### 5. 成本控制

```python
# DeepSeek API 成本估算
# 价格: ¥0.001/千tokens

# 示例研究成本：
# - 5个人物
# - 9个波次
# - 每波次3个问题
# - 每个响应约200 tokens
# 
# 总tokens ≈ 5 × 9 × 3 × 200 = 27,000 tokens
# 成本 ≈ ¥0.027 (不到3分钱)

# 加上对话历史（累积增长）
# 实际成本 ≈ ¥0.05-0.10
```

## 故障排查

### 问题：对话历史过长导致超出限制

```python
# 解决方案：定期清理旧消息
history = engine.conversation_histories[persona_name]

# 只保留最近N轮对话
MAX_MESSAGES = 50
if len(history.messages) > MAX_MESSAGES:
    # 保留system message和最近的消息
    system_msgs = [m for m in history.messages if m['role'] == 'system']
    recent_msgs = history.messages[-MAX_MESSAGES:]
    history.messages = system_msgs + recent_msgs
```

### 问题：响应不一致

```python
# 解决方案：
# 1. 降低temperature
# 2. 在system message中强调一致性
# 3. 添加明确的时间提示
```

### 问题：忘记干预内容

```python
# 解决方案：在每个干预后波次重新提及
wave_context = f"""
已经过去{days_since_intervention}天。
回顾一下，在第{intervention_wave}波次，你收到了关于{intervention_summary}的信息。
请基于这个信息和你的实践经验来回答。
"""
```

## 输出示例

运行研究后，你会得到：

```
data/longitudinal_studies/
├── meditation_study_20231028_143022_final.json       # 最终结果
├── meditation_study_20231028_143022_conversations.json  # 完整对话历史
├── meditation_study_20231028_143022_checkpoint_wave_1.json  # 检查点
├── meditation_study_20231028_143022_checkpoint_wave_2.json
└── ...
```

## 下一步

1. 查看 `examples/longitudinal_study_demo.py` 获取完整示例
2. 阅读 `API_GUIDE.md` 了解更多API细节
3. 尝试自定义研究设计
4. 探索数据可视化和统计分析

---

**推荐使用新版纵向研究功能，获得最真实、最连贯的模拟结果！** 🚀
