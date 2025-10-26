"""A/B testing framework for intervention comparisons."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import random
from scipy import stats
import numpy as np


@dataclass
class Condition:
    """Represents an experimental condition."""
    condition_id: str
    condition_name: str
    intervention_text: str
    allocation_weight: float = 1.0


@dataclass
class ABTestConfig:
    """Configuration for A/B test."""
    test_name: str
    conditions: List[Condition]
    questions: List[str]
    random_assignment: bool = True
    stratify_by: Optional[str] = None


class ABTestManager:
    """Manages A/B testing experiments."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize A/B test manager."""
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        self.assignments: Dict[str, str] = {}  # persona_id -> condition_id
    
    def assign_personas(
        self,
        personas: List[Any],
        conditions: List[Condition],
        stratify_by: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Randomly assign personas to conditions.
        
        Args:
            personas: List of Persona objects
            conditions: List of Condition objects
            stratify_by: Optional attribute to stratify by (e.g., 'gender')
            
        Returns:
            Dictionary mapping persona names to condition IDs
        """
        assignments = {}
        
        if stratify_by:
            # Stratified assignment
            strata = {}
            for persona in personas:
                stratum_value = getattr(persona, stratify_by, None)
                if stratum_value not in strata:
                    strata[stratum_value] = []
                strata[stratum_value].append(persona)
            
            # Assign within each stratum
            for stratum_value, stratum_personas in strata.items():
                stratum_assignments = self._random_assignment(
                    stratum_personas, conditions
                )
                assignments.update(stratum_assignments)
        else:
            # Simple random assignment
            assignments = self._random_assignment(personas, conditions)
        
        self.assignments = assignments
        return assignments
    
    def _random_assignment(
        self,
        personas: List[Any],
        conditions: List[Condition]
    ) -> Dict[str, str]:
        """Perform random assignment."""
        assignments = {}
        
        # Calculate weights
        total_weight = sum(c.allocation_weight for c in conditions)
        probabilities = [c.allocation_weight / total_weight for c in conditions]
        condition_ids = [c.condition_id for c in conditions]
        
        # Assign each persona
        for persona in personas:
            condition_id = np.random.choice(condition_ids, p=probabilities)
            assignments[persona.name] = condition_id
        
        return assignments
    
    def compare_conditions(
        self,
        results_by_condition: Dict[str, List[float]],
        test_type: str = 'anova'
    ) -> Dict[str, Any]:
        """
        Compare outcomes across conditions.
        
        Args:
            results_by_condition: Dict mapping condition_id to list of numeric outcomes
            test_type: 'anova' for >2 conditions, 't_test' for 2 conditions
            
        Returns:
            Statistical comparison results
        """
        condition_ids = list(results_by_condition.keys())
        
        if len(condition_ids) < 2:
            return {'error': 'Need at least 2 conditions'}
        
        if test_type == 't_test' or len(condition_ids) == 2:
            # Independent t-test
            data1 = results_by_condition[condition_ids[0]]
            data2 = results_by_condition[condition_ids[1]]
            
            t_stat, p_value = stats.ttest_ind(data1, data2)
            
            # Cohen's d
            pooled_std = np.sqrt(
                ((len(data1) - 1) * np.std(data1, ddof=1) ** 2 +
                 (len(data2) - 1) * np.std(data2, ddof=1) ** 2) /
                (len(data1) + len(data2) - 2)
            )
            cohens_d = (np.mean(data1) - np.mean(data2)) / pooled_std if pooled_std > 0 else 0
            
            return {
                'test': 't-test',
                'statistic': float(t_stat),
                'p_value': float(p_value),
                'effect_size': float(cohens_d),
                'significant': p_value < 0.05,
                'means': {cid: float(np.mean(results_by_condition[cid])) for cid in condition_ids}
            }
        else:
            # One-way ANOVA
            data_groups = [results_by_condition[cid] for cid in condition_ids]
            f_stat, p_value = stats.f_oneway(*data_groups)
            
            # Eta-squared
            grand_mean = np.mean([v for vals in data_groups for v in vals])
            ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in data_groups)
            ss_total = sum((v - grand_mean) ** 2 for vals in data_groups for v in vals)
            eta_squared = ss_between / ss_total if ss_total > 0 else 0
            
            return {
                'test': 'ANOVA',
                'statistic': float(f_stat),
                'p_value': float(p_value),
                'effect_size': float(eta_squared),
                'significant': p_value < 0.05,
                'means': {cid: float(np.mean(results_by_condition[cid])) for cid in condition_ids}
            }
    
    def power_analysis(
        self,
        effect_size: float,
        alpha: float = 0.05,
        power: float = 0.80,
        n_conditions: int = 2
    ) -> int:
        """
        Calculate required sample size for desired power.
        
        Args:
            effect_size: Expected effect size (Cohen's d or eta-squared)
            alpha: Significance level
            power: Desired statistical power
            n_conditions: Number of conditions
            
        Returns:
            Required sample size per condition
        """
        # Simplified power calculation
        # For more accurate results, use statsmodels.stats.power
        
        if n_conditions == 2:
            # t-test power
            # Using simplified formula
            from scipy.stats import norm
            z_alpha = norm.ppf(1 - alpha/2)
            z_beta = norm.ppf(power)
            n_per_group = ((z_alpha + z_beta) / effect_size) ** 2 * 2
        else:
            # ANOVA power (rough estimate)
            from scipy.stats import f as f_dist
            # Simplified: assume equal group sizes
            f_crit = f_dist.ppf(1 - alpha, n_conditions - 1, 100)
            ncp = effect_size * n_conditions * 30  # Non-centrality parameter estimate
            n_per_group = int(ncp / effect_size)
        
        return max(int(np.ceil(n_per_group)), 10)  # Minimum 10 per group
