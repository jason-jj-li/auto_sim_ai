"""Cost and time estimation for simulations."""
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class SimulationEstimate:
    """Container for simulation estimates."""
    total_llm_calls: int
    total_tokens_estimate: int
    estimated_time_seconds: float
    estimated_cost_usd: Optional[float]
    breakdown: Dict[str, Any]
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'total_llm_calls': self.total_llm_calls,
            'total_tokens_estimate': self.total_tokens_estimate,
            'estimated_time_seconds': self.estimated_time_seconds,
            'estimated_time_formatted': str(timedelta(seconds=int(self.estimated_time_seconds))),
            'estimated_cost_usd': self.estimated_cost_usd,
            'breakdown': self.breakdown,
            'warnings': self.warnings
        }


class SimulationEstimator:
    """Estimates cost, time, and resources for simulations."""
    
    def __init__(
        self,
        avg_response_time: float = 2.5,
        avg_tokens_per_question: int = 100,
        avg_tokens_per_response: int = 150,
        cost_per_1k_input_tokens: Optional[float] = None,
        cost_per_1k_output_tokens: Optional[float] = None
    ):
        """
        Initialize estimator.
        
        Args:
            avg_response_time: Average seconds per LLM call
            avg_tokens_per_question: Average tokens in a question
            avg_tokens_per_response: Average tokens in a response
            cost_per_1k_input_tokens: Cost per 1K input tokens (None for local)
            cost_per_1k_output_tokens: Cost per 1K output tokens (None for local)
        """
        self.avg_response_time = avg_response_time
        self.avg_tokens_per_question = avg_tokens_per_question
        self.avg_tokens_per_response = avg_tokens_per_response
        self.cost_per_1k_input_tokens = cost_per_1k_input_tokens
        self.cost_per_1k_output_tokens = cost_per_1k_output_tokens
        
        # Historical tracking
        self.historical_times: List[float] = []
    
    def update_historical_time(self, response_time: float):
        """
        Update historical response times for better estimates.
        
        Args:
            response_time: Actual response time in seconds
        """
        self.historical_times.append(response_time)
        # Keep only last 100 measurements
        if len(self.historical_times) > 100:
            self.historical_times = self.historical_times[-100:]
        
        # Update average
        if self.historical_times:
            self.avg_response_time = sum(self.historical_times) / len(self.historical_times)
    
    def estimate_simulation(
        self,
        num_personas: int,
        num_questions: int,
        consistency_repeats: int = 1,
        use_parallel: bool = False,
        max_workers: int = 5,
        use_cache: bool = False,
        cache_hit_rate: float = 0.0,
        persona_context_length: int = 200,
        survey_context_length: int = 100
    ) -> SimulationEstimate:
        """
        Estimate resources for a simulation.
        
        Args:
            num_personas: Number of personas
            num_questions: Number of questions
            consistency_repeats: Number of times to repeat for consistency checking
            use_parallel: Whether parallel processing is enabled
            max_workers: Number of parallel workers
            use_cache: Whether caching is enabled
            cache_hit_rate: Expected cache hit rate (0.0-1.0)
            persona_context_length: Average persona context length in tokens
            survey_context_length: Survey context length in tokens
            
        Returns:
            SimulationEstimate object
        """
        warnings = []
        
        # Calculate total LLM calls
        total_calls_raw = num_personas * num_questions * consistency_repeats
        
        # Adjust for cache hits
        if use_cache and cache_hit_rate > 0:
            cache_savings = int(total_calls_raw * cache_hit_rate)
            total_calls_actual = total_calls_raw - cache_savings
            warnings.append(f"Cache enabled: ~{cache_savings} calls saved ({cache_hit_rate*100:.0f}% hit rate)")
        else:
            total_calls_actual = total_calls_raw
        
        # Estimate tokens
        # Input tokens = persona context + survey context + question
        avg_input_tokens = (persona_context_length + 
                           survey_context_length + 
                           self.avg_tokens_per_question)
        total_input_tokens = total_calls_actual * avg_input_tokens
        total_output_tokens = total_calls_actual * self.avg_tokens_per_response
        total_tokens = total_input_tokens + total_output_tokens
        
        # Estimate time
        if use_parallel and max_workers > 1:
            # With parallelization, time is roughly divided by number of workers
            # But with some overhead
            parallelization_efficiency = 0.85  # Account for coordination overhead
            estimated_time = (total_calls_actual * self.avg_response_time) / (max_workers * parallelization_efficiency)
            warnings.append(f"Parallel processing enabled: ~{max_workers}x speedup expected")
        else:
            estimated_time = total_calls_actual * self.avg_response_time
        
        # Estimate cost (if API-based)
        estimated_cost = None
        if self.cost_per_1k_input_tokens and self.cost_per_1k_output_tokens:
            cost_input = (total_input_tokens / 1000) * self.cost_per_1k_input_tokens
            cost_output = (total_output_tokens / 1000) * self.cost_per_1k_output_tokens
            estimated_cost = cost_input + cost_output
        
        # Generate warnings
        if estimated_time > 3600:  # > 1 hour
            hours = estimated_time / 3600
            warnings.append(f"⚠️ Long simulation: ~{hours:.1f} hours estimated")
        
        if estimated_time > 7200:  # > 2 hours
            warnings.append("💡 Consider enabling parallel processing to reduce time")
        
        if not use_cache and consistency_repeats > 1:
            warnings.append("💡 Enable caching to avoid redundant LLM calls")
        
        if num_personas * num_questions > 10000:
            warnings.append("⚠️ Very large simulation: Consider breaking into batches")
        
        # Breakdown
        breakdown = {
            'personas': num_personas,
            'questions': num_questions,
            'consistency_repeats': consistency_repeats,
            'total_calls_raw': total_calls_raw,
            'total_calls_actual': total_calls_actual,
            'cache_savings': total_calls_raw - total_calls_actual if use_cache else 0,
            'avg_input_tokens_per_call': avg_input_tokens,
            'avg_output_tokens_per_call': self.avg_tokens_per_response,
            'total_input_tokens': total_input_tokens,
            'total_output_tokens': total_output_tokens,
            'parallel_enabled': use_parallel,
            'max_workers': max_workers if use_parallel else 1,
            'avg_response_time': self.avg_response_time
        }
        
        return SimulationEstimate(
            total_llm_calls=total_calls_actual,
            total_tokens_estimate=total_tokens,
            estimated_time_seconds=estimated_time,
            estimated_cost_usd=estimated_cost,
            breakdown=breakdown,
            warnings=warnings
        )
    
    def estimate_from_text(
        self,
        questions_text: str,
        num_personas: int,
        consistency_repeats: int = 1,
        **kwargs
    ) -> SimulationEstimate:
        """
        Estimate simulation based on question text.
        
        Args:
            questions_text: Text containing questions (one per line)
            num_personas: Number of personas
            consistency_repeats: Number of consistency repeats
            **kwargs: Additional arguments for estimate_simulation
            
        Returns:
            SimulationEstimate object
        """
        # Count questions
        questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
        num_questions = len(questions)
        
        # Estimate average tokens per question (rough: 1 token ≈ 4 chars)
        if questions:
            avg_question_len = sum(len(q) for q in questions) / len(questions)
            avg_tokens = int(avg_question_len / 4)
            self.avg_tokens_per_question = max(avg_tokens, 10)  # Minimum 10 tokens
        
        return self.estimate_simulation(
            num_personas=num_personas,
            num_questions=num_questions,
            consistency_repeats=consistency_repeats,
            **kwargs
        )
    
    def compare_scenarios(
        self,
        num_personas: int,
        num_questions: int,
        consistency_repeats: int = 1
    ) -> Dict[str, SimulationEstimate]:
        """
        Compare different simulation scenarios.
        
        Args:
            num_personas: Number of personas
            num_questions: Number of questions
            consistency_repeats: Number of consistency repeats
            
        Returns:
            Dictionary of scenario names to estimates
        """
        scenarios = {}
        
        # Baseline: Sequential, no cache
        scenarios['baseline'] = self.estimate_simulation(
            num_personas=num_personas,
            num_questions=num_questions,
            consistency_repeats=consistency_repeats,
            use_parallel=False,
            use_cache=False
        )
        
        # With caching
        scenarios['with_cache'] = self.estimate_simulation(
            num_personas=num_personas,
            num_questions=num_questions,
            consistency_repeats=consistency_repeats,
            use_parallel=False,
            use_cache=True,
            cache_hit_rate=0.3  # Conservative 30% hit rate
        )
        
        # With parallelization
        scenarios['with_parallel'] = self.estimate_simulation(
            num_personas=num_personas,
            num_questions=num_questions,
            consistency_repeats=consistency_repeats,
            use_parallel=True,
            max_workers=5,
            use_cache=False
        )
        
        # Optimized: Both cache and parallel
        scenarios['optimized'] = self.estimate_simulation(
            num_personas=num_personas,
            num_questions=num_questions,
            consistency_repeats=consistency_repeats,
            use_parallel=True,
            max_workers=5,
            use_cache=True,
            cache_hit_rate=0.3
        )
        
        return scenarios
    
    def format_time(self, seconds: float) -> str:
        """
        Format seconds into human-readable time.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted string (e.g., "2h 34m 12s")
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            secs = int(seconds % 60)
            if hours > 24:
                days = hours // 24
                hours = hours % 24
                return f"{days}d {hours}h {minutes}m"
            return f"{hours}h {minutes}m {secs}s"
    
    def get_recommendation(
        self,
        num_personas: int,
        num_questions: int,
        consistency_repeats: int = 1
    ) -> str:
        """
        Get recommendation for simulation configuration.
        
        Args:
            num_personas: Number of personas
            num_questions: Number of questions
            consistency_repeats: Number of consistency repeats
            
        Returns:
            Recommendation string
        """
        total_calls = num_personas * num_questions * consistency_repeats
        
        if total_calls < 100:
            return "✅ Small simulation - default settings recommended"
        elif total_calls < 500:
            return "💡 Medium simulation - consider enabling caching"
        elif total_calls < 2000:
            return "⚡ Large simulation - enable both caching and parallel processing (5 workers)"
        else:
            return "🚀 Very large simulation - enable caching, parallel processing (10 workers), and consider breaking into batches"

