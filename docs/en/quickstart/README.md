# Quick Start Guide

Get started with Auto Sim AI in 5 minutes!

---

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **LLM Provider** (choose one):
  - LM Studio (local, free)
  - DeepSeek/OpenAI API key

---

## 🚀 Installation

### Option 1: Using Setup Script (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai

# 2. Run the setup script
chmod +x setup.sh
./setup.sh

# 3. Start the application
streamlit run app.py
```

### Option 2: Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the application
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## ⚙️ LLM Configuration

### Option A: Local LM Studio (Recommended for Beginners)

**Advantages**: Free, private, no API key required

1. **Download LM Studio**
   - Visit [lmstudio.ai](https://lmstudio.ai/)
   - Download the version for your OS

2. **Download a Model**
   - Open LM Studio
   - Click the 🔍 search icon
   - Search for recommended models:
     - `mistral-7b-instruct-v0.2` (recommended)
     - `llama-2-7b-chat`
     - `yi-6b-chat`
   - Click download (7B models need ~4-8GB)

3. **Start the Server**
   - Click the **↔️ Local Server** tab
   - Select your downloaded model from the dropdown
   - Click **Start Server**
   - Wait for "Server running on http://localhost:1234"

4. **Connect in the App**
   - In the app homepage, select "Local (LM Studio)"
   - Default address: `http://127.0.0.1:1234/v1`
   - Click **Test Connection**
   - You should see "✅ System Ready!"

### Option B: DeepSeek API (Recommended for Production)

**Advantages**: Fast, cheap (¥0.001/1K tokens), Chinese-optimized

