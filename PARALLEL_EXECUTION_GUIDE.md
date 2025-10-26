# ⚡ 并行执行功能说明

## 📋 功能概述

本系统现已支持**并行请求执行**，可将模拟速度提升 **5-30 倍**！

### ✅ 支持的 API 类型

| API 类型 | 并行支持 | 速度提升 | 成本 |
|---------|---------|---------|------|
| **Local (LM Studio)** | ❌ 不支持 | 1x (基准) | 免费 |
| **DeepSeek** | ✅ 支持 | 5-20x | 极低 (~$0.0001/call) |
| **OpenAI** | ✅ 支持 | 5-30x | 中等 (~$0.001/call) |
| **Custom Cloud API** | ✅ 支持 | 5-30x | 取决于提供商 |

---

## 🚀 如何使用

### **步骤 1: 在首页配置 API**

1. 打开 `app.py` (首页)
2. 选择 API 提供商：
   - **DeepSeek** (推荐 - 便宜且快速)
   - **OpenAI** (最强大但较贵)
   - **Custom OpenAI-Compatible**

3. 输入 API Key

4. **查看并行设置区域** (自动显示):
   ```
   ⚡ Parallel Execution Settings
   
   [✓] Enable Parallel Requests
   
   Concurrent Workers: [5] ━━━━━━━━━━━ (1-20)
   
   Estimated Speedup: ~5x faster
   
   Example: 100 personas × 10 questions
   - Sequential: ~33 minutes
   - Parallel (5 workers): ~6 minutes
   ```

5. 调整 **Concurrent Workers** (并发数):
   - **5-10**: 安全且快速 ✅
   - **10-15**: 更快，但可能遇到速率限制 ⚠️
   - **15-20**: 最快，但需要高级 API 账户 🚨

---

### **步骤 2: 运行模拟**

1. 进入 **Simulation 页面**
2. 选择模式 (Survey / Message Testing / A/B Testing)
3. 选择 personas 和问题
4. 点击 **"Run Simulation"**

系统会自动：
- ✅ 检测是否启用了并行模式
- ✅ 使用异步并发执行 (云 API)
- ✅ 或使用序列执行 (本地 LM Studio)

---

## 📊 性能对比示例

### **场景: 100 个 personas × 10 个问题 = 1000 次调用**

| 配置 | 执行时间 | 加速比 | 成本 |
|------|---------|--------|------|
| **LM Studio (序列)** | ~33 分钟 | 1x | $0 |
| **DeepSeek (5 并发)** | ~6 分钟 | 5.5x | ~$0.14 |
| **DeepSeek (10 并发)** | ~3 分钟 | 11x | ~$0.14 |
| **OpenAI GPT-3.5 (5 并发)** | ~6 分钟 | 5.5x | ~$1.50 |
| **OpenAI GPT-4 (5 并发)** | ~6 分钟 | 5.5x | ~$30 |

---

## ⚙️ 技术实现

### **架构**

```
┌─────────────────────────────────────┐
│   Streamlit UI (pages/2_Simulation.py)   │
└─────────────────┬───────────────────┘
                  │
    ┌─────────────┴──────────────┐
    │                            │
    ▼                            ▼
┌──────────────────┐    ┌──────────────────────┐
│ SimulationEngine │    │ ParallelSimulationEngine │
│   (Sequential)   │    │     (Async/Parallel)     │
└─────────┬────────┘    └──────────┬───────────┘
          │                        │
          ▼                        ▼
    ┌────────────┐          ┌────────────────┐
    │ LMStudioClient │      │ AsyncLLMClient │
    │   (Sync)   │          │   (Async)      │
    └────────────┘          └────────────────┘
```

### **关键代码**

#### **1. 异步 LLM 客户端** (`src/llm_client.py`)

```python
class AsyncLLMClient:
    async def generate_response_async(self, prompt: str, ...) -> str:
        """异步生成响应，支持并发"""
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                data = await response.json()
                return data['choices'][0]['message']['content']
```

