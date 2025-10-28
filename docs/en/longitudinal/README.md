# Longitudinal Study Guide

Guide for conducting multi-wave longitudinal studies with Auto Sim AI.

## Overview

Auto Sim AI supports longitudinal studies with **conversation memory** - personas remember previous responses across waves.

## Key Features

✅ **Conversation Memory** - Personas remember all previous interactions  
✅ **Time Awareness** - Simulate time passage between waves  
✅ **Context Coherence** - Realistic, consistent responses  
✅ **Checkpoint Saving** - Auto-save after each wave  
✅ **History Tracking** - Complete conversation logs

## How It Works

### Multi-Turn Conversation Mechanism

Each persona maintains a complete conversation history across waves:

```
Wave 1 (Baseline):
User: "Rate your stress level (1-10)"
Persona: "7 - Very busy at work lately"

Wave 2 (7 days later):
User: "It's been 7 days. How is your stress now?"
Persona: "6 - Still busy but slightly better"
         (Remembers the previous "7" response)

Wave 3 (After intervention):
User: "After trying meditation, what's your stress level?"
Persona: "4 - Meditation helped significantly"
         (Remembers both previous responses + intervention)
```

## Quick Start

### 1. Import Modules

```python
from src import (
    LMStudioClient,
    PersonaManager,
    LongitudinalStudyEngine,
    LongitudinalStudyBuilder
)
```

### 2. Create Study Design

```python
# Create pre-post intervention study
study_config = LongitudinalStudyBuilder.create_pre_post_study(
    study_name="Meditation Intervention Study",
    
    # Baseline questions (asked in all waves)
    baseline_questions=[
        "Rate your stress level (1-10)",
        "How is your sleep quality?",
        "How is your overall well-being?"
    ],
    
    # Intervention content
    intervention_text="""
Research shows that 10 minutes of daily mindfulness meditation can:
• Reduce stress by 30%
• Improve sleep quality by 50%
• Enhance overall well-being

Try meditating daily for the next 30 days using apps like Calm or Headspace.
    """,
    
    # Follow-up questions (after intervention)
    followup_questions=[
        "Rate your stress level (1-10)",
        "How is your sleep quality?",
        "How is your overall well-being?",
        "Did you try meditation?",
        "If yes, what changes did you notice?"
    ],
    
    # Study parameters
    num_pre_waves=3,       # 3 baseline waves
    num_post_waves=5,      # 5 follow-up waves
    days_between_waves=7   # Weekly measurements
)

print(f"Study design: {len(study_config.waves)} waves")
for wave in study_config.waves:
    print(f"  Wave {wave.wave_number}: {wave.wave_name} (Day {wave.days_from_baseline})")
```

### 3. Prepare Personas

```python
# Load personas
persona_manager = PersonaManager()
persona_manager.load_from_file("data/personas/my_personas.json")
personas = persona_manager.get_all_personas()[:50]
```

### 4. Run Study

```python
# Initialize LLM client
client = LMStudioClient(
    base_url="https://api.deepseek.com/v1",
    api_key="your-api-key"
)

# Create longitudinal engine
engine = LongitudinalStudyEngine(
    llm_client=client,
    storage_dir="data/longitudinal_studies"
)

# Progress callback
def on_progress(message):
    print(f"📊 {message}")

# Run complete study
result = engine.run_study(
    config=study_config,
    personas=personas,
    temperature=0.7,
    max_tokens=300,
    progress_callback=on_progress,
    save_checkpoints=True
)

print(f"\n✅ Study complete!")
print(f"Study ID: {result.study_id}")
print(f"Participants: {len(result.persona_results)}")
print(f"Total waves: {len(study_config.waves)}")
```

## Study Design Patterns

### 1. Pre-Post Intervention

```python
study = LongitudinalStudyBuilder.create_pre_post_study(
    baseline_questions=[...],
    intervention_text="...",
    followup_questions=[...],
    num_pre_waves=2,
    num_post_waves=3
)
```

**Use cases**: Treatment effects, intervention studies, behavior change

### 2. Panel Survey

