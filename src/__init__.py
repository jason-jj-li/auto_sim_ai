"""LLM Simulation Survey System - Core modules."""
from .llm_client import LMStudioClient, AsyncLLMClient
from .persona import Persona, PersonaManager
from .simulation import SimulationEngine, SimulationResult, ParallelSimulationEngine
from .storage import ResultsStorage
from .tools import ToolRegistry, get_default_tool_registry
from .logging_config import setup_logging, get_logger
from .validators import InputValidator, ValidationError
from .connection_manager import ConnectionManager
from .ui_components import render_navigation, render_connection_status, render_page_header, render_system_status_badge
from .survey_templates import (
    QuestionMetadata,
    SurveySection,
    SurveyTemplate,
    SurveyTemplateLibrary
)
from .survey_config import SurveyConfig, SurveyConfigManager
from .scoring import SurveyScorer
from .cache import ResponseCache
from .checkpoint import Checkpoint, CheckpointManager
from .validation import ResponseValidator, ConsistencyChecker, ConsistencyMetrics
from .analysis import StatisticalAnalyzer, StatisticalResult
from .export import ScriptGenerator
from .estimation import SimulationEstimator, SimulationEstimate
from .persona_generator import PersonaGenerator, DistributionConfig
from .ab_testing import ABTestManager, Condition, ABTestConfig
from .sensitivity import SensitivityAnalyzer
from .project import ProjectManager
from .intervention_study import (
    InterventionWave,
    InterventionStudyConfig,
    InterventionStudyBuilder,
    InterventionStudyManager
)
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
    'ToolRegistry',
    'get_default_tool_registry',
    # Utilities
    'setup_logging',
    'get_logger',
    'InputValidator',
    'ValidationError',
    'ConnectionManager',
    'render_navigation',
    'render_connection_status',
    'render_page_header',
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
    'Checkpoint',
    'CheckpointManager',
    # Validation
    'ResponseValidator',
    'ConsistencyChecker',
    'ConsistencyMetrics',
    # Analysis
    'StatisticalAnalyzer',
    'StatisticalResult',
    'ScriptGenerator',
    'SimulationEstimator',
    'SimulationEstimate',
    # Research Features
    'PersonaGenerator',
    'DistributionConfig',
    'ABTestManager',
    'Condition',
    'ABTestConfig',
    'SensitivityAnalyzer',
    'ProjectManager',
    # Intervention Studies (Old)
    'InterventionWave',
    'InterventionStudyConfig',
    'InterventionStudyBuilder',
    'InterventionStudyManager',
    # Longitudinal Studies (New - with conversation memory)
    'ConversationHistory',
    'WaveConfig',
    'LongitudinalStudyConfig',
    'WaveResult',
    'LongitudinalStudyResult',
    'LongitudinalStudyEngine',
    'LongitudinalStudyBuilder'
]

