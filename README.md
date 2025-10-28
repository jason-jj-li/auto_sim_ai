# Auto Sim AI - LLM Survey Simulation System

<div align="center">

**English Version | [中文版](README_zh.md)**

---

🔬 **AI-Powered Survey and Intervention Simulation System**

Simulate real survey research and intervention effects using LLM-driven virtual personas.

🚀 **[Launch Web Application](https://jason-jj-li-auto-sim-ai-app-gkcvcf.streamlit.app)** 🚀

� **[View Complete English Documentation](./docs/en/README.md)**

[Quick Start](./docs/en/quickstart/README.md) •
[Features](#-features) •
[API Reference](./docs/en/api/README.md) •
[Contributing](./docs/en/contributing/README.md)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [User Guide](#user-guide)
- [Architecture](#architecture)
- [Advanced Features](#advanced-features)
- [API Reference](#api-reference)
- [📚 Complete Documentation](#complete-documentation)
  - [Quick Start Guide](./docs/en/quickstart/README.md)
  - [API Guide](./docs/en/api/README.md)
  - [Architecture Guide](./docs/en/architecture/README.md)
  - [Longitudinal Study Guide](./docs/en/longitudinal/README.md)
  - [Contributing Guide](./docs/en/contributing/README.md)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

<a id="overview"></a>
## 🎯 Overview

**LLM Simulation Survey System** is an innovative research toolkit that leverages Large Language Models (LLMs) to generate virtual personas that emulate human responses to surveys and interventions.

### Use Cases

- 🏥 **Health Intervention Research** – Test the impact of health messaging on different populations
- 📊 **Market Research** – Rapidly evaluate user feedback for products or services
- 🎓 **Educational Research** – Assess teaching effectiveness across learner profiles
- 💡 **Policy Analysis** – Anticipate policy impacts on diverse communities
- 🧪 **A/B Testing** – Compare multiple approaches before real-world rollout
- 📈 **Prototype Validation** – Iterate research designs before launching costly studies

### Core Advantages

✅ **Fast Iteration** – Complete hundreds of simulated responses in minutes  
✅ **Cost-Effective** – Eliminate participant recruitment overhead  
✅ **Reproducible** – Precisely control variables for repeatable experiments  
✅ **Diverse** – Create personas covering varied backgrounds, ages, and cultures  
✅ **Deep Insights** – Gather rich qualitative and quantitative outputs  
✅ **Flexible Deployment** – Run locally or through cloud APIs

---

<a id="features"></a>
## 🚀 Features

### Core Capabilities

#### 1️⃣ Virtual Persona Management
- **Rich persona attributes**: age, gender, occupation, education, personality traits, values, and more
- **Batch generation** based on demographic distributions to mirror real populations
- **CSV import/export** for seamless integration with spreadsheets and databases
- **Demo templates** that provide ready-to-use persona examples

#### 2️⃣ Multiple Simulation Modes
- **Survey mode** for standardized questionnaires (PHQ-9, GAD-7, PSS-10, etc.)
- **Intervention mode** to evaluate message impact across audience segments
- **A/B testing** to compare multiple content versions simultaneously
- **Longitudinal studies** for multi-wave tracking with memory
- **Sensitivity analysis** to measure how parameter changes influence outcomes

#### 3️⃣ LLM Integration
- **Local deployment** via LM Studio (free, private, hardware dependent)
- **Commercial APIs**:
  - DeepSeek (cost-effective, Chinese optimized)
  - OpenAI (GPT-4, GPT-3.5)
  - Other OpenAI-compatible providers
- **Flexible switching** to change models and providers without code changes

#### 4️⃣ Advanced Analysis
- **Automatic scoring** for validated scales (PHQ-9, GAD-7, PSS-10, etc.)
- **Statistical summaries** covering descriptive stats, correlations, and group comparisons
- **Consistency checks** to validate response logic and internal coherence
- **Interactive visualizations** including charts, distributions, and word clouds
- **Data exports** to CSV, JSON, or ready-to-run Python/R analysis scripts

#### 5️⃣ Performance Optimization
- **Asynchronous execution** to process many personas in parallel
- **Smart caching** that avoids duplicate LLM calls and reduces cost
- **Checkpointing** for pause-and-resume workflows
- **Progress tracking** with real-time completion estimates

---

<a id="quick-start"></a>
## ⚡ Quick Start

### System Requirements

- **Python**: 3.8 or higher
- **Memory**: 8 GB RAM recommended
- **LLM Provider** (choose one):
  - LM Studio for local, offline inference
  - DeepSeek or OpenAI API key for hosted models

### 1. Clone the Project

```bash
git clone https://github.com/jason-jj-li/auto_sim_ai.git
cd auto_sim_ai
```

### 2. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install runtime requirements
pip install -r requirements.txt
```

Or use the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

### 3. Configure LLM Access

**Option A: LM Studio (local, recommended for development)**

1. Download [LM Studio](https://lmstudio.ai/).
2. Install a compatible model (`mistral-7b-instruct`, `llama-2-7b-chat`, or any 7B+ model).
3. Open the "Local Server" tab, select the model, click **Start Server**, and confirm the endpoint `http://localhost:1234`.

**Option B: Hosted APIs (recommended for production)**

```bash
cp env.example .env
# Edit .env and add your credentials
# DEEPSEEK_API_KEY=your_api_key
# OPENAI_API_KEY=your_api_key
```

### 4. Launch the Streamlit App

```bash
streamlit run app.py
```

The UI will open at `http://localhost:8501`.

### First Run Checklist

1. **Connect the LLM** – Pick a provider, test the connection, and wait for the "System Ready" status.
2. **Create Personas** – Use "Create Demo Personas", manually add entries, or import from CSV.
3. **Run a Simulation** – Choose the mode (survey/intervention/A/B), select personas, set questions, and start the run.
4. **Review Results** – Inspect individual responses, explore analytics, and export data for further analysis.

---

<a id="user-guide"></a>
## 📖 User Guide

### Persona Design Best Practices

#### Create High-Quality Personas

```python
# Strong example: specific, detailed, and believable
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

# Weak example: vague and generic
{
    "name": "John Doe",
    "age": 30,
    "gender": "Male",
    "occupation": "Engineer",
    "background": "Average person",
    "personality_traits": ["Normal"],
    "values": ["Happiness"]
}
```

#### Ensure Persona Diversity

- **Age**: represent multiple age brackets (18–80)
- **Gender**: include male, female, and non-binary identities
- **Occupation**: cover industries and seniority levels
- **Education**: range from high school to graduate degrees
- **Location**: mix of urban, rural, and regional contexts
- **Cultural background**: incorporate different ethnicities, religions, and traditions

### Questionnaire Design Tips

#### Characteristics of Strong Questions

✅ **Clear and specific**
```
Good: In the past two weeks, how many days did you feel down or depressed?
Poor: How have you been feeling lately?
```

✅ **Avoid double-barreled questions**
```
Good: How many times do you exercise each week? How long is each session?
Poor: How often do you exercise, how long, and at what intensity?
```

✅ **Use standardized scales when possible**
```
Never (0) – Rarely (1) – Often (2) – Always (3)
```

#### Leverage Built-In Templates

The app ships with validated questionnaires such as:

- **PHQ-9** for depression screening
- **GAD-7** for anxiety screening
- **PSS-10** for perceived stress
- Additional templates are continuously added

### Simulation Settings

#### Temperature

Controls output variability:

- **0.0 – 0.3**: highly consistent, suited to standardized responses
- **0.5 – 0.7**: balanced; recommended default for most surveys
- **0.8 – 1.0**: diverse and creative; use for exploratory studies

#### Max Tokens

- **150–300**: short answers (Likert items, scale ratings)
- **300–500**: medium-length responses (short answer questions)
- **500–1000**: long-form narratives or in-depth interviews

#### Parallelism

- **Small runs (<10 personas)**: 2–3 concurrent workers
- **Medium runs (10–50 personas)**: 5–10 concurrent workers
- **Large runs (>50 personas)**: 10–15 workers (monitor API rate limits)

---

<a id="architecture"></a>
## 🏗️ Architecture

Refer to the detailed **[Architecture Guide](./docs/en/architecture/README.md)** for diagrams and deep dives.

### Project Layout

```
auto_sim_ai/
├── app.py                      # Streamlit entry point
├── pages/                      # Multi-page UI
│   ├── 1_Setup.py              # Persona management
│   ├── 2_Simulation.py         # Simulation workflows
│   └── 3_Results.py            # Results visualization
├── src/                        # Core engine modules
│   ├── llm_client.py           # LLM clients (sync & async)
│   ├── persona.py              # Persona model utilities
│   ├── simulation.py           # Simulation orchestration
│   ├── storage.py              # Persistent storage helpers
│   ├── cache.py                # Response caching layer
│   ├── checkpoint.py           # Pause/resume checkpoints
│   ├── scoring.py              # Standardized scoring utilities
│   ├── ab_testing.py           # A/B testing helpers
│   ├── intervention_study.py   # Legacy intervention engine
│   ├── longitudinal_study.py   # Recommended longitudinal engine
│   ├── persona_generator.py    # Batch persona generation
│   ├── survey_templates.py     # Questionnaire templates
│   ├── survey_config.py        # Survey configuration schemas
│   ├── tools.py                # Tool registry
│   ├── ui_components.py        # Shared Streamlit widgets
│   ├── styles.py               # Design system definitions
│   └── validators.py           # Input validation rules
├── data/                       # Working data artifacts
│   ├── personas/               # Persona definitions
│   ├── results/                # Simulation outputs
│   ├── cache/                  # Cached LLM responses
│   ├── checkpoints/            # Checkpoint snapshots
│   └── survey_configs/         # Survey configuration bundles
├── docs/                       # Multilingual documentation
├── tests/                      # Automated test suite
├── requirements.txt            # Runtime dependencies
└── pytest.ini                  # Pytest configuration
```

### Core Modules

- **`llm_client.py`** – Unified sync/async clients compatible with LM Studio and OpenAI-style APIs.
- **`simulation.py`** – Sequential and parallel execution engines with retries, aggregation, and progress callbacks.
- **`cache.py`** – Hash-based response caching to reuse identical prompts and cut latency and cost.
- **`scoring.py`** – Automates calculation of standardized scales with support for custom scoring rules.

---

<a id="advanced-features"></a>
## 🔬 Advanced Features

> 💡 **Tip**: Additional usage examples are available in the [API Guide](./docs/en/api/README.md).

### 1. A/B Testing

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

### 2. Longitudinal Studies

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

### 3. Batch Persona Generation

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

### 4. Response Validation

```python
from src import ResponseValidator, ConsistencyChecker

validator = ResponseValidator()
checker = ConsistencyChecker()

is_valid = validator.validate_response(response, question_type)
metrics = checker.check_consistency(persona_responses)
print(metrics.consistency_score)
```

---

<a id="api-reference"></a>
## 🧰 API Reference

### PersonaManager

```python
from src import PersonaManager

manager = PersonaManager()

# Add a persona
manager.add_persona(persona)

# Retrieve all personas
personas = manager.get_all_personas()
# Filter by attributes
young_adults = manager.filter_personas(
    age_range=(18, 30),
manager.load_from_file("personas.json")

### SimulationEngine

```python
from src import SimulationEngine

gine = SimulationEngine(
    llm_client=client,
    cache=cache,
# Run a survey
survey_result = engine.run_survey(
    personas=personas,
    questions=questions,
    temperature=0.7,
    max_tokens=300
)

# Run an intervention
intervention_result = engine.run_intervention(
    personas=personas,
    intervention_text="Health intervention content",
    questions=followup_questions
)
```
from src import ResultsStorage

storage = ResultsStorage()

results = storage.load_all_results()

# Export to CSV
storage.export_to_csv(simulation_result, "output.csv")

# Generate analysis scripts
storage.export_analysis_script(simulation_result, "analysis.py", language="python")
```

---

<a id="complete-documentation"></a>
## 📚 Complete Documentation

- [Quick Start Guide](./docs/en/quickstart/README.md)
- [API Guide](./docs/en/api/README.md)
- [Architecture Guide](./docs/en/architecture/README.md)
- [Longitudinal Study Guide](./docs/en/longitudinal/README.md)
- [Contributing Guide](./docs/en/contributing/README.md)


<a id="faq"></a>
## ❓ FAQ

### How many LLM API calls will I need?


### How long do simulations take?

### How reliable are the results?
LLM simulations are exploratory. They excel at prototyping, hypothesis generation, and pretesting questionnaires but do **not** replace human studies.

### How can I improve response quality?
3. Tune temperature for the desired variability.
5. Enable validation and consistency checks.

### What does it cost?

- **LM Studio**: free (requires capable local hardware)
- **DeepSeek API**: ≈ $0.0001 per 1K tokens
- **OpenAI GPT-3.5**: ≈ $0.002 per 1K tokens
- **OpenAI GPT-4**: ≈ $0.03 per 1K tokens

### Is data secure?

- **Local mode** keeps data on-premises.
- **API mode** follows each provider's privacy policy.
- Prefer local mode for sensitive datasets.

---

<a id="contributing"></a>
## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete workflow.

### Development Setup

```bash
pip install -r requirements-dev.txt
pytest
black src/ tests/
isort src/ tests/
mypy src/
```

### Report Issues

Encountered a bug or have an idea? [Open an issue](https://github.com/jason-jj-li/auto_sim_ai/issues) on GitHub.

---

<a id="license"></a>
## 📄 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

<a id="acknowledgments"></a>
## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) – Python web framework
- [LM Studio](https://lmstudio.ai/) – Local LLM runtime
- [OpenAI](https://openai.com/) – API compatibility standard
- [DeepSeek](https://www.deepseek.com/) – Cost-effective LLM provider

---

<a id="contact"></a>
## 📞 Contact

- **Maintainer**: Jason Li
- **GitHub**: [@jason-jj-li](https://github.com/jason-jj-li)
- **Email**: Please reach out via GitHub issues

---

<div align="center">

**⭐ If this project helps you, please give it a star!**

Made with ❤️ by Jason Li

</div>