1. **Get API Key**
   - Visit [platform.deepseek.com](https://platform.deepseek.com)
   - Sign up/log in
   - Go to API Keys page
   - Create a new API Key
   - Copy and save it (shown only once!)

2. **Configure in the App**
   - In the app homepage, select "DeepSeek"
   - Paste your API Key
   - Model name: `deepseek-chat` (auto-filled)
   - Click **Test Connection**

### Option C: OpenAI API

1. **Get API Key**
   - Visit [platform.openai.com](https://platform.openai.com)
   - Create account or log in
   - Navigate to API keys
   - Create new key

2. **Configure in the App**
   - Select "OpenAI"
   - Enter your API key
   - Choose model (e.g., `gpt-3.5-turbo`, `gpt-4`)

---

## 🎯 Run Your First Simulation

### Method 1: Survey Mode (Recommended for Beginners)

**Use Case**: Test complete questionnaires with standardized questions

1. **Navigate to Simulation Page**
   - Click **"2_Simulation"** in the sidebar
   - Select **"Survey"** mode

2. **Configure LLM** (if not done)
   - Choose your LLM provider
   - Test connection

3. **Upload Survey Configuration**
   - Click **"Upload Survey JSON"**
   - Select a config file from `data/survey_configs/`
   - Or use the built-in **"Political Orientation Survey"** example

4. **Generate Personas**
   - Click **"Generate Personas"**
   - Select from `data/personas/` or use built-in examples
   - Configure sample size (e.g., 100 personas)

5. **Run Simulation**
   - Click **"Start Simulation"**
   - Watch real-time progress
   - View results in the **Results** page

### Method 2: Message Testing Mode

**Use Case**: Test single messages/questions before adding to formal surveys

1. **Select "Message Testing" Mode**
   
2. **Enter Your Message**
   ```
   Example: "Do you support environmental protection policies?"
   ```

3. **Choose Response Format**
   - Likert scale (1-5, 1-7)
   - Multiple choice
   - Open-ended text

4. **Run Quick Test**
   - Start simulation
   - Get instant feedback
   - Refine your question

### Method 3: A/B Testing Mode

**Use Case**: Compare two versions of a question/message

1. **Select "A/B Testing" Mode**

2. **Enter Two Versions**
   ```
   Version A: "Do you agree with this policy?"
   Version B: "To what extent do you support this policy?"
   ```

3. **Configure Test**
   - Choose sample split (50/50 or custom)
   - Set response format

4. **Compare Results**
   - View side-by-side comparison
   - Statistical significance testing
   - Export comparison report

---

## 📊 View Results

1. **Navigate to Results Page**
   - Click **"3_Results"** in the sidebar

2. **Select Your Simulation**
   - Browse saved results
   - Filter by date, mode, or project name

3. **Analyze Data**
   - **Descriptive Statistics**: mean, median, std dev
   - **Distribution Charts**: histograms, bar charts
   - **Raw Responses**: view individual persona answers
   - **Export Options**: CSV, JSON formats

4. **Download Data**
   - Click **"Export to CSV"**
   - Use data for further analysis in R/Python/SPSS

---

## 🔄 Longitudinal Study (Multi-Wave Research)

**Use Case**: Track opinion changes over time, test interventions

1. **Navigate to Simulation Page**
   - Select **"Survey"** mode

2. **Create a Longitudinal Study**
   - Click **"Enable Longitudinal Study"**
   - Configure waves:
     ```
     Wave 1: Baseline survey (T0)
     Wave 2: Follow-up after intervention (T1)
     Wave 3: Final measurement (T2)
     ```

3. **Design Intervention** (optional)
   - Add treatment messages between waves
   - Example: "Recent studies show climate change accelerating..."

4. **Run Multi-Wave Simulation**
   - System tracks persona memory across waves
   - Personas remember previous responses
   - Analyze within-person changes

5. **Analyze Longitudinal Data**
   - View wave-by-wave changes
   - Track individual trajectories
   - Export for statistical analysis (mixed models, GEE, etc.)

**Example Use Cases**:
- Opinion change after exposure to information
- Treatment effect studies
- Panel surveys
- Intervention effectiveness research

---

## 💡 Tips for Best Results

### LLM Selection

- **Local Models** (LM Studio):
  - ✅ Free, private
  - ✅ Good for development/testing
  - ❌ Slower than APIs
  - ❌ Quality depends on model size

- **DeepSeek API**:
  - ✅ Very cost-effective (¥0.001/1K tokens)
  - ✅ Excellent Chinese language support
  - ✅ Fast inference
  - ✅ Good reasoning capabilities

- **OpenAI GPT-4**:
  - ✅ Highest quality responses
  - ✅ Best for complex reasoning
  - ❌ More expensive
  - ✅ Best for final/production runs

### Persona Design

- **Use diverse personas** for realistic simulations
- **Include demographic variety**: age, gender, location, education
- **Define clear attitudes** when testing opinion-based surveys
- **Be specific**: "35-year-old teacher in rural area" vs "adult"

### Survey Design

- **Clear questions**: Avoid ambiguous wording
- **Appropriate scale**: Use validated scales when possible
- **Test incrementally**: Start with Message Testing before full Survey mode
- **Use A/B testing**: Compare question wordings

### Sample Size

- **Message Testing**: 20-50 personas (quick feedback)
- **Survey Testing**: 100-200 personas (reliable patterns)
- **Final Validation**: 300-500 personas (statistical power)
- **Longitudinal Studies**: 150+ per wave (account for attrition)

---

## 🆘 Troubleshooting

### Connection Issues

**Problem**: "Connection failed" with LM Studio

```bash
# Solution 1: Check if server is running
# In LM Studio, verify "Server running" message

# Solution 2: Check port
# Default is 1234, verify in LM Studio settings

# Solution 3: Try alternative address
http://localhost:1234/v1
http://127.0.0.1:1234/v1
```

**Problem**: DeepSeek API errors

```python
# Check API key validity
# Go to platform.deepseek.com -> API Keys
# Ensure key is active and has credits
```

### Performance Issues

**Problem**: Simulation is slow

```
Solutions:
1. Use async mode (enabled by default)
2. Reduce concurrent requests in Settings
3. Switch to faster LLM (DeepSeek > local models)
4. Reduce sample size for testing
```

### Data Issues

**Problem**: Results not showing

```bash
# Check data directory
ls data/results/

# Verify permissions
chmod -R 755 data/

# Check logs
tail -f logs/app.log
```

---

## 📚 Next Steps

1. **Explore Advanced Features**
   - [Longitudinal Studies](../longitudinal/README.md)
   - [API Reference](../api/README.md)
   - [Architecture Guide](../architecture/README.md)

2. **Customize Your Research**
   - Create custom survey configurations
   - Design your own personas
   - Build intervention studies

3. **Contribute**
   - [Contributing Guide](../contributing/README.md)
   - Report bugs on GitHub
   - Share your research use cases

---

## 🎓 Example Research Workflows

### Workflow 1: Survey Pre-testing

```
1. Draft survey questions
2. Test each question in Message Testing mode (n=30)
3. Refine wording based on response quality
4. Run full Survey simulation (n=200)
5. Analyze distributions and validity
6. Deploy finalized survey to real respondents
```

### Workflow 2: Intervention Study

```
1. Create baseline survey (Wave 1)
2. Run initial simulation (n=300)
3. Design intervention message
4. Run Wave 2 with intervention
5. Compare T0 vs T1 responses
6. Analyze treatment effects
7. Design real-world intervention
```

### Workflow 3: Question Wording A/B Test

```
1. Create two question versions
2. Run A/B test (n=100 per version)
3. Compare response distributions
4. Test statistical significance
5. Choose optimal wording
6. Validate in full Survey mode
```

---

**Need Help?**

- 📖 [Full Documentation](../README.md)
- 💬 [GitHub Issues](https://github.com/jason-jj-li/auto_sim_ai/issues)
- 📧 Contact: jason-jj-li@outlook.com

**Happy Simulating! 🚀**
