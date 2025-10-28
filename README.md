# Auto Sim AI - LLM Survey Simulation System

**English Version | [中文版](README_zh.md)**

🔬 **AI-Powered Survey and Intervention Simulation System**

Simulate real survey research and intervention effects using LLM-driven virtual personas.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

📖 **[Complete English Documentation](docs/en/README.md)**

- [Quick Start](#quick-start)
- [Features](#features)
- [API Reference](docs/en/api/README.md)
- [Contributing](docs/en/contributing/README.md)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [User Guide](#user-guide)
- [📚 Complete Documentation](#-complete-documentation)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## 🎯 Overview

**LLM Simulation Survey System** is an innovative research tool that leverages Large Language Models (LLMs) to generate virtual personas that simulate real human responses to surveys and interventions.

### Use Cases

- 🏥 **Health Intervention Research** – Test the impact of health messaging on different populations
- 📊 **Market Research** – Rapidly evaluate user feedback for products or services
- 🎓 **Educational Research** – Assess teaching method effectiveness across learner types
- 💡 **Policy Analysis** – Predict potential policy impacts on diverse populations
- 🧪 **A/B Testing** – Compare effectiveness across different approaches
- 📈 **Prototype Validation** – Iterate designs before running real-world research

### Core Advantages

- ✅ **Fast Iteration** – Complete simulations with hundreds of personas in minutes
- ✅ **Cost-Effective** – No need to recruit real participants
- ✅ **Reproducible** – Precisely control variables for repeatable experiments
- ✅ **Diverse** – Create personas spanning varied backgrounds, ages, and cultures
- ✅ **Deep Insights** – Gather rich qualitative and quantitative outputs
- ✅ **Flexible Deployment** – Run locally or via cloud APIs

---

## 🚀 Features

### 1️⃣ Virtual Persona Management

- Rich persona attributes: age, gender, occupation, education, personality traits, values, more
- Batch creation based on demographic distributions
- CSV import/export for Excel or database pipelines
- Ready-to-use demo persona templates

### 2️⃣ Multiple Simulation Modes

- Survey mode for standardized questionnaires (PHQ-9, GAD-7, etc.)
- Intervention mode to evaluate message impact on different personas
- A/B testing to compare multiple content versions
- Longitudinal studies for multi-wave tracking
- Sensitivity analysis to measure parameter influence

### 3️⃣ LLM Integration

- Local deployment through LM Studio (free and private)
- Commercial APIs including DeepSeek, OpenAI (GPT-4, GPT-3.5), and compatible providers
- Seamless provider switching via unified client interfaces

### 4️⃣ Advanced Analysis

- Automatic scoring for standardized scales
- Descriptive stats, correlation analysis, and group comparisons
- Consistency checks for validating answer logic
- Interactive visualizations (charts, word clouds, distributions)
- Exports to CSV, JSON, and ready-to-run Python/R scripts

### 5️⃣ Performance Optimization

- Asynchronous processing for high-throughput simulations
- Smart caching to avoid repeated LLM calls
- Checkpointing for pause-and-resume workflows
- Real-time progress tracking with completion estimates

---

## ⚡ Quick Start

### System Requirements

- Python 3.8 or higher
- 8 GB RAM recommended
- One LLM provider: LM Studio or an API key for DeepSeek/OpenAI

### Installation Steps

```bash
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai
```

#### Option A: Automated Setup (Recommended)

```bash
chmod +x setup.sh
./setup.sh
```

#### Option B: Manual Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure LLM Access

#### Local LM Studio

1. Download [LM Studio](https://lmstudio.ai/).
2. Install a model (`mistral-7b-instruct`, `llama-2-7b-chat`, or any 7B+ model).
3. Start the local server ("Local Server" tab) and confirm `http://localhost:1234`.

#### Online API Provider

```bash
cp env.example .env
# Edit .env and add credentials
# DEEPSEEK_API_KEY=your_key
# or
# OPENAI_API_KEY=your_key
```

### Launch Streamlit App

```bash
streamlit run app.py
```

The UI loads at `http://localhost:8501`.

### First Run Checklist

1. **Connect LLM** – Choose provider, test connection, wait for "System Ready".
2. **Create Personas** – Use "Create Demo Personas", manual entry, or CSV upload.
3. **Run Simulation** – Pick mode (survey/intervention/A/B), select personas, configure questions, run.
4. **Review Results** – Inspect responses, view analytics, export for further study.

---

## 📖 User Guide

### Persona Design Best Practices

```python
# Strong persona: specific, credible, detailed
{
    "name": "Li Ming",
    "age": 32,
    "gender": "Male",
    "occupation": "Software engineer at a startup",
    "education": "BSc Computer Science",
    "location": "Beijing",
    "background": "Works long hours in a fast-growing tech company. Recently stressed with poor sleep. Enjoys exercise but rarely has time.",
    "personality_traits": ["Perfectionist", "Responsible", "Slightly anxious"],
    "values": ["Career growth", "Work-life balance", "Family health"]
}
```

- Cover demographic diversity (age, gender identity, occupation, education, region, culture).
- Provide concrete backgrounds and motivations to guide consistent LLM responses.

### Questionnaire Design Tips

- Ask clear, single-focus questions.
- Avoid multi-part questions; split them instead.
- Use validated scales when possible (PHQ-9, GAD-7, PSS-10).
- Provide answer formats (Likert scales, numeric ranges) in prompts.

### Simulation Settings

- **Temperature**: 0.0–0.3 for consistent responses, 0.5–0.7 balanced (default), 0.8–1.0 exploratory.
- **Max Tokens**: 150–300 for short answers, 300–500 medium, 500–1000 detailed narratives.
- **Parallelism**: 2–3 personas (small runs), 5–10 (medium), 10–15 (large – watch rate limits).

---

## 🏗️ Architecture Design

Project structure highlights:

```
auto_sim_ai/
├── app.py                  # Streamlit entrypoint
├── pages/                  # UI subpages
│   ├── 1_Setup.py          # Persona management
│   ├── 2_Simulation.py     # Simulation workflows
│   └── 3_Results.py        # Results visualization
├── src/                    # Core engine modules
│   ├── llm_client.py       # Sync/async LLM clients
│   ├── persona.py          # Persona model & utilities
│   ├── simulation.py       # Simulation orchestration
│   ├── storage.py          # Persistent results management
│   ├── cache.py            # Response caching layer
│   ├── checkpoint.py       # Pause/resume checkpoints
│   ├── scoring.py          # Survey scoring utilities
│   ├── ab_testing.py       # A/B testing helpers
│   ├── longitudinal_study.py
│   ├── persona_generator.py
│   ├── survey_templates.py
│   ├── survey_config.py
│   ├── tools.py            # Tool registry
│   ├── ui_components.py    # Shared Streamlit widgets
│   ├── styles.py           # Design system
│   └── validators.py       # Input validation
├── tests/                  # Automated tests
├── data/                   # Personas, results, caches
├── docs/                   # Full documentation
├── requirements.txt        # Runtime dependencies
└── pytest.ini              # Test configuration
```

### Core Modules

- **llm_client.py** – Unified interfaces for LM Studio and API providers (sync + async).
- **simulation.py** – Sequential and parallel engines with retries and aggregation.
- **cache.py** – Hash-based cache to reuse identical prompts and save cost.
- **scoring.py** – Automatic scoring for standardized scales with custom rules.

---

## 🔬 Advanced Features

### A/B Testing

```python
from src import ABTestManager, Condition

condition_a = Condition(
    name="Version A",
    intervention_text="Meditating 10 minutes daily reduces stress.",
    questions=["Would you try this method?"]
)

condition_b = Condition(
    name="Version B",
    intervention_text="Studies show daily 10-minute meditation can cut stress by 30%.",
    questions=["Would you try this method?"]
)

manager = ABTestManager()
results = manager.run_test([condition_a, condition_b], personas)
```

### Longitudinal Studies

```python
from src import LongitudinalStudyEngine, WaveConfig, LongitudinalStudyConfig

waves = [
    WaveConfig(
        wave_number=1,
        wave_name="Baseline",
        questions=["Rate your current stress (1-10)."],
        days_from_baseline=0
    ),
    WaveConfig(
        wave_number=2,
        wave_name="1 Month",
        questions=["Rate your current stress (1-10)."],
        days_from_baseline=30,
        intervention_text="Practice 10 minutes of meditation daily."
    )
]

config = LongitudinalStudyConfig(
    study_id="stress",
    study_name="Stress Intervention",
    waves=waves
)

engine = LongitudinalStudyEngine(llm_client)
results = engine.run_study(personas, config)
```

### Batch Persona Generation

```python
from src import PersonaGenerator, DistributionConfig

config = DistributionConfig(
    age_distribution={"18-30": 0.3, "31-50": 0.4, "51-70": 0.3},
    gender_distribution={"Male": 0.48, "Female": 0.52}
)

generator = PersonaGenerator()
personas = generator.generate_batch(
    count=100,
    distribution_config=config,
    llm_client=client
)
```

### Response Validation

```python
from src import ResponseValidator, ConsistencyChecker

validator = ResponseValidator()
checker = ConsistencyChecker()

is_valid = validator.validate_response(response, question_type)
metrics = checker.check_consistency(persona_responses)
print(metrics.consistency_score)
```

---

## 📚 Complete Documentation

- [Quick Start Guide](docs/quickstart/README.md)
- [API Documentation](docs/api/README.md)
- [Architecture Guide](docs/architecture/README.md)
- [Longitudinal Studies Guide](docs/longitudinal/README.md)
- [Contributing Guide](docs/contributing/README.md)

---

## ❓ FAQ

### How many LLM API calls will I need?

Call count = number of personas × number of questions. Example: 10 personas × 9 questions = 90 calls. Caching greatly reduces duplicates.

### How long do simulations take?

- Local model: roughly 5–15 seconds per response
- API model: roughly 1–3 seconds per response
- Parallel execution can reduce runtime by 50–80%

### How reliable are the results?

LLM simulations are exploratory—ideal for prototyping, hypothesis generation, and pretesting questionnaires. They do **not** replace human studies.

### How can I improve response quality?

1. Provide rich persona backgrounds.
2. Ask precise, scoped questions.
3. Tune temperature for the desired variability.
4. Use higher-quality models when possible.
5. Enable validation and consistency checks.

### What does it cost?

- LM Studio: free (requires capable hardware)
- DeepSeek API: ≈ $0.0001 per 1k tokens
- OpenAI GPT-3.5: ≈ $0.002 per 1k tokens
- OpenAI GPT-4: ≈ $0.03 per 1k tokens

### Is data secure?

- Local mode keeps data on-premises.
- API mode follows provider privacy policies.
- Prefer local mode for sensitive datasets.

---

## 🤝 Contributing

We welcome contributions! Read [CONTRIBUTING.md](CONTRIBUTING.md) for workflow details.

```bash
pip install -r requirements-dev.txt
pytest
black src/ tests/
isort src/ tests/
mypy src/
```

Report bugs or ideas via [GitHub issues](https://github.com/jason-jj-li/auto_sim_ai/issues).

---

## 📄 License

Released under the MIT License. Refer to [LICENSE](LICENSE).

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) – Python web framework
- [LM Studio](https://lmstudio.ai/) – Local LLM runtime
- [OpenAI](https://openai.com/) – API compatibility standard
- [DeepSeek](https://www.deepseek.com/) – Cost-effective LLM provider

---

## 📞 Contact

- Maintainer: Jason Li
- GitHub: [@jason-jj-li](https://github.com/jason-jj-li)
- Email: please reach out via GitHub issues

---

**⭐ If this project helps you, consider starring the repository.**
