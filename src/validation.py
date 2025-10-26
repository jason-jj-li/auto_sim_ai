"""Response validation and consistency checking for LLM simulations."""
import re
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ConsistencyMetrics:
    """Metrics for response consistency analysis."""
    persona_name: str
    question: str
    responses: List[str]
    mean_value: Optional[float]
    std_dev: Optional[float]
    coefficient_variation: Optional[float]
    consistency_score: float  # 0-1, higher is more consistent
    is_consistent: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'persona_name': self.persona_name,
            'question': self.question,
            'responses': self.responses,
            'mean_value': self.mean_value,
            'std_dev': self.std_dev,
            'coefficient_variation': self.coefficient_variation,
            'consistency_score': self.consistency_score,
            'is_consistent': self.is_consistent
        }


class ResponseValidator:
    """Validates LLM responses for quality and consistency."""
    
    # Non-responsive patterns
    NON_RESPONSIVE_PATTERNS = [
        r"^i don'?t know",
        r"^n/?a$",
        r"^not applicable",
        r"^cannot (answer|respond|say)",
        r"^unable to (answer|respond|say)",
        r"^i('m| am) (not sure|unsure|uncertain)",
        r"^no (answer|response|comment)",
        r"^skip",
        r"^pass$"
    ]
    
    # Generic/evasive patterns
    GENERIC_PATTERNS = [
        r"^(it depends|that depends)",
        r"^(maybe|perhaps|possibly)$",
        r"^i (would say|think|believe|feel) (that )?it",
        r"^well,? (i think|i guess|i suppose)",
    ]
    
    def __init__(
        self,
        non_responsive_threshold: float = 0.8,
        generic_threshold: float = 0.7,
        min_response_length: int = 3
    ):
        """
        Initialize validator.
        
        Args:
            non_responsive_threshold: Confidence threshold for flagging non-responsive
            generic_threshold: Confidence threshold for flagging generic responses
            min_response_length: Minimum response length in characters
        """
        self.non_responsive_threshold = non_responsive_threshold
        self.generic_threshold = generic_threshold
        self.min_response_length = min_response_length
    
    def is_non_responsive(self, response: str) -> Tuple[bool, str]:
        """
        Check if response is non-responsive.
        
        Returns:
            (is_non_responsive, reason)
        """
        if not response or len(response.strip()) < self.min_response_length:
            return True, "Empty or too short"
        
        response_lower = response.lower().strip()
        
        # Check patterns
        for pattern in self.NON_RESPONSIVE_PATTERNS:
            if re.search(pattern, response_lower):
                return True, f"Matches non-responsive pattern: {pattern}"
        
        return False, ""
    
    def is_generic(self, response: str) -> Tuple[bool, str]:
        """
        Check if response is generic or evasive.
        
        Returns:
            (is_generic, reason)
        """
        response_lower = response.lower().strip()
        
        for pattern in self.GENERIC_PATTERNS:
            if re.search(pattern, response_lower):
                return True, f"Matches generic pattern: {pattern}"
        
        # Check for very short responses that don't provide information
        words = response.split()
        if len(words) <= 2:
            return True, "Too short to be informative"
        
        return False, ""
    
    def is_repetitive(self, response: str, previous_responses: List[str]) -> Tuple[bool, float]:
        """
        Check if response is repetitive compared to previous responses.
        
        Returns:
            (is_repetitive, similarity_score)
        """
        if not previous_responses:
            return False, 0.0
        
        # Simple word-overlap similarity
        response_words = set(response.lower().split())
        max_similarity = 0.0
        
        for prev_response in previous_responses:
            prev_words = set(prev_response.lower().split())
            if len(response_words) == 0 or len(prev_words) == 0:
                continue
            
            intersection = response_words.intersection(prev_words)
            union = response_words.union(prev_words)
            similarity = len(intersection) / len(union) if union else 0.0
            max_similarity = max(max_similarity, similarity)
        
        # Consider repetitive if >80% word overlap
        return max_similarity > 0.8, max_similarity
    
    def validate_response(
        self,
        response: str,
        previous_responses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive response validation.
        
        Returns:
            Dictionary with validation results
        """
        results = {
            'is_valid': True,
            'issues': []
        }
        
        # Check non-responsive
        is_non_resp, reason = self.is_non_responsive(response)
        if is_non_resp:
            results['is_valid'] = False
            results['issues'].append(f"Non-responsive: {reason}")
        
        # Check generic
        is_gen, reason = self.is_generic(response)
        if is_gen:
            results['issues'].append(f"Generic response: {reason}")
        
        # Check repetitive
        if previous_responses:
            is_rep, similarity = self.is_repetitive(response, previous_responses)
            if is_rep:
                results['issues'].append(f"Repetitive (similarity: {similarity:.2f})")
        
        return results


class ConsistencyChecker:
    """Checks consistency of responses across multiple trials."""
    
    def __init__(self, consistency_threshold: float = 0.8):
        """
        Initialize consistency checker.
        
        Args:
            consistency_threshold: Threshold for considering responses consistent (0-1)
        """
        self.consistency_threshold = consistency_threshold
    
    def check_numeric_consistency(
        self,
        persona_name: str,
        question: str,
        responses: List[str]
    ) -> ConsistencyMetrics:
        """
        Check consistency for numeric responses.
        
        Args:
            persona_name: Name of persona
            question: Question text
            responses: List of response strings
            
        Returns:
            ConsistencyMetrics object
        """
        # Extract numeric values
        numeric_values = []
        for response in responses:
            match = re.search(r'-?\d+\.?\d*', response)
            if match:
                try:
                    numeric_values.append(float(match.group()))
                except:
                    pass
        
        if len(numeric_values) < 2:
            # Not enough numeric responses to check consistency
            return ConsistencyMetrics(
                persona_name=persona_name,
                question=question,
                responses=responses,
                mean_value=None,
                std_dev=None,
                coefficient_variation=None,
                consistency_score=0.0,
                is_consistent=False
            )
        
        # Calculate statistics
        mean_val = np.mean(numeric_values)
        std_val = np.std(numeric_values)
        cv = std_val / abs(mean_val) if mean_val != 0 else float('inf')
        
        # Consistency score: higher when CV is lower
        # CV < 0.1 = very consistent (score ~1.0)
        # CV > 0.5 = inconsistent (score ~0.0)
        consistency_score = max(0.0, 1.0 - (cv / 0.5))
        
        is_consistent = consistency_score >= self.consistency_threshold
        
        return ConsistencyMetrics(
            persona_name=persona_name,
            question=question,
            responses=responses,
            mean_value=mean_val,
            std_dev=std_val,
            coefficient_variation=cv,
            consistency_score=consistency_score,
            is_consistent=is_consistent
        )
    
    def check_categorical_consistency(
        self,
        persona_name: str,
        question: str,
        responses: List[str]
    ) -> ConsistencyMetrics:
        """
        Check consistency for categorical responses.
        
        Args:
            persona_name: Name of persona
            question: Question text
            responses: List of response strings
            
        Returns:
            ConsistencyMetrics object
        """
        if len(responses) < 2:
            return ConsistencyMetrics(
                persona_name=persona_name,
                question=question,
                responses=responses,
                mean_value=None,
                std_dev=None,
                coefficient_variation=None,
                consistency_score=0.0,
                is_consistent=False
            )
        
        # Normalize responses
        normalized = [r.strip().lower() for r in responses]
        
        # Count most common response
        from collections import Counter
        counts = Counter(normalized)
        most_common_count = counts.most_common(1)[0][1]
        
        # Consistency score = proportion of most common response
        consistency_score = most_common_count / len(responses)
        
        is_consistent = consistency_score >= self.consistency_threshold
        
        return ConsistencyMetrics(
            persona_name=persona_name,
            question=question,
            responses=responses,
            mean_value=None,
            std_dev=None,
            coefficient_variation=None,
            consistency_score=consistency_score,
            is_consistent=is_consistent
        )
    
    def analyze_all_responses(
        self,
        results: List[Dict[str, Any]],
        response_type: str = 'auto'
    ) -> List[ConsistencyMetrics]:
        """
        Analyze consistency across all persona-question pairs.
        
        Args:
            results: List of response dictionaries from simulation
            response_type: 'numeric', 'categorical', or 'auto'
            
        Returns:
            List of ConsistencyMetrics objects
        """
        # Group responses by persona and question
        grouped = defaultdict(lambda: defaultdict(list))
        for result in results:
            persona_name = result.get('persona_name', 'Unknown')
            question = result.get('question', 'Unknown')
            response = result.get('response', '')
            grouped[persona_name][question].append(response)
        
        # Analyze each group
        metrics = []
        for persona_name, questions in grouped.items():
            for question, responses in questions.items():
                if len(responses) < 2:
                    continue  # Need at least 2 responses to check consistency
                
                # Auto-detect response type if needed
                if response_type == 'auto':
                    # Check if responses are numeric
                    is_numeric = any(re.search(r'-?\d+\.?\d*', r) for r in responses)
                    detected_type = 'numeric' if is_numeric else 'categorical'
                else:
                    detected_type = response_type
                
                # Check consistency based on type
                if detected_type == 'numeric':
                    metric = self.check_numeric_consistency(persona_name, question, responses)
                else:
                    metric = self.check_categorical_consistency(persona_name, question, responses)
                
                metrics.append(metric)
        
        return metrics
    
    def generate_consistency_report(
        self,
        metrics: List[ConsistencyMetrics]
    ) -> Dict[str, Any]:
        """
        Generate summary report of consistency analysis.
        
        Args:
            metrics: List of ConsistencyMetrics objects
            
        Returns:
            Summary report dictionary
        """
        if not metrics:
            return {
                'total_checks': 0,
                'consistent_count': 0,
                'inconsistent_count': 0,
                'consistency_rate': 0.0,
                'avg_consistency_score': 0.0
            }
        
        consistent_count = sum(1 for m in metrics if m.is_consistent)
        avg_score = np.mean([m.consistency_score for m in metrics])
        
        # Find most inconsistent
        inconsistent = sorted(
            [m for m in metrics if not m.is_consistent],
            key=lambda m: m.consistency_score
        )[:10]  # Top 10 most inconsistent
        
        return {
            'total_checks': len(metrics),
            'consistent_count': consistent_count,
            'inconsistent_count': len(metrics) - consistent_count,
            'consistency_rate': consistent_count / len(metrics),
            'avg_consistency_score': avg_score,
            'most_inconsistent': [m.to_dict() for m in inconsistent]
        }

