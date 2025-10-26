# Quick Start Guide

Get up and running with the LLM Simulation Survey System in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- LM Studio (for local LLM) OR API key for online provider (DeepSeek, OpenAI, etc.)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the setup script:

```bash
./setup.sh
```

### 2. Set Up Your LLM Provider

**Option A: Local (LM Studio)**

1. Download and install [LM Studio](https://lmstudio.ai/)
2. Download a model (recommended: 7B+ parameters)
   - Click 🔍 Search icon
   - Download: Llama 2 7B, Mistral 7B, or similar
3. Start the local server:
   - Click **↔️ Local Server** tab
   - Click **Start Server** button
   - Wait for "Server running on http://localhost:1234"

**Option B: Online API (DeepSeek, OpenAI)**

1. Get an API key:
   - DeepSeek: https://platform.deepseek.com
   - OpenAI: https://platform.openai.com/api-keys
2. Keep your API key handy (you'll enter it in the app)

## Running the Application

### Start the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### First-Time Setup

1. **Connect to LLM**
   - On the Home page, select your provider
   - For local: Keep default URL (`http://127.0.0.1:1234/v1`)
   - For online: Enter your API key
   - Click **Test Connection**
   - Wait for "System Ready!" message

2. **Create Personas** (Setup page)
   - Click **📋 Setup** button
   - Use **Create Demo Personas** for instant setup
   - OR create custom personas using the form
   - OR upload a CSV file with persona data

3. **Run Your First Simulation** (Simulation page)
   - Click **🎯 Simulation** button
   - Select **Survey** mode
   - Choose personas to include
   - Select a template (e.g., PHQ-9) or enter custom questions
   - Click **Run Simulation**
   - Watch real-time progress!

4. **View Results** (Results page)
   - Click **📊 Results** button
   - Browse simulation results
   - View responses by persona or question
   - Export data as CSV or JSON

## Example Workflow

### Scenario: Testing a Health Message

**Goal:** See how different personas respond to a mental health intervention.

1. **Create Personas** (or use demo personas)
2. **Go to Simulation → Intervention Mode**
3. **Enter Intervention Text:**
   ```
   Taking 10 minutes daily for mindfulness meditation can significantly reduce stress 
   and improve mental wellbeing. Try it for 30 days!
   ```
4. **Enter Follow-up Questions:**
   ```
   How likely are you to try this intervention?
   What barriers might prevent you from trying this?
   What would make this more appealing to you?
   ```
5. **Click Run Simulation**
6. **Analyze Results** to see how different demographics respond

## Tips for Best Results

### Persona Design
- Be specific about background, values, and personality
- Include demographic diversity
- Give personas realistic constraints and motivations

### Question Design
- Ask clear, specific questions
- Avoid overly complex or compound questions
- Consider persona perspective when wording questions

### Model Settings
- **Temperature 0.5-0.7**: Balanced responses (recommended)
- **Temperature 0.0-0.3**: More consistent/focused
- **Temperature 0.8-1.0**: More creative/varied
- **Max Tokens 200-500**: Standard responses
- **Max Tokens 500+**: Detailed responses

### Performance
- Fewer personas = faster simulation
- Shorter questions = faster responses
- Use caching for repeated questions

## Common Issues

### "Connection Refused" Error
- **Local**: Make sure LM Studio server is running
- **Online**: Check your internet connection

### "No Models Found"
- **Local**: Load a model in LM Studio first
- **Online**: Enter model name manually (e.g., "gpt-4", "deepseek-chat")

### Slow Responses
- Use a smaller model (local)
- Reduce number of personas
- Reduce max_tokens setting
- Enable GPU in LM Studio

### Out of Memory
- Close other applications
- Use a smaller model
- Reduce context length in LM Studio

## Next Steps

- **Explore Templates**: Try PHQ-9, GAD-7, or other validated instruments
- **A/B Testing**: Compare different interventions
- **Export Data**: Analyze results in Python, R, or Excel

## Getting Help

- Check the main [README.md](README.md) for detailed information
- Review configuration in Setup page
- Check logs in `logs/` directory for errors

## Resources

- **LM Studio**: https://lmstudio.ai/
- **DeepSeek API**: https://platform.deepseek.com
- **OpenAI API**: https://platform.openai.com
- **Streamlit Docs**: https://docs.streamlit.io

---

**Happy Simulating! 🎯**

Time to first results: **~5 minutes**

