"""Sensitivity analysis for testing robustness of findings."""
from typing import List, Dict, Any, Optional, Callable
import numpy as np
from copy import deepcopy


class SensitivityAnalyzer:
    """Analyze sensitivity of results to parameter changes."""
    
    def __init__(self):
        """Initialize sensitivity analyzer."""
        self.results_cache: Dict[str, Any] = {}
    
    def temperature_sensitivity(
        self,
        simulation_func: Callable,
        personas: List[Any],
        questions: List[str],
        temperature_range: List[float] = [0.3, 0.5, 0.7, 0.9, 1.1],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Test sensitivity to temperature parameter.
        
        Args:
            simulation_func: Function that runs simulation
            personas: List of personas
            questions: List of questions
            temperature_range: Temperatures to test
            **kwargs: Other simulation parameters
            
        Returns:
            Sensitivity analysis results
        """
        results_by_temp = {}
        
        for temp in temperature_range:
            result = simulation_func(
                personas=personas,
                questions=questions,
                temperature=temp,
                **kwargs
            )
            results_by_temp[temp] = result
        
        # Analyze variance across temperatures
        analysis = {
            'temperature_range': temperature_range,
            'results': results_by_temp,
            'variance': self._calculate_response_variance(results_by_temp),
            'robust_findings': []
        }
        
        return analysis
    
    def bootstrap_confidence_intervals(
        self,
        data: List[float],
        n_bootstrap: int = 1000,
        confidence_level: float = 0.95
    ) -> Dict[str, float]:
        """
        Calculate bootstrap confidence intervals.
        
        Args:
            data: Numeric data
            n_bootstrap: Number of bootstrap samples
            confidence_level: Confidence level (e.g., 0.95 for 95% CI)
            
        Returns:
            Dictionary with mean and CI bounds
        """
        if len(data) < 2:
            return {'mean': 0, 'lower': 0, 'upper': 0}
        
        bootstrap_means = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(data, size=len(data), replace=True)
            bootstrap_means.append(np.mean(sample))
        
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        return {
            'mean': float(np.mean(data)),
            'lower': float(np.percentile(bootstrap_means, lower_percentile)),
            'upper': float(np.percentile(bootstrap_means, upper_percentile)),
            'std_error': float(np.std(bootstrap_means))
        }
    
    def _calculate_response_variance(
        self,
        results_by_param: Dict[Any, Any]
    ) -> float:
        """Calculate variance in responses across parameter values."""
        # Extract all numeric responses
        all_responses = []
        for result in results_by_param.values():
            if hasattr(result, 'persona_responses'):
                for resp in result.persona_responses:
                    response_text = resp.get('response', '')
                    # Try to extract numeric value
                    try:
                        numeric_val = float(response_text)
                        all_responses.append(numeric_val)
                    except:
                        pass
        
        if len(all_responses) > 1:
            return float(np.var(all_responses))
        return 0.0
    
    def compare_models(
        self,
        results_model_a: List[Dict[str, Any]],
        results_model_b: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare results from two different models.
        
        Args:
            results_model_a: Results from model A
            results_model_b: Results from model B
            
        Returns:
            Comparison metrics
        """
        # Extract responses
        responses_a = [r.get('response', '') for r in results_model_a]
        responses_b = [r.get('response', '') for r in results_model_b]
        
        # Calculate agreement rate
        agreement = sum(1 for a, b in zip(responses_a, responses_b) if a == b)
        agreement_rate = agreement / len(responses_a) if responses_a else 0
        
        return {
            'agreement_rate': agreement_rate,
            'num_comparisons': len(responses_a),
            'agreements': agreement,
            'disagreements': len(responses_a) - agreement
        }
    
    def robustness_score(
        self,
        variance: float,
        threshold: float = 0.1
    ) -> Dict[str, Any]:
        """
        Calculate robustness score based on variance.
        
        Args:
            variance: Variance across parameter settings
            threshold: Threshold for considering robust
            
        Returns:
            Robustness assessment
        """
        if variance < threshold:
            status = 'robust'
            score = 1.0 - (variance / threshold)
        else:
            status = 'fragile'
            score = threshold / variance if variance > 0 else 0
        
        return {
            'score': float(score),
            'status': status,
            'variance': float(variance),
            'threshold': threshold
        }
