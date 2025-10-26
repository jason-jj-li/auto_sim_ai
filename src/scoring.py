"""Scoring algorithms for standard psychological and health instruments."""
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd


class SurveyScorer:
    """Calculator for survey instrument scores."""
    
    @staticmethod
    def score_phq9(responses: List[int]) -> Dict[str, Any]:
        """Score PHQ-9 depression screening.
        
        Args:
            responses: List of 9 responses (0-3 each)
            
        Returns:
            Dictionary with score, severity, and interpretation
        """
        if len(responses) != 9:
            return {"error": "PHQ-9 requires exactly 9 responses"}
        
        total_score = sum(responses)
        
        # Determine severity
        if total_score <= 4:
            severity = "Minimal"
            color = "green"
        elif total_score <= 9:
            severity = "Mild"
            color = "yellow"
        elif total_score <= 14:
            severity = "Moderate"
            color = "orange"
        elif total_score <= 19:
            severity = "Moderately Severe"
            color = "darkorange"
        else:
            severity = "Severe"
            color = "red"
        
        return {
            "instrument": "PHQ-9",
            "total_score": total_score,
            "max_score": 27,
            "severity": severity,
            "color": color,
            "interpretation": f"{severity} depression (score: {total_score}/27)",
            "clinical_cutoff": total_score >= 10,  # Moderate or higher
            "items": responses
        }
    
    @staticmethod
    def score_gad7(responses: List[int]) -> Dict[str, Any]:
        """Score GAD-7 anxiety screening.
        
        Args:
            responses: List of 7 responses (0-3 each)
            
        Returns:
            Dictionary with score, severity, and interpretation
        """
        if len(responses) != 7:
            return {"error": "GAD-7 requires exactly 7 responses"}
        
        total_score = sum(responses)
        
        # Determine severity
        if total_score <= 4:
            severity = "Minimal"
            color = "green"
        elif total_score <= 9:
            severity = "Mild"
            color = "yellow"
        elif total_score <= 14:
            severity = "Moderate"
            color = "orange"
        else:
            severity = "Severe"
            color = "red"
        
        return {
            "instrument": "GAD-7",
            "total_score": total_score,
            "max_score": 21,
            "severity": severity,
            "color": color,
            "interpretation": f"{severity} anxiety (score: {total_score}/21)",
            "clinical_cutoff": total_score >= 10,  # Moderate or higher
            "items": responses
        }
    
    @staticmethod
    def score_pss10(responses: List[int]) -> Dict[str, Any]:
        """Score PSS-10 perceived stress scale.
        
        Args:
            responses: List of 10 responses (0-4 each)
            
        Returns:
            Dictionary with score, severity, and interpretation
        """
        if len(responses) != 10:
            return {"error": "PSS-10 requires exactly 10 responses"}
        
        # Reverse score items 4, 5, 7, 8 (indices 3, 4, 6, 7)
        reverse_indices = [3, 4, 6, 7]
        scored_responses = responses.copy()
        
        for idx in reverse_indices:
            scored_responses[idx] = 4 - scored_responses[idx]
        
        total_score = sum(scored_responses)
        
        # Determine stress level
        if total_score <= 13:
            level = "Low"
            color = "green"
        elif total_score <= 26:
            level = "Moderate"
            color = "yellow"
        else:
            level = "High"
            color = "red"
        
        return {
            "instrument": "PSS-10",
            "total_score": total_score,
            "max_score": 40,
            "severity": level,
            "color": color,
            "interpretation": f"{level} perceived stress (score: {total_score}/40)",
            "clinical_cutoff": total_score >= 27,  # High stress
            "items": responses,
            "reverse_scored_items": reverse_indices
        }
    
    @staticmethod
    def score_who5(responses: List[int]) -> Dict[str, Any]:
        """Score WHO-5 Well-Being Index.
        
        Args:
            responses: List of 5 responses (0-5 each)
            
        Returns:
            Dictionary with score, percentage, and interpretation
        """
        if len(responses) != 5:
            return {"error": "WHO-5 requires exactly 5 responses"}
        
        raw_score = sum(responses)
        percentage_score = (raw_score / 25) * 100
        
        # Determine well-being level
        if percentage_score < 28:
            level = "Poor"
            color = "red"
            note = "Score suggests need for depression screening"
        elif percentage_score < 50:
            level = "Below Average"
            color = "orange"
            note = "Low well-being"
        elif percentage_score < 70:
            level = "Average"
            color = "yellow"
            note = "Adequate well-being"
        else:
            level = "Good to Excellent"
            color = "green"
            note = "Good well-being"
        
        return {
            "instrument": "WHO-5",
            "raw_score": raw_score,
            "max_score": 25,
            "percentage_score": round(percentage_score, 1),
            "severity": level,
            "color": color,
            "interpretation": f"{level} well-being ({percentage_score:.1f}%)",
            "clinical_cutoff": percentage_score < 50,  # Below 50% threshold
            "note": note,
            "items": responses
        }
    
    @staticmethod
    def score_survey(instrument_name: str, responses: List[int]) -> Dict[str, Any]:
        """Score a survey based on instrument name.
        
        Args:
            instrument_name: Name of the instrument (PHQ-9, GAD-7, etc.)
            responses: List of numeric responses
            
        Returns:
            Dictionary with scoring results
        """
        scorers = {
            "PHQ-9": SurveyScorer.score_phq9,
            "GAD-7": SurveyScorer.score_gad7,
            "PSS-10": SurveyScorer.score_pss10,
            "WHO-5": SurveyScorer.score_who5,
        }
        
        scorer = scorers.get(instrument_name)
        if scorer:
            return scorer(responses)
        else:
            return {
                "error": f"Unknown instrument: {instrument_name}",
                "instrument": instrument_name,
                "total_score": sum(responses) if responses else 0,
                "items": responses
            }
    
    @staticmethod
    def calculate_scores_for_personas(
        results_df: pd.DataFrame,
        instrument_name: str
    ) -> pd.DataFrame:
        """Calculate scores for each persona from results dataframe.
        
        Args:
            results_df: DataFrame with columns [persona_name, question, response]
            instrument_name: Name of the instrument
            
        Returns:
            DataFrame with persona scores and interpretations
        """
        scores = []
        
        # Group by persona
        for persona_name, group in results_df.groupby('persona_name'):
            # Get responses in order
            responses_str = group.sort_values('question')['response'].tolist()
            
            # Convert to numeric
            try:
                responses = [int(r) for r in responses_str]
            except (ValueError, TypeError):
                continue
            
            # Calculate score
            score_result = SurveyScorer.score_survey(instrument_name, responses)
            
            if 'error' not in score_result:
                scores.append({
                    'persona_name': persona_name,
                    'instrument': instrument_name,
                    'total_score': score_result.get('total_score', score_result.get('raw_score')),
                    'severity': score_result.get('severity', ''),
                    'interpretation': score_result.get('interpretation', ''),
                    'clinical_cutoff': score_result.get('clinical_cutoff', False),
                    'percentage_score': score_result.get('percentage_score'),
                    'color': score_result.get('color', 'gray')
                })
        
        return pd.DataFrame(scores)
    
    @staticmethod
    def get_score_statistics(scores_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate statistics for a set of scores.
        
        Args:
            scores_df: DataFrame with persona scores
            
        Returns:
            Dictionary with statistical summary
        """
        if scores_df.empty:
            return {}
        
        stats = {
            "mean_score": scores_df['total_score'].mean(),
            "median_score": scores_df['total_score'].median(),
            "std_score": scores_df['total_score'].std(),
            "min_score": scores_df['total_score'].min(),
            "max_score": scores_df['total_score'].max(),
            "n_personas": len(scores_df),
        }
        
        # Count severity levels
        if 'severity' in scores_df.columns:
            severity_counts = scores_df['severity'].value_counts().to_dict()
            stats['severity_distribution'] = severity_counts
        
        # Count clinical cases
        if 'clinical_cutoff' in scores_df.columns:
            stats['n_clinical'] = scores_df['clinical_cutoff'].sum()
            stats['pct_clinical'] = (stats['n_clinical'] / stats['n_personas']) * 100
        
        return stats

