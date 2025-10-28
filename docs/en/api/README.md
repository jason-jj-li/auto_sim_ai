# API Reference Guide

Complete API documentation and code examples for Auto Sim AI.

> ⚠️ **Note**: This documentation reflects the current version of the system. Previous advanced features (`StatisticalAnalyzer`, `ScriptGenerator`, `SensitivityAnalyzer`, `ProjectManager`, `ResponseValidator`, `SimulationEstimator`) have been removed as they lacked UI support. The current system focuses on core simulation features with complete UI coverage.

---

## 📋 Table of Contents

- [Core Modules](#core-modules)
  - [LLM Client](#llm-client)
  - [Persona Management](#persona-management)
  - [Simulation Engine](#simulation-engine)
  - [Results Storage](#results-storage)
- [Advanced Features](#advanced-features)
  - [A/B Testing](#ab-testing)
  - [Longitudinal Studies](#longitudinal-studies)
  - [Batch Persona Generation](#batch-persona-generation)
- [Utilities](#utilities)
- [Complete Examples](#complete-examples)

---

## Core Modules

### LLM Client

#### Synchronous Client

```python
from src import LMStudioClient

# Initialize local client
client = LMStudioClient(
    base_url="http://127.0.0.1:1234/v1",
    model="local-model"
)

# Or initialize API client
client = LMStudioClient(
    base_url="https://api.deepseek.com/v1",
    api_key="your-api-key",
    model="deepseek-chat"
)

# Generate response
response = client.generate(
    prompt="Hello, please introduce yourself",
    temperature=0.7,
    max_tokens=300
)
print(response)

# Test connection
is_connected = client.test_connection()
print(f"Connection status: {is_connected}")

# Get available models
models = client.list_models()
print(f"Available models: {models}")
```

#### Async Client (Recommended for High Performance)

```python
import asyncio
from src import AsyncLLMClient

async def main():
    # Initialize async client
    client = AsyncLLMClient(
        base_url="https://api.deepseek.com/v1",
        api_key="your-api-key",
        model="deepseek-chat"
    )
    
    # Single request
    response = await client.generate_async(
        prompt="What is your age?",
        temperature=0.7
    )
    
    # Batch requests (parallel processing)
    prompts = ["Question 1", "Question 2", "Question 3"]
    responses = await client.generate_batch(
        prompts=prompts,
        temperature=0.7,
        max_concurrent=5  # Process 5 requests in parallel
    )
    
    for i, response in enumerate(responses):
        print(f"Response {i+1}: {response}")

asyncio.run(main())
```

**Performance Comparison**:
- Sync client: 100 personas × 10 questions = ~10-20 minutes
- Async client: 100 personas × 10 questions = ~2-3 minutes (with max_concurrent=10)

---

### Persona Management

#### Persona Class

```python
from src import Persona

# Create a persona
persona = Persona(
    name="John Smith",
    age=32,
    gender="Male",
    occupation="Software Engineer",
    background="Works at a tech company in Silicon Valley, often works overtime...",
    personality_traits=["Introverted", "Perfectionist", "Responsible"],
    values=["Career Development", "Work-Life Balance"],
    education="Bachelor's in Computer Science",
    location="San Francisco, CA"
)

# Convert to dictionary
persona_dict = persona.to_dict()

# Create from dictionary
persona_from_dict = Persona.from_dict(persona_dict)

# Generate prompt context
context = persona.to_prompt_context(use_json_format=True)
print(context)
```

#### PersonaManager Class

```python
from src import PersonaManager

# Initialize manager
manager = PersonaManager()

# Add personas
manager.add_persona(persona)

# Batch add
personas = [persona1, persona2, persona3]
for p in personas:
    manager.add_persona(p)

# Get all personas
all_personas = manager.get_all_personas()
print(f"Total: {len(all_personas)} personas")

# Get by ID
persona = manager.get_persona_by_id("persona_001")

# Save to file
manager.save_to_json("my_personas.json")

# Load from file
manager = PersonaManager.load_from_json("my_personas.json")
```

---

### Simulation Engine

#### Survey Mode

```python
from src import SimulationEngine, SurveyConfig

# Load survey configuration
survey = SurveyConfig.load_from_json("data/survey_configs/political_survey.json")

# Initialize simulation engine
engine = SimulationEngine(
    llm_client=client,
    survey_config=survey,
    simulation_mode="survey"
)

# Run simulation
results = engine.run_simulation(
    personas=personas,
    save_results=True,
    result_name="political_survey_wave1"
)

# Access results
for result in results:
    print(f"Persona: {result['persona_name']}")
    print(f"Responses: {result['responses']}")
```

#### Message Testing Mode

```python
# Initialize for message testing
engine = SimulationEngine(
    llm_client=client,
    simulation_mode="message"
)

# Test a single message
message = "Do you support environmental protection policies?"
response_format = {
    "type": "likert",
    "scale": 5,
    "labels": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
}

results = engine.test_message(
    message=message,
    personas=personas,
    response_format=response_format
)
```

#### A/B Testing Mode

```python
from src import ABTestEngine

# Initialize A/B test engine
ab_engine = ABTestEngine(llm_client=client)

# Define two message versions
version_a = "Do you agree with this policy?"
version_b = "To what extent do you support this policy?"

# Run A/B test
results = ab_engine.run_ab_test(
    version_a=version_a,
    version_b=version_b,
    personas=personas,
    split_ratio=0.5,  # 50/50 split
    response_format=response_format
)

# Get comparison statistics
comparison = ab_engine.compare_results(results)
print(f"Version A mean: {comparison['version_a_mean']}")
print(f"Version B mean: {comparison['version_b_mean']}")
print(f"P-value: {comparison['p_value']}")
```

---

### Results Storage

#### SimulationResults Class

```python
from src import SimulationResults

# Create results object
results = SimulationResults(
    simulation_id="sim_20250101_001",
    mode="survey",
    timestamp="2025-01-01 10:00:00",
    personas=personas,
    responses=response_data,
    metadata={
        "survey_name": "Political Orientation Survey",
        "total_questions": 15,
        "llm_model": "deepseek-chat"
    }
)

# Save results
results.save_to_json("data/results/political_survey_results.json")

# Load results
loaded_results = SimulationResults.load_from_json("data/results/political_survey_results.json")

# Export to CSV
results.export_to_csv("data/results/political_survey.csv")

# Get summary statistics
summary = results.get_summary()
print(summary)
```

#### ResultsManager Class

```python
from src import ResultsManager

# Initialize manager
rm = ResultsManager(results_dir="data/results")

# List all results
all_results = rm.list_results()
for result_file in all_results:
    print(result_file)

# Load specific result
result = rm.load_result("sim_20250101_001")

# Delete result
rm.delete_result("sim_20250101_001")

# Search results
survey_results = rm.search_results(mode="survey", keyword="political")
```

---

## Advanced Features

### A/B Testing

```python
from src import ABTestEngine, ABTestConfig

# Create A/B test configuration
config = ABTestConfig(
    test_name="Policy Wording Test",
    version_a={
        "message": "Do you agree with this policy?",
        "variant_name": "Direct Question"
    },
    version_b={
        "message": "To what extent do you support this policy?",
        "variant_name": "Extent Question"
    },
    response_format={
        "type": "likert",
        "scale": 5
    },
    split_ratio=0.5,
    sample_size=200
)

# Initialize engine
ab_engine = ABTestEngine(llm_client=client)

# Run test
results = ab_engine.run_test(
    config=config,
    personas=personas
)

# Analyze results
analysis = ab_engine.analyze_results(results)
print(f"Winner: {analysis['recommended_version']}")
print(f"Confidence: {analysis['confidence']}")
print(f"Effect size: {analysis['effect_size']}")
```

---

### Longitudinal Studies

```python
from src import LongitudinalStudyEngine, WaveConfig

# Create wave configurations
wave1_config = WaveConfig(
    wave_number=1,
    wave_name="Baseline",
    survey_config=baseline_survey,
    intervention=None
)

wave2_config = WaveConfig(
    wave_number=2,
    wave_name="Post-Intervention",
    survey_config=followup_survey,
    intervention={
        "type": "information",
        "content": "Recent studies show that climate change is accelerating...",
        "timing": "before_survey"
    }
)

# Initialize longitudinal engine
long_engine = LongitudinalStudyEngine(
    llm_client=client,
    study_name="Climate Opinion Change Study"
)

# Add waves
long_engine.add_wave(wave1_config)
long_engine.add_wave(wave2_config)

# Run all waves
results = long_engine.run_all_waves(
    personas=personas,
    track_memory=True  # Personas remember previous responses
)

# Analyze changes
changes = long_engine.analyze_changes(results)
print(f"Mean change: {changes['mean_change']}")
print(f"Positive changers: {changes['positive_change_pct']}%")
print(f"Negative changers: {changes['negative_change_pct']}%")

# Export longitudinal data
long_engine.export_longitudinal_data(
    output_file="climate_study_longitudinal.csv",
    format="wide"  # or "long"
)
```

#### Persona Memory System

```python
# In longitudinal studies, personas maintain conversation history
from src import PersonaConversationMemory

# Create memory for a persona
memory = PersonaConversationMemory(persona_id="persona_001")

# Add conversation turn
memory.add_turn(
    wave_number=1,
    question="What is your opinion on climate policy?",
    response="I support strong climate action..."
)

# Retrieve memory for Wave 2
context = memory.get_context_for_wave(wave_number=2)
# Context includes previous responses to maintain consistency
```

---

### Batch Persona Generation

```python
from src import PersonaGenerator

# Initialize generator
generator = PersonaGenerator(llm_client=client)

# Generate personas from criteria
criteria = {
    "demographics": {
        "age_range": [25, 65],
        "gender_distribution": {"Male": 0.48, "Female": 0.52},
        "education_levels": ["High School", "Bachelor's", "Master's", "PhD"],
        "locations": ["Urban", "Suburban", "Rural"]
    },
    "political_spectrum": {
        "distribution": "normal",
        "mean": 0,  # Center
        "std": 1.5
    },
    "sample_size": 300
}

# Generate
personas = generator.generate_batch(
    criteria=criteria,
    diversity=True  # Ensure diverse backgrounds
)

# Save personas
generator.save_personas(personas, "data/personas/generated_sample_300.json")

# Load personas
loaded_personas = PersonaGenerator.load_personas("data/personas/generated_sample_300.json")
```

---

## Utilities

### Survey Configuration Builder

```python
from src import SurveyConfigBuilder

# Build survey programmatically
builder = SurveyConfigBuilder(survey_name="Customer Satisfaction Survey")

# Add questions
builder.add_likert_question(
    question_id="q1",
    text="How satisfied are you with our product?",
    scale=5
)

builder.add_multiple_choice_question(
    question_id="q2",
    text="Which feature do you use most?",
    options=["Feature A", "Feature B", "Feature C", "Other"]
)

builder.add_open_ended_question(
    question_id="q3",
    text="What improvements would you suggest?"
)

# Build and save
survey_config = builder.build()
survey_config.save_to_json("data/survey_configs/customer_satisfaction.json")
```

### Response Scoring

```python
from src import ResponseScorer, ScoringRule

# Define scoring rules
rules = [
    ScoringRule(
        question_id="q1",
        scoring_type="likert",
        mapping={1: -2, 2: -1, 3: 0, 4: 1, 5: 2}
    ),
    ScoringRule(
        question_id="q2",
        scoring_type="categorical",
        mapping={"Option A": 1, "Option B": 0, "Option C": 1}
    )
]

# Initialize scorer
scorer = ResponseScorer(rules=rules)

# Score responses
persona_responses = {
    "q1": 5,
    "q2": "Option A"
}

total_score = scorer.score_responses(persona_responses)
print(f"Total score: {total_score}")
```

### Data Export

```python
from src import DataExporter

# Initialize exporter
exporter = DataExporter(results=simulation_results)

# Export to different formats
exporter.to_csv("results.csv", format="wide")
exporter.to_json("results.json", indent=2)
exporter.to_excel("results.xlsx", include_summary=True)

# Export for specific analysis tools
exporter.to_spss("results.sav")
exporter.to_stata("results.dta")
exporter.to_r("results.rds")
```

---

## Complete Examples

### Example 1: Complete Survey Workflow

```python
import asyncio
from src import AsyncLLMClient, PersonaManager, SimulationEngine, SurveyConfig

async def run_survey_simulation():
    # 1. Initialize LLM client
    client = AsyncLLMClient(
        base_url="https://api.deepseek.com/v1",
        api_key="your-api-key",
        model="deepseek-chat"
    )
    
    # 2. Load personas
    persona_manager = PersonaManager.load_from_json("data/personas/diverse_sample_200.json")
    personas = persona_manager.get_all_personas()
    
    # 3. Load survey configuration
    survey = SurveyConfig.load_from_json("data/survey_configs/political_survey.json")
    
    # 4. Initialize simulation engine
    engine = SimulationEngine(
        llm_client=client,
        survey_config=survey,
        simulation_mode="survey"
    )
    
    # 5. Run simulation
    results = await engine.run_simulation_async(
        personas=personas,
        save_results=True,
        result_name="political_survey_2025"
    )
    
    # 6. Export results
    results.export_to_csv("political_survey_results.csv")
    
    print(f"✅ Simulation complete! {len(results)} responses collected.")
    
    return results

# Run
asyncio.run(run_survey_simulation())
```

### Example 2: Longitudinal Intervention Study

```python
from src import LongitudinalStudyEngine, WaveConfig, SurveyConfig, InterventionConfig

# Define baseline survey
baseline_survey = SurveyConfig.load_from_json("data/survey_configs/baseline_attitudes.json")

# Define intervention
intervention = InterventionConfig(
    intervention_type="information_exposure",
    content="Recent scientific evidence shows that renewable energy is now cheaper than fossil fuels...",
    timing="between_waves"
)

# Define follow-up survey
followup_survey = SurveyConfig.load_from_json("data/survey_configs/followup_attitudes.json")

# Create wave configurations
waves = [
    WaveConfig(wave_number=1, survey=baseline_survey, intervention=None),
    WaveConfig(wave_number=2, survey=followup_survey, intervention=intervention)
]

# Initialize longitudinal engine
long_engine = LongitudinalStudyEngine(
    llm_client=client,
    study_name="Energy Attitude Intervention Study",
    waves=waves
)

# Run study
results = long_engine.run_study(
    personas=personas,
    track_memory=True
)

# Analyze intervention effect
effect = long_engine.calculate_intervention_effect(results)
print(f"Average attitude change: {effect['mean_change']}")
print(f"Effect size (Cohen's d): {effect['effect_size']}")
print(f"Statistical significance: p = {effect['p_value']}")
```

### Example 3: A/B Test with Statistical Analysis

```python
from src import ABTestEngine, StatisticalTest

# Define test
ab_engine = ABTestEngine(llm_client=client)

version_a = "How much do you agree with this statement?"
version_b = "To what extent do you support this statement?"

# Run A/B test
results = ab_engine.run_ab_test(
    version_a=version_a,
    version_b=version_b,
    personas=personas,
    split_ratio=0.5,
    response_format={"type": "likert", "scale": 5}
)

# Statistical analysis
stats = StatisticalTest.compare_groups(
    group_a=results['version_a_responses'],
    group_b=results['version_b_responses'],
    test_type="t-test"
)

print(f"Version A mean: {stats['group_a_mean']:.2f}")
print(f"Version B mean: {stats['group_b_mean']:.2f}")
print(f"Difference: {stats['difference']:.2f}")
print(f"P-value: {stats['p_value']:.4f}")
print(f"Significant: {stats['significant']}")
print(f"Recommended version: {'A' if stats['group_a_mean'] > stats['group_b_mean'] else 'B'}")
```

---

## Best Practices

### Performance Optimization

1. **Use Async Client for Large Simulations**
   ```python
   # Instead of sync
   client = LMStudioClient(...)
   
   # Use async
   client = AsyncLLMClient(...)
   results = await engine.run_simulation_async(...)
   ```

2. **Batch Requests**
   ```python
   # Process in batches of 10
   results = await client.generate_batch(prompts, max_concurrent=10)
   ```

3. **Cache Results**
   ```python
   # Enable caching to avoid re-processing
   engine = SimulationEngine(client, cache_enabled=True)
   ```

### Error Handling

```python
from src import SimulationError, LLMConnectionError

try:
    results = engine.run_simulation(personas)
except LLMConnectionError as e:
    print(f"Connection failed: {e}")
    # Retry logic
except SimulationError as e:
    print(f"Simulation error: {e}")
    # Save partial results
```

### Data Validation

```python
from src import PersonaValidator, SurveyValidator

# Validate personas before simulation
validator = PersonaValidator()
for persona in personas:
    if not validator.validate(persona):
        print(f"Invalid persona: {persona.name}")

# Validate survey configuration
survey_validator = SurveyValidator()
if not survey_validator.validate(survey_config):
    print(f"Invalid survey configuration")
```

---

## API Changelog

### Current Version (v2.0)

**Added**:
- ✅ Async LLM client for parallel processing
- ✅ Longitudinal study support with persona memory
- ✅ A/B testing engine
- ✅ Batch persona generation

**Removed**:
- ❌ StatisticalAnalyzer (no UI)
- ❌ ScriptGenerator (no UI)
- ❌ SensitivityAnalyzer (no UI)
- ❌ ProjectManager (no UI)
- ❌ ResponseValidator (no UI)
- ❌ SimulationEstimator (no UI)

**Changed**:
- 🔄 SimulationEngine now supports three modes: Survey, Message, A/B Testing
- 🔄 Results storage format updated for longitudinal data
- 🔄 PersonaManager now supports batch operations

---

## Additional Resources

- **[Architecture Guide](../architecture/README.md)** - Understand system design
- **[Longitudinal Study Guide](../longitudinal/README.md)** - Detailed guide for multi-wave studies
- **[Code Examples](../examples/)** - More practical examples
- **[Contributing Guide](../contributing/README.md)** - Contribute to the API

---

**API Version:** 2.0.0  
**Last Updated:** 2025-01  
**Status:** Stable
