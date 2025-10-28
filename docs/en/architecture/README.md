# System Architecture

Auto Sim AI system architecture and design documentation.

## Overview

**Modular, Async-First** architecture supporting survey simulation, A/B testing, and longitudinal studies.

## Core Modules (20 Total)

All modules have complete UI coverage through Streamlit.

### Infrastructure Layer
- `llm_client.py` - LLM API communication (sync/async)
- `connection_manager.py` - Connection pooling
- `cache.py` - Response caching
- `storage.py` - Data persistence

### Domain Layer
- `persona.py` - Virtual respondent profiles
- `survey_config.py` - Survey configuration
- `survey_templates.py` - Reusable templates
- `scoring.py` - Response scoring

### Application Layer
- `simulation.py` - Core simulation engine
- `longitudinal_study.py` - Multi-wave studies with memory
- `ab_testing.py` - A/B testing engine
- `persona_generator.py` - Batch persona generation
- `checkpoint.py` - Progress saving/resuming

### Presentation Layer
- `ui_components.py` - Reusable UI components
- `styles.py` - UI styling
- `validators.py` - Input validation

## Technology Stack

- **Python 3.8+** - Core language
- **Streamlit 1.32** - Web UI
- **asyncio** - Async programming
- **Pandas/NumPy** - Data processing
- **OpenAI SDK** - LLM APIs

## Performance

- **Async mode**: 5-10x faster than sync
- **Throughput**: 30-50 personas/minute
- **Caching**: Instant for repeated prompts
- **Checkpoints**: Resume after failures

## Data Flow

```
User Input → Load Config + Personas → Process (Async) → Aggregate → Save → Display/Export
```

See [API Reference](../api/README.md) for detailed module documentation.

**Version**: 2.0 | **Status**: Stable
