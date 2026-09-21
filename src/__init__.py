"""LLM Simulation Survey System - Core modules."""
from .llm_client import LMStudioClient, AsyncLLMClient
from .persona import Persona, PersonaManager, personas_from_dataframe
from .simulation import SimulationEngine, SimulationResult, ParallelSimulationEngine
from .storage import ResultsStorage, results_to_wide
from .logging_config import setup_logging, get_logger
from .validators import InputValidator, ValidationError
from .ui_components import (
    render_navigation, render_page_header, section, stat_cards,
    render_stepper, render_empty_state, workflow_strip, feature_grid,
)
from .survey_templates import (
    QuestionMetadata,
    SurveySection,
    SurveyTemplate,
    SurveyTemplateLibrary
)
from .survey_config import SurveyConfig, SurveyConfigManager
from .scoring import SurveyScorer
from .cache import ResponseCache
from .model_connection_ui import render_model_connection
from .persona_generator import PersonaGenerator, DistributionConfig
from .ab_testing import ABTestManager, Condition, ABTestConfig, run_ab_test
from .reliability import cronbach_alpha, question_collapse_report, test_retest, distribution_divergence
from .longitudinal_study import (
    ConversationHistory,
    WaveConfig,
    LongitudinalStudyConfig,
    WaveResult,
    LongitudinalStudyResult,
    LongitudinalStudyEngine,
    LongitudinalStudyBuilder
)

__all__ = [
    # Core
    'LMStudioClient',
    'AsyncLLMClient',
    'Persona',
    'PersonaManager',
    'SimulationEngine',
    'SimulationResult',
    'ParallelSimulationEngine',
    'ResultsStorage',
    'results_to_wide',
    # Utilities
    'setup_logging',
    'get_logger',
    'InputValidator',
    'ValidationError',
    'render_navigation',
    'render_page_header',
    'section',
    'stat_cards',
    'render_stepper',
    'render_empty_state',
    'workflow_strip',
    'feature_grid',
    # Survey System
    'QuestionMetadata',
    'SurveySection',
    'SurveyTemplate',
    'SurveyTemplateLibrary',
    'SurveyConfig',
    'SurveyConfigManager',
    'SurveyScorer',
    # Performance
    'ResponseCache',
    'render_model_connection',
    # Research Features
    'PersonaGenerator',
    'DistributionConfig',
    'ABTestManager',
    'Condition',
    'ABTestConfig',
    'run_ab_test',
    # Reliability & Validity
    'cronbach_alpha',
    'question_collapse_report',
    'test_retest',
    'distribution_divergence',
    # Longitudinal Studies (with conversation memory)
    'ConversationHistory',
    'WaveConfig',
    'LongitudinalStudyConfig',
    'WaveResult',
    'LongitudinalStudyResult',
    'LongitudinalStudyEngine',
    'LongitudinalStudyBuilder'
]
