"""A/B testing framework for intervention comparisons."""
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from scipy import stats
import numpy as np


def run_ab_test(
    run_survey_fn: Callable,
    personas: List[Any],
    conditions: List['Condition'],
    assignments: Dict[str, str],
    questions: List[str],
    **kwargs
):
    """Run the survey once per condition group and merge into one tagged result.

    The condition's intervention_text becomes the survey_context, so each persona
    actually answers under its assigned condition. Works with both engines:
    pass SimulationEngine.run_survey directly, or a lambda wrapping
    ParallelSimulationEngine.run_survey_parallel via asyncio.run.

    Args:
        run_survey_fn: callable(personas=..., questions=..., survey_context=..., **kwargs)
        personas: All selected personas
        conditions: Condition list from the A/B config
        assignments: persona_id -> condition_id (from ABTestManager.assign_personas)
        questions: Follow-up questions
        **kwargs: Forwarded to run_survey_fn (temperature, max_tokens, ...)

    Returns:
        SimulationResult with each response dict tagged with 'condition'
    """
    from datetime import datetime
    from .simulation import SimulationResult

    merged = SimulationResult('ab_testing', datetime.now().isoformat())
    merged.questions = questions
    base_context = kwargs.pop('base_context', None)
    merged.metadata['assignments'] = assignments
    merged.metadata['conditions'] = [
        {
            'condition_id': c.condition_id,
            'condition_name': c.condition_name,
            'allocation_weight': c.allocation_weight,
        }
        for c in conditions
    ]

    for cond in conditions:
        group = [p for p in personas if assignments.get(p.persona_id) == cond.condition_id]
        if not group:
            continue
        context = (
            f"Please read the following material carefully and keep it in mind "
            f"while answering all questions:\n\n{cond.intervention_text}"
        )
        if base_context:
            context = f"{context}\n\n{base_context}"
        r = run_survey_fn(personas=group, questions=questions, survey_context=context, **kwargs)
        for key in ('model', 'seed', 'execution'):
            if key in r.metadata:
                merged.metadata[key] = r.metadata[key]
        for resp in r.persona_responses:
            resp['condition'] = cond.condition_name
        merged.persona_responses.extend(r.persona_responses)
        merged.metadata[f'n_{cond.condition_name}'] = len(group)
        if r.metadata.get('stopped_early'):
            merged.metadata['stopped_early'] = True
            merged.metadata['completed_queries'] = len(merged.persona_responses)
            merged.metadata['total_queries'] = len(personas) * len(questions)
            break

    return merged


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
        self.seed = seed
        self._rng = np.random.default_rng(seed)
        self.assignments: Dict[str, str] = {}  # persona_id -> condition_id
    
    def assign_personas(
        self,
        personas: List[Any],
        conditions: List[Condition],
        stratify_by: Optional[str] = None,
        random_assignment: bool = True,
    ) -> Dict[str, str]:
        """
        Randomly assign personas to conditions.
        
        Args:
            personas: List of Persona objects
            conditions: List of Condition objects
            stratify_by: Optional attribute to stratify by (e.g., 'gender')
            
        Returns:
            Dictionary mapping stable persona IDs to condition IDs
        """
        assignments = {}
        
        if stratify_by:
            # Stratified assignment
            strata = {}
            for persona in personas:
                if stratify_by == 'age_group':
                    age = getattr(persona, 'age', None)
                    if age is None:
                        stratum_value = 'Unknown'
                    elif age < 30:
                        stratum_value = '18-29'
                    elif age < 45:
                        stratum_value = '30-44'
                    elif age < 60:
                        stratum_value = '45-59'
                    else:
                        stratum_value = '60+'
                else:
                    stratum_value = getattr(persona, stratify_by, None) or 'Unknown'
                if stratum_value not in strata:
                    strata[stratum_value] = []
                strata[stratum_value].append(persona)
            
            # Assign within each stratum
            for stratum_value, stratum_personas in strata.items():
                stratum_assignments = self._random_assignment(
                    stratum_personas, conditions, random_assignment
                )
                assignments.update(stratum_assignments)
        else:
            # Simple random assignment
            assignments = self._random_assignment(personas, conditions, random_assignment)
        
        self.assignments = assignments
        return assignments
    
    def _random_assignment(
        self,
        personas: List[Any],
        conditions: List[Condition],
        random_assignment: bool = True,
    ) -> Dict[str, str]:
        """Allocate exact weighted group counts, optionally shuffling participants."""
        if not conditions:
            raise ValueError("At least one A/B condition is required")
        total_weight = sum(c.allocation_weight for c in conditions)
        if total_weight <= 0:
            raise ValueError("A/B condition allocation weights must sum to more than zero")
        probabilities = [c.allocation_weight / total_weight for c in conditions]
        condition_ids = [c.condition_id for c in conditions]

        expected = np.asarray(probabilities) * len(personas)
        counts = np.floor(expected).astype(int)
        remainder = len(personas) - int(counts.sum())
        if remainder:
            order = np.argsort(-(expected - counts))
            counts[order[:remainder]] += 1

        condition_pool = [
            condition_id
            for condition_id, count in zip(condition_ids, counts)
            for _ in range(int(count))
        ]
        ordered_personas = list(personas)
        if random_assignment:
            self._rng.shuffle(ordered_personas)
            self._rng.shuffle(condition_pool)

        return {
            persona.persona_id: condition_id
            for persona, condition_id in zip(ordered_personas, condition_pool)
        }
    
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
            # Welch's independent t-test is robust to unequal variances and
            # unequal group sizes, both common in stratified assignment.
            data1 = results_by_condition[condition_ids[0]]
            data2 = results_by_condition[condition_ids[1]]
            if len(data1) < 2 or len(data2) < 2:
                return {'error': 'Each condition needs at least 2 numeric observations'}
            t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=False)
            
            # Cohen's d
            pooled_std = np.sqrt(
                ((len(data1) - 1) * np.std(data1, ddof=1) ** 2 +
                 (len(data2) - 1) * np.std(data2, ddof=1) ** 2) /
                (len(data1) + len(data2) - 2)
            )
            cohens_d = (np.mean(data1) - np.mean(data2)) / pooled_std if pooled_std > 0 else 0
            
            return {
                'test': "Welch's t-test",
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