```python
study = LongitudinalStudyBuilder.create_panel_study(
    questions=[...],
    num_waves=5,
    days_between_waves=30
)
```

**Use cases**: Opinion tracking, trend analysis, cohort studies

### 3. Custom Design

```python
from src import WaveConfig

waves = [
    WaveConfig(wave_number=1, questions=[...], intervention=None),
    WaveConfig(wave_number=2, questions=[...], intervention="Treatment A"),
    WaveConfig(wave_number=3, questions=[...], intervention=None)
]

study = LongitudinalStudyConfig(waves=waves)
```

## Analyzing Results

### Load Study Results

```python
# Load saved study
result = engine.load_study(study_id="study_20250128_001")

# Access wave results
for wave_num, wave_result in result.wave_results.items():
    print(f"Wave {wave_num}: {len(wave_result.responses)} responses")
```

### Analyze Changes

```python
# Calculate within-person changes
changes = engine.analyze_changes(
    result,
    baseline_wave=1,
    followup_wave=5,
    outcome_question="stress_level"
)

print(f"Mean change: {changes['mean_change']:.2f}")
print(f"Improved: {changes['improved_pct']:.1f}%")
print(f"Worsened: {changes['worsened_pct']:.1f}%")
print(f"No change: {changes['no_change_pct']:.1f}%")
```

### Export for Statistical Analysis

```python
# Export to wide format (one row per person)
engine.export_to_csv(
    result,
    output_file="longitudinal_data_wide.csv",
    format="wide"
)

# Export to long format (one row per person-wave)
engine.export_to_csv(
    result,
    output_file="longitudinal_data_long.csv",
    format="long"
)
```

## Statistical Analysis Examples

### In R

```r
# Load data
library(lme4)
data <- read.csv("longitudinal_data_long.csv")

# Mixed effects model
model <- lmer(stress_level ~ wave + intervention + (1|persona_id), data=data)
summary(model)

# Plot trajectories
library(ggplot2)
ggplot(data, aes(x=wave, y=stress_level, group=persona_id)) +
  geom_line(alpha=0.3) +
  stat_summary(aes(group=1), fun=mean, geom="line", size=2, color="red")
```

### In Python

```python
import pandas as pd
import statsmodels.formula.api as smf

# Load data
df = pd.read_csv("longitudinal_data_long.csv")

# Mixed effects model
model = smf.mixedlm("stress_level ~ wave + intervention", df, groups=df["persona_id"])
result = model.fit()
print(result.summary())
```

## Best Practices

### Persona Design

- Use realistic, diverse personas
- Include relevant background details
- Define clear baseline attitudes

### Wave Timing

- Allow sufficient time between waves (e.g., 7-30 days)
- Consider intervention duration
- Plan for realistic follow-up periods

### Intervention Design

- Clear, specific intervention content
- Appropriate length and detail
- Realistic implementation scenarios

### Sample Size

- **Pilot testing**: 20-30 personas
- **Small studies**: 50-100 personas
- **Full studies**: 150-300 personas
- Account for attrition in real studies

## Troubleshooting

### Memory Issues

If personas don't seem to remember previous responses:

```python
# Check conversation history
history = engine.get_conversation_history(persona_id, study_id)
print(history)

# Verify memory is enabled
engine = LongitudinalStudyEngine(
    llm_client=client,
    enable_memory=True  # Make sure this is True
)
```

### Consistency Issues

For more consistent responses across waves:

```python
# Use lower temperature
engine.run_study(
    config=study_config,
    personas=personas,
    temperature=0.5  # Lower = more consistent
)
```

## Example Use Cases

### 1. Opinion Change Study

Track how exposure to information changes opinions over time.

### 2. Intervention Effectiveness

Test whether an intervention (e.g., educational content) changes behavior or attitudes.

### 3. Panel Survey

Repeatedly measure the same constructs to track trends.

### 4. Within-Person Experiments

Compare individual change patterns rather than group averages.

---

**Related Documentation**:
- [API Reference](../api/README.md) - Detailed API docs
- [Quick Start](../quickstart/README.md) - Get started
- [Examples](../examples/) - Code examples

**Version**: 2.0 | **Last Updated**: 2025-01
