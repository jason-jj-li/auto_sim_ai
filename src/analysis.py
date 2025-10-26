"""Statistical analysis module for survey simulation results."""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from scipy import stats
from dataclasses import dataclass


@dataclass
class StatisticalResult:
    """Container for statistical test results."""
    test_name: str
    statistic: float
    p_value: float
    effect_size: Optional[float]
    interpretation: str
    details: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'test_name': self.test_name,
            'statistic': self.statistic,
            'p_value': self.p_value,
            'effect_size': self.effect_size,
            'interpretation': self.interpretation,
            'details': self.details
        }


class StatisticalAnalyzer:
    """Comprehensive statistical analysis for survey data."""
    
    def __init__(self, significance_level: float = 0.05):
        """
        Initialize analyzer.
        
        Args:
            significance_level: Alpha level for hypothesis tests (default: 0.05)
        """
        self.alpha = significance_level
    
    def descriptive_stats(
        self,
        data: pd.DataFrame,
        numeric_columns: Optional[List[str]] = None,
        groupby: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate descriptive statistics.
        
        Args:
            data: DataFrame with survey responses
            numeric_columns: Columns to analyze (auto-detect if None)
            groupby: Column to group by (e.g., 'persona_gender')
            
        Returns:
            Dictionary with descriptive stats
        """
        if numeric_columns is None:
            numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_columns:
            return {'error': 'No numeric columns found'}
        
        results = {}
        
        if groupby and groupby in data.columns:
            # Grouped statistics
            for col in numeric_columns:
                if col in data.columns:
                    grouped = data.groupby(groupby)[col].agg([
                        'count', 'mean', 'median', 'std', 'min', 'max',
                        ('q25', lambda x: x.quantile(0.25)),
                        ('q75', lambda x: x.quantile(0.75))
                    ])
                    results[col] = grouped.to_dict('index')
        else:
            # Overall statistics
            for col in numeric_columns:
                if col in data.columns:
                    col_data = data[col].dropna()
                    if len(col_data) > 0:
                        results[col] = {
                            'count': len(col_data),
                            'mean': float(col_data.mean()),
                            'median': float(col_data.median()),
                            'std': float(col_data.std()),
                            'min': float(col_data.min()),
                            'max': float(col_data.max()),
                            'q25': float(col_data.quantile(0.25)),
                            'q75': float(col_data.quantile(0.75)),
                            'mode': float(col_data.mode()[0]) if len(col_data.mode()) > 0 else None
                        }
        
        return results
    
    def independent_t_test(
        self,
        data: pd.DataFrame,
        dependent_var: str,
        group_var: str,
        group1: str,
        group2: str
    ) -> StatisticalResult:
        """
        Perform independent samples t-test.
        
        Args:
            data: DataFrame with survey responses
            dependent_var: Column with numeric values to compare
            group_var: Column with group labels
            group1: First group label
            group2: Second group label
            
        Returns:
            StatisticalResult object
        """
        group1_data = data[data[group_var] == group1][dependent_var].dropna()
        group2_data = data[data[group_var] == group2][dependent_var].dropna()
        
        if len(group1_data) < 2 or len(group2_data) < 2:
            return StatisticalResult(
                test_name='Independent t-test',
                statistic=0.0,
                p_value=1.0,
                effect_size=None,
                interpretation='Insufficient data for analysis',
                details={}
            )
        
        # Perform t-test
        statistic, p_value = stats.ttest_ind(group1_data, group2_data)
        
        # Calculate Cohen's d (effect size)
        pooled_std = np.sqrt(
            ((len(group1_data) - 1) * group1_data.std() ** 2 +
             (len(group2_data) - 1) * group2_data.std() ** 2) /
            (len(group1_data) + len(group2_data) - 2)
        )
        cohens_d = (group1_data.mean() - group2_data.mean()) / pooled_std if pooled_std > 0 else 0.0
        
        # Interpretation
        if p_value < self.alpha:
            interpretation = f'Significant difference (p < {self.alpha}). '
        else:
            interpretation = f'No significant difference (p >= {self.alpha}). '
        
        if abs(cohens_d) < 0.2:
            interpretation += 'Negligible effect size.'
        elif abs(cohens_d) < 0.5:
            interpretation += 'Small effect size.'
        elif abs(cohens_d) < 0.8:
            interpretation += 'Medium effect size.'
        else:
            interpretation += 'Large effect size.'
        
        return StatisticalResult(
            test_name='Independent t-test',
            statistic=float(statistic),
            p_value=float(p_value),
            effect_size=float(cohens_d),
            interpretation=interpretation,
            details={
                'group1_mean': float(group1_data.mean()),
                'group2_mean': float(group2_data.mean()),
                'group1_std': float(group1_data.std()),
                'group2_std': float(group2_data.std()),
                'group1_n': len(group1_data),
                'group2_n': len(group2_data)
            }
        )
    
    def paired_t_test(
        self,
        data: pd.DataFrame,
        var1: str,
        var2: str,
        id_var: str
    ) -> StatisticalResult:
        """
        Perform paired samples t-test.
        
        Args:
            data: DataFrame with survey responses
            var1: First variable (e.g., pre-test)
            var2: Second variable (e.g., post-test)
            id_var: ID column to match pairs
            
        Returns:
            StatisticalResult object
        """
        # Ensure we have matched pairs
        paired_data = data[[id_var, var1, var2]].dropna()
        
        if len(paired_data) < 2:
            return StatisticalResult(
                test_name='Paired t-test',
                statistic=0.0,
                p_value=1.0,
                effect_size=None,
                interpretation='Insufficient paired data',
                details={}
            )
        
        # Perform paired t-test
        statistic, p_value = stats.ttest_rel(paired_data[var1], paired_data[var2])
        
        # Calculate effect size (Cohen's d for paired samples)
        diff = paired_data[var1] - paired_data[var2]
        cohens_d = diff.mean() / diff.std() if diff.std() > 0 else 0.0
        
        # Interpretation
        if p_value < self.alpha:
            interpretation = f'Significant difference (p < {self.alpha}). '
        else:
            interpretation = f'No significant difference (p >= {self.alpha}). '
        
        if abs(cohens_d) < 0.2:
            interpretation += 'Negligible effect size.'
        elif abs(cohens_d) < 0.5:
            interpretation += 'Small effect size.'
        elif abs(cohens_d) < 0.8:
            interpretation += 'Medium effect size.'
        else:
            interpretation += 'Large effect size.'
        
        return StatisticalResult(
            test_name='Paired t-test',
            statistic=float(statistic),
            p_value=float(p_value),
            effect_size=float(cohens_d),
            interpretation=interpretation,
            details={
                'mean_difference': float(diff.mean()),
                'std_difference': float(diff.std()),
                'n_pairs': len(paired_data)
            }
        )
    
    def one_way_anova(
        self,
        data: pd.DataFrame,
        dependent_var: str,
        group_var: str
    ) -> StatisticalResult:
        """
        Perform one-way ANOVA.
        
        Args:
            data: DataFrame with survey responses
            dependent_var: Column with numeric values
            group_var: Column with group labels
            
        Returns:
            StatisticalResult object
        """
        groups = data[group_var].unique()
        if len(groups) < 2:
            return StatisticalResult(
                test_name='One-way ANOVA',
                statistic=0.0,
                p_value=1.0,
                effect_size=None,
                interpretation='Need at least 2 groups',
                details={}
            )
        
        # Extract data for each group
        group_data = [data[data[group_var] == g][dependent_var].dropna() for g in groups]
        group_data = [g for g in group_data if len(g) > 0]
        
        if len(group_data) < 2:
            return StatisticalResult(
                test_name='One-way ANOVA',
                statistic=0.0,
                p_value=1.0,
                effect_size=None,
                interpretation='Insufficient data in groups',
                details={}
            )
        
        # Perform ANOVA
        statistic, p_value = stats.f_oneway(*group_data)
        
        # Calculate eta-squared (effect size)
        grand_mean = data[dependent_var].mean()
        ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in group_data)
        ss_total = sum((data[dependent_var] - grand_mean) ** 2)
        eta_squared = ss_between / ss_total if ss_total > 0 else 0.0
        
        # Interpretation
        if p_value < self.alpha:
            interpretation = f'Significant group differences (p < {self.alpha}). '
        else:
            interpretation = f'No significant group differences (p >= {self.alpha}). '
        
        if eta_squared < 0.01:
            interpretation += 'Negligible effect size.'
        elif eta_squared < 0.06:
            interpretation += 'Small effect size.'
        elif eta_squared < 0.14:
            interpretation += 'Medium effect size.'
        else:
            interpretation += 'Large effect size.'
        
        return StatisticalResult(
            test_name='One-way ANOVA',
            statistic=float(statistic),
            p_value=float(p_value),
            effect_size=float(eta_squared),
            interpretation=interpretation,
            details={
                'num_groups': len(groups),
                'group_means': {str(g): float(data[data[group_var] == g][dependent_var].mean()) 
                               for g in groups}
            }
        )
    
    def chi_square_test(
        self,
        data: pd.DataFrame,
        var1: str,
        var2: str
    ) -> StatisticalResult:
        """
        Perform chi-square test of independence for categorical variables.
        
        Args:
            data: DataFrame with survey responses
            var1: First categorical variable
            var2: Second categorical variable
            
        Returns:
            StatisticalResult object
        """
        # Create contingency table
        contingency_table = pd.crosstab(data[var1], data[var2])
        
        if contingency_table.size < 4:
            return StatisticalResult(
                test_name='Chi-square test',
                statistic=0.0,
                p_value=1.0,
                effect_size=None,
                interpretation='Insufficient categories for chi-square',
                details={}
            )
        
        # Perform chi-square test
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # Calculate Cramér's V (effect size)
        n = contingency_table.sum().sum()
        min_dim = min(contingency_table.shape[0] - 1, contingency_table.shape[1] - 1)
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0.0
        
        # Interpretation
        if p_value < self.alpha:
            interpretation = f'Significant association (p < {self.alpha}). '
        else:
            interpretation = f'No significant association (p >= {self.alpha}). '
        
        if cramers_v < 0.1:
            interpretation += 'Negligible effect size.'
        elif cramers_v < 0.3:
            interpretation += 'Small effect size.'
        elif cramers_v < 0.5:
            interpretation += 'Medium effect size.'
        else:
            interpretation += 'Large effect size.'
        
        return StatisticalResult(
            test_name='Chi-square test',
            statistic=float(chi2),
            p_value=float(p_value),
            effect_size=float(cramers_v),
            interpretation=interpretation,
            details={
                'degrees_of_freedom': int(dof),
                'contingency_table': contingency_table.to_dict()
            }
        )
    
    def correlation_analysis(
        self,
        data: pd.DataFrame,
        variables: Optional[List[str]] = None,
        method: str = 'pearson'
    ) -> Dict[str, Any]:
        """
        Calculate correlation matrix.
        
        Args:
            data: DataFrame with survey responses
            variables: List of variables to correlate (auto-detect if None)
            method: 'pearson', 'spearman', or 'kendall'
            
        Returns:
            Dictionary with correlation matrix and p-values
        """
        if variables is None:
            variables = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(variables) < 2:
            return {'error': 'Need at least 2 numeric variables'}
        
        # Select only specified variables
        df = data[variables].dropna()
        
        if len(df) < 3:
            return {'error': 'Insufficient data for correlation'}
        
        # Calculate correlation matrix
        if method == 'pearson':
            corr_matrix = df.corr(method='pearson')
        elif method == 'spearman':
            corr_matrix = df.corr(method='spearman')
        elif method == 'kendall':
            corr_matrix = df.corr(method='kendall')
        else:
            return {'error': f'Unknown correlation method: {method}'}
        
        # Calculate p-values
        n = len(df)
        p_values = pd.DataFrame(np.zeros((len(variables), len(variables))),
                               columns=variables, index=variables)
        
        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if i != j:
                    if method == 'pearson':
                        _, p = stats.pearsonr(df[var1], df[var2])
                    elif method == 'spearman':
                        _, p = stats.spearmanr(df[var1], df[var2])
                    elif method == 'kendall':
                        _, p = stats.kendalltau(df[var1], df[var2])
                    p_values.iloc[i, j] = p
        
        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'p_values': p_values.to_dict(),
            'method': method,
            'n': n
        }
    
    def cronbachs_alpha(
        self,
        data: pd.DataFrame,
        items: List[str]
    ) -> Dict[str, Any]:
        """
        Calculate Cronbach's alpha for scale reliability.
        
        Args:
            data: DataFrame with survey responses
            items: List of item columns to include in scale
            
        Returns:
            Dictionary with alpha and related statistics
        """
        # Select item data
        item_data = data[items].dropna()
        
        if len(item_data) < 2:
            return {'error': 'Insufficient data', 'alpha': None}
        
        # Calculate Cronbach's alpha
        n_items = len(items)
        item_variances = item_data.var(axis=0, ddof=1)
        total_variance = item_data.sum(axis=1).var(ddof=1)
        
        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
        
        # Calculate item-total correlations
        scale_scores = item_data.sum(axis=1)
        item_total_corr = {}
        alpha_if_deleted = {}
        
        for item in items:
            # Item-total correlation (corrected)
            scale_without_item = scale_scores - item_data[item]
            corr, _ = stats.pearsonr(item_data[item], scale_without_item)
            item_total_corr[item] = float(corr)
            
            # Alpha if item deleted
            remaining_items = [i for i in items if i != item]
            if len(remaining_items) > 1:
                remaining_data = item_data[remaining_items]
                remaining_vars = remaining_data.var(axis=0, ddof=1)
                remaining_total_var = remaining_data.sum(axis=1).var(ddof=1)
                alpha_deleted = ((len(remaining_items) / (len(remaining_items) - 1)) *
                               (1 - remaining_vars.sum() / remaining_total_var))
                alpha_if_deleted[item] = float(alpha_deleted)
        
        # Interpretation
        if alpha >= 0.9:
            interpretation = 'Excellent reliability'
        elif alpha >= 0.8:
            interpretation = 'Good reliability'
        elif alpha >= 0.7:
            interpretation = 'Acceptable reliability'
        elif alpha >= 0.6:
            interpretation = 'Questionable reliability'
        elif alpha >= 0.5:
            interpretation = 'Poor reliability'
        else:
            interpretation = 'Unacceptable reliability'
        
        return {
            'alpha': float(alpha),
            'interpretation': interpretation,
            'n_items': n_items,
            'n_observations': len(item_data),
            'item_total_correlations': item_total_corr,
            'alpha_if_item_deleted': alpha_if_deleted
        }