#### **2. 并行模拟引擎** (`src/simulation.py`)

```python
class ParallelSimulationEngine:
    async def run_survey_parallel(self, personas, questions, ...):
        """并行执行所有 persona-question 组合"""
        semaphore = Semaphore(self.max_workers)  # 限流
        
        async def process_single_query(persona, question):
            async with semaphore:
                return await self.async_client.generate_response_async(...)
        
        tasks = [process_single_query(p, q) for p in personas for q in questions]
        results = await asyncio.gather(*tasks)  # 并行执行
```

#### **3. UI 集成** (`pages/2_Simulation.py`)

```python
if use_parallel:
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()  # 允许嵌套事件循环
    
    parallel_engine = ParallelSimulationEngine(llm_client, max_workers=5)
    result = asyncio.run(parallel_engine.run_survey_parallel(...))
else:
    engine = SimulationEngine(llm_client)
    result = engine.run_survey(...)  # 序列执行
```

---

## 🛡️ 速率限制处理

### **使用 Semaphore 控制并发**

```python
semaphore = Semaphore(max_workers)  # 例如：5

async def limited_request():
    async with semaphore:  # 最多同时 5 个请求
        await make_api_call()
```

### **API 提供商限制**

| 提供商 | 默认限制 | 推荐并发数 |
|--------|---------|-----------|
| DeepSeek Free | 50 requests/min | 5-10 |
| DeepSeek Paid | 500 requests/min | 10-20 |
| OpenAI Tier 1 | 3 requests/min | 2-3 |
| OpenAI Tier 3 | 3500 requests/min | 10-20 |

---

## 📝 使用建议

### **何时使用并行？**

✅ **适合场景:**
- 大规模调研 (50+ personas)
- 使用云 API (DeepSeek/OpenAI)
- 时间敏感的项目

❌ **不适合场景:**
- 本地 LM Studio (不会更快)
- 小规模测试 (<10 queries)
- API 账户有严格速率限制

### **优化建议**

1. **从小开始**: 先用 5 个并发测试
2. **监控进度**: 查看是否有错误
3. **逐步增加**: 如果稳定，可增加到 10-15
4. **设置重试**: 处理偶发的超时错误

---

## 🐛 故障排查

### **问题: 并行选项不显示**

**原因**: 选择了 Local (LM Studio)

**解决**: 切换到 DeepSeek 或 OpenAI

---

### **问题: 遇到速率限制错误**

**症状**:
```
Error 429: Too Many Requests
```

**解决**:
1. 降低 Concurrent Workers (例如从 10 → 5)
2. 等待 1 分钟后重试
3. 升级 API 账户 tier

---

### **问题: 部分请求失败**

**原因**: 网络不稳定或超时

**解决**: 系统会自动返回 `[Error: No response]`，检查网络连接

---

## 📈 性能监控

### **查看实时进度**

```
⚡ Progress: 234/1000 (23.4%)
```

### **查看完成统计**

模拟完成后会显示：
- ✅ 成功响应数
- ❌ 失败响应数
- ⏱️ 总耗时
- 💰 预估成本

---

## 🔒 安全提示

1. **不要在代码中硬编码 API Key**
2. **使用环境变量** (`.env` 文件)
3. **定期轮换 API Key**
4. **监控 API 使用量**，避免意外高额账单

---

## 📞 技术支持

如有问题，请检查：

1. **依赖安装**: `pip install -r requirements.txt`
2. **必需包**: `aiohttp`, `nest-asyncio`
3. **Python 版本**: >= 3.8

---

## 📜 更新日志

### v1.0 (2025-10-25)
- ✅ 添加异步 LLM 客户端
- ✅ 实现并行模拟引擎
- ✅ UI 自动检测并显示并行选项
- ✅ 支持 Survey 和 Message Testing 模式
- ✅ 添加并发数控制和进度反馈

---

**🎉 享受 5-30 倍的速度提升！**
