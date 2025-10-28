# 快速开始指南

5分钟上手 LLM Simulation Survey System！

---

## 📋 前置要求

- **Python**: 3.8 或更高版本
- **LLM提供商**（任选其一）:
  - LM Studio（本地，免费）
  - DeepSeek/OpenAI API密钥

---

## 🚀 安装

### 方式一：使用安装脚本（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai

# 2. 运行安装脚本
chmod +x setup.sh
./setup.sh

# 3. 启动应用
streamlit run app.py
```

### 方式二：手动安装

```bash
# 1. 克隆项目
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
streamlit run app.py
```

应用将自动在浏览器打开：`http://localhost:8501`

---

## ⚙️ LLM 配置

### 选项 A：本地 LM Studio（推荐新手）

**优点**: 免费、私密、无需API密钥

1. **下载 LM Studio**
   - 访问 [lmstudio.ai](https://lmstudio.ai/)
   - 下载适合你操作系统的版本

2. **下载模型**
   - 打开 LM Studio
   - 点击 🔍 搜索图标
   - 搜索推荐模型：
     - `mistral-7b-instruct-v0.2` (推荐)
     - `llama-2-7b-chat`
     - `yi-6b-chat`
   - 点击下载（7B模型约需4-8GB空间）

3. **启动服务器**
   - 点击 **↔️ Local Server** 标签
   - 从下拉菜单选择已下载的模型
   - 点击 **Start Server** 按钮
   - 等待显示 "Server running on http://localhost:1234"

4. **在应用中连接**
   - 在应用首页选择 "Local (LM Studio)"
   - 默认地址：`http://127.0.0.1:1234/v1`
   - 点击 **Test Connection**
   - 看到 "✅ System Ready!" 即可开始使用

### 选项 B：DeepSeek API（推荐生产环境）

**优点**: 快速、便宜（¥0.001/千token）、中文优化

1. **获取API密钥**
   - 访问 [platform.deepseek.com](https://platform.deepseek.com)
   - 注册/登录账号
   - 进入 API Keys 页面
   - 创建新的 API Key
   - 复制保存（只显示一次！）

2. **在应用中配置**
   - 在应用首页选择 "DeepSeek"
   - 粘贴你的 API Key
   - 模型名称：`deepseek-chat`（自动填充）
   - 点击 **Test Connection**

3. **环境变量配置（可选）**
   ```bash
   # 复制模板
   cp env.example .env
   
   # 编辑 .env 文件
   echo "DEEPSEEK_API_KEY=your_api_key_here" >> .env
   ```

### 选项 C：OpenAI API

**优点**: 最强性能、最稳定

1. **获取API密钥**
   - 访问 [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - 登录并创建 API Key

2. **在应用中配置**
   - 选择 "OpenAI"
   - 输入 API Key
   - 选择模型（gpt-3.5-turbo 或 gpt-4）
   - 点击 **Test Connection**

---

## 🎯 第一次模拟

### 1. 创建虚拟人物

**方式A：使用演示人物（最快）**

1. 点击页面顶部的 **📋 Setup** 按钮
2. 找到 "Quick Start" 部分
3. 点击 **Create Demo Personas**
4. 等待几秒，系统自动创建5个典型人物
5. 完成！你现在有5个虚拟人物了

**方式B：手动创建**

1. 进入 Setup 页面
2. 填写表单：
   ```
   姓名: 王小明
   年龄: 28
   性别: 男
   职业: 软件工程师
   教育背景: 本科
   居住地: 上海
   背景故事: 在互联网公司工作，经常加班，最近感到压力大...
   性格特征: 内向, 完美主义, 责任心强
   核心价值观: 职业发展, 工作生活平衡, 健康
   ```
3. 点击 **Add Persona**
4. 重复步骤创建更多人物

**方式C：批量导入CSV**

1. 准备CSV文件（参考 `data/samples/personas_template.csv`）
2. 在 Setup 页面找到 "Import from CSV" 部分
3. 上传你的CSV文件
4. 系统自动导入所有人物

### 2. 运行调查模拟

1. 点击 **🎯 Simulation** 按钮
2. 选择 **Survey Mode（调查模式）**
3. **选择人物**: 勾选你想参与的人物（或全选）
4. **选择问卷**:
   - 使用模板：从下拉菜单选择 "PHQ-9 (Depression Screening)"
   - 或输入自定义问题（每行一个问题）
5. **调整设置**（可选）:
   - Temperature: 0.7（默认，推荐）
   - Max Tokens: 300
   - 并发数: 5
6. 点击 **▶️ Run Simulation**
7. 观看实时进度条！

### 3. 查看结果

1. 模拟完成后，点击 **📊 Results** 按钮
2. 浏览最新的模拟结果
3. 查看选项：
   - **By Persona**: 查看每个人物的所有回答
   - **By Question**: 查看每个问题的所有回答
   - **Statistics**: 查看统计分析
4. **导出数据**:
   - CSV格式：用于Excel分析
   - JSON格式：用于程序处理
   - Analysis Script：生成Python/R分析代码

---

## 💡 实例场景

### 场景：测试健康干预信息

**目标**: 了解不同人群对冥想建议的接受度

#### 步骤

1. **创建人物**（或使用演示人物）
   - 确保有不同年龄、职业的人物

2. **切换到 Intervention Mode（干预模式）**
   - 在 Simulation 页面选择 "Intervention"

3. **输入干预文本**:
   ```
   研究表明，每天进行10分钟的正念冥想可以：
   - 降低30%的压力水平
   - 改善睡眠质量
   - 提升专注力和工作效率
   
   建议您尝试30天冥想挑战，每天早晨或睡前花10分钟练习。
   ```

4. **输入后续问题**:
   ```
   1. 您会尝试这个干预方法吗？为什么？
   2. 什么因素可能阻止您尝试？
   3. 如何调整这个建议能让您更愿意尝试？
   ```

5. **运行模拟**

6. **分析结果**:
   - 查看不同年龄/职业人群的接受度
   - 识别常见障碍
   - 优化你的干预信息

---

## 🎨 最佳实践

### 人物设计

✅ **具体详细**
```
好: "35岁护士，单亲妈妈，工作压力大，经常失眠，希望找到简单的压力缓解方法"
差: "中年女性，有压力"
```

✅ **多样化**
- 不同年龄段：20-30岁、31-50岁、51-70岁
- 不同职业：学生、白领、蓝领、退休
- 不同教育背景
- 不同生活情况

### 问题设计

✅ **清晰直接**
```
好: "在过去两周，您有多少天感到心情低落？"
差: "您最近情绪怎么样？"
```

✅ **一次问一件事**
```
好: "您每周锻炼几次？" + "您每次锻炼多久？"
差: "您多久锻炼一次，每次多久，什么强度？"
```

### 温度设置

- **0.3**: 高度一致的回答（适合标准化问卷）
- **0.7**: 平衡真实感和一致性（推荐）
- **1.0**: 更多样化（适合探索性研究）

---

## ⚠️ 常见问题

### 问题：连接失败

**本地模式**:
- ✅ 检查 LM Studio 是否运行
- ✅ 确认服务器地址是 `http://127.0.0.1:1234`
- ✅ 在 LM Studio 中确认模型已加载

**API模式**:
- ✅ 检查网络连接
- ✅ 确认API密钥正确
- ✅ 检查账户余额

### 问题：没有找到模型

**本地模式**:
- 在 LM Studio 中先加载一个模型
- 刷新应用页面

**API模式**:
- 手动输入模型名称（如 `gpt-3.5-turbo`、`deepseek-chat`）

### 问题：响应很慢

**本地模式**:
- 使用更小的模型（7B 而非 13B）
- 在 LM Studio 设置中启用 GPU 加速
- 减少 Max Tokens 设置

**API模式**:
- 检查网络延迟
- 减少并发数
- 考虑换用更快的模型

### 问题：内存不足

- 关闭其他应用程序
- 使用更小的模型
- 减少同时模拟的人物数量
- 在 LM Studio 中降低上下文长度

---

## 📈 下一步

恭喜！你已经掌握基础操作。继续探索：

- 📚 **阅读完整文档**: [README.md](README.md)
- 🔬 **尝试高级功能**: 
  - A/B 测试
  - 敏感性分析
  - 纵向研究
- 🛠️ **自定义开发**: [API_GUIDE.md](docs/API_GUIDE.md)
- 💬 **获取帮助**: [GitHub Issues](https://github.com/jason-jj-li/auto_sim_ai/issues)

---

## 📊 性能参考

| 场景 | 配置 | 预计时间 |
|-----|------|---------|
| 小规模测试 | 5人物 × 9问题 | 2-5分钟 |
| 中等规模 | 20人物 × 15问题 | 10-20分钟 |
| 大规模研究 | 100人物 × 20问题 | 1-2小时 |

*时间基于 DeepSeek API，并发数=10

---

## 💰 成本估算

### 本地 LM Studio
- **成本**: 完全免费
- **要求**: GPU（推荐6GB+显存）

### DeepSeek API
- **价格**: ¥0.001/千tokens
- **示例**: 100人物 × 10问题 ≈ ¥0.50

### OpenAI API
- **GPT-3.5**: ¥0.015/千tokens
- **GPT-4**: ¥0.30/千tokens

---

## 🆘 获取帮助

- 📖 **文档**: [完整README](README.md)
- 🐛 **报告Bug**: [GitHub Issues](https://github.com/jason-jj-li/auto_sim_ai/issues)
- 💡 **功能建议**: [GitHub Discussions](https://github.com/jason-jj-li/auto_sim_ai/discussions)

---

**祝模拟愉快！🎉**

从零到第一次成功模拟：**5分钟** ⏱️
