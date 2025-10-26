"""
Longitudinal Intervention Study Module

Implements repeated-measures intervention studies with pre/post design.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json


@dataclass
class InterventionWave:
    """Represents a single wave/timepoint in the intervention study."""
    wave_number: int
    wave_label: str  # "Baseline", "Follow-up 1", etc.
    days_from_baseline: int  # Time elapsed since baseline
    is_intervention_wave: bool = False  # Does intervention happen at this wave?
    intervention_text: Optional[str] = None  # Intervention content (if applicable)
    questions: List[str] = field(default_factory=list)  # Questions for this wave
    context_update: Optional[str] = None  # Context to add for this wave


@dataclass
class InterventionStudyConfig:
    """Configuration for a longitudinal intervention study."""
    study_name: str
    waves: List[InterventionWave]
    baseline_questions: List[str]  # Questions asked at all waves
    intervention_wave_number: int  # Which wave has the intervention (e.g., wave 3)
    intervention_text: str  # The intervention content
    follow_up_period_days: int  # Days between waves
    total_waves: int  # Total number of waves (e.g., 10)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "study_name": self.study_name,
            "waves": [
                {
                    "wave_number": w.wave_number,
                    "wave_label": w.wave_label,
                    "days_from_baseline": w.days_from_baseline,
                    "is_intervention_wave": w.is_intervention_wave,
                    "intervention_text": w.intervention_text,
                    "questions": w.questions,
                    "context_update": w.context_update
                }
                for w in self.waves
            ],
            "baseline_questions": self.baseline_questions,
            "intervention_wave_number": self.intervention_wave_number,
            "intervention_text": self.intervention_text,
            "follow_up_period_days": self.follow_up_period_days,
            "total_waves": self.total_waves
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InterventionStudyConfig':
        """Create from dictionary."""
        waves = [
            InterventionWave(
                wave_number=w["wave_number"],
                wave_label=w["wave_label"],
                days_from_baseline=w["days_from_baseline"],
                is_intervention_wave=w.get("is_intervention_wave", False),
                intervention_text=w.get("intervention_text"),
                questions=w.get("questions", []),
                context_update=w.get("context_update")
            )
            for w in data["waves"]
        ]
        
        return cls(
            study_name=data["study_name"],
            waves=waves,
            baseline_questions=data["baseline_questions"],
            intervention_wave_number=data["intervention_wave_number"],
            intervention_text=data["intervention_text"],
            follow_up_period_days=data["follow_up_period_days"],
            total_waves=data["total_waves"]
        )


class InterventionStudyBuilder:
    """Helper class to build intervention study configurations."""
    
    @staticmethod
    def create_pre_post_intervention_study(
        study_name: str,
        baseline_questions: List[str],
        intervention_text: str,
        total_waves: int = 10,
        follow_up_period_days: int = 7,
        intervention_wave_number: int = 5,
        intervention_questions: Optional[List[str]] = None
    ) -> InterventionStudyConfig:
        """
        Create a standard pre-post intervention study.
        
        Args:
            study_name: Name of the study
            baseline_questions: Questions repeated at each wave
            intervention_text: The intervention content
            total_waves: Total number of waves (default: 10)
            follow_up_period_days: Days between each wave (default: 7)
            intervention_wave_number: Which wave has intervention (default: 5, mid-point)
            intervention_questions: Additional questions only at intervention wave
        
        Returns:
            InterventionStudyConfig object
        """
        waves = []
        
        for i in range(1, total_waves + 1):
            # Determine wave label
            if i == 1:
                label = "Baseline"
            elif i < intervention_wave_number:
                label = f"Pre-intervention {i-1}"
            elif i == intervention_wave_number:
                label = "Intervention"
            else:
                label = f"Follow-up {i - intervention_wave_number}"
            
            # Calculate days from baseline
            days_from_baseline = (i - 1) * follow_up_period_days
            
            # Is this the intervention wave?
            is_intervention = (i == intervention_wave_number)
            
            # Questions for this wave
            wave_questions = baseline_questions.copy()
            if is_intervention and intervention_questions:
                wave_questions.extend(intervention_questions)
            
            # Context update for time progression
            if i == 1:
                context_update = "You are being surveyed for the first time as part of a longitudinal study."
            elif i < intervention_wave_number:
                context_update = f"It has been {days_from_baseline} days since the baseline survey. Please answer based on your current feelings and experiences."
            elif i == intervention_wave_number:
                context_update = f"It has been {days_from_baseline} days since the baseline survey. You will now be presented with important information."
            else:
                days_since_intervention = (i - intervention_wave_number) * follow_up_period_days
                context_update = f"It has been {days_since_intervention} days since the intervention. Please answer based on your current feelings and experiences, considering what you learned during the intervention."
            
            wave = InterventionWave(
                wave_number=i,
                wave_label=label,
                days_from_baseline=days_from_baseline,
                is_intervention_wave=is_intervention,
                intervention_text=intervention_text if is_intervention else None,
                questions=wave_questions,
                context_update=context_update
            )
            
            waves.append(wave)
        
        return InterventionStudyConfig(
            study_name=study_name,
            waves=waves,
            baseline_questions=baseline_questions,
            intervention_wave_number=intervention_wave_number,
            intervention_text=intervention_text,
            follow_up_period_days=follow_up_period_days,
            total_waves=total_waves
        )
    
    @staticmethod
    def create_multiple_intervention_study(
        study_name: str,
        baseline_questions: List[str],
        interventions: List[Dict[str, Any]],  # [{"wave": 3, "text": "...", "questions": [...]}, ...]
        total_waves: int = 10,
        follow_up_period_days: int = 7
    ) -> InterventionStudyConfig:
        """
        Create a study with multiple intervention points.
        
        Args:
            study_name: Name of the study
            baseline_questions: Questions repeated at each wave
            interventions: List of intervention dicts with "wave", "text", "questions"
            total_waves: Total number of waves
            follow_up_period_days: Days between waves
        
        Returns:
            InterventionStudyConfig object
        """
        intervention_waves = {i["wave"]: i for i in interventions}
        waves = []
        
        for i in range(1, total_waves + 1):
            # Determine wave label
            if i == 1:
                label = "Baseline"
            elif i in intervention_waves:
                label = f"Intervention {list(intervention_waves.keys()).index(i) + 1}"
            else:
                label = f"Wave {i}"
            
            days_from_baseline = (i - 1) * follow_up_period_days
            is_intervention = i in intervention_waves
            
            wave_questions = baseline_questions.copy()
            intervention_text_for_wave = None
            
            if is_intervention:
                intervention_text_for_wave = intervention_waves[i]["text"]
                if "questions" in intervention_waves[i]:
                    wave_questions.extend(intervention_waves[i]["questions"])
            
            # Context update
            context_update = f"It has been {days_from_baseline} days since the baseline survey. "
            if is_intervention:
                context_update += "You will now be presented with important information."
            else:
                context_update += "Please answer based on your current feelings and experiences."
            
            wave = InterventionWave(
                wave_number=i,
                wave_label=label,
                days_from_baseline=days_from_baseline,
                is_intervention_wave=is_intervention,
                intervention_text=intervention_text_for_wave,
                questions=wave_questions,
                context_update=context_update
            )
            
            waves.append(wave)
        
        # Use first intervention as primary
        primary_intervention = interventions[0] if interventions else {"wave": 5, "text": ""}
        
        return InterventionStudyConfig(
            study_name=study_name,
            waves=waves,
            baseline_questions=baseline_questions,
            intervention_wave_number=primary_intervention["wave"],
            intervention_text=primary_intervention["text"],
            follow_up_period_days=follow_up_period_days,
            total_waves=total_waves
        )


class InterventionStudyManager:
    """Manages intervention study configurations."""
    
    def __init__(self, storage_dir: str = "data/intervention_studies"):
        """Initialize manager with storage directory."""
        self.storage_dir = storage_dir
        import os
        os.makedirs(storage_dir, exist_ok=True)
    
    def save_config(self, config: InterventionStudyConfig) -> str:
        """Save intervention study configuration."""
        import os
        filename = f"{config.study_name.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)
        
        return filepath
    
    def load_config(self, study_name: str) -> Optional[InterventionStudyConfig]:
        """Load intervention study configuration."""
        import os
        filename = f"{study_name.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return InterventionStudyConfig.from_dict(data)
    
    def list_studies(self) -> List[str]:
        """List all saved intervention studies."""
        import os
        if not os.path.exists(self.storage_dir):
            return []
        
        studies = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                study_name = filename.replace('.json', '').replace('_', ' ').title()
                studies.append(study_name)
        
        return studies
    
    def delete_config(self, study_name: str) -> bool:
        """Delete intervention study configuration."""
        import os
        filename = f"{study_name.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

