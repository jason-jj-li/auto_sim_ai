"""Export module for generating analysis-ready scripts in R, Python, and SPSS."""
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd


class ScriptGenerator:
    """Generate analysis scripts in various languages."""
    
    def __init__(self, data_filename: str, output_dir: str = "exports"):
        """
        Initialize script generator.
        
        Args:
            data_filename: Name of the CSV file with data
            output_dir: Directory for generated scripts
        """
        self.data_filename = data_filename
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_r_script(
        self,
        numeric_vars: List[str],
        categorical_vars: List[str],
        grouping_var: Optional[str] = None
    ) -> str:
        """
        Generate R analysis script with ggplot2 visualizations.
        
        Args:
            numeric_vars: List of numeric variable names
            categorical_vars: List of categorical variable names
            grouping_var: Optional grouping variable for comparisons
            
        Returns:
            R script as string
        """
        script = f"""# Analysis Script for LLM Simulation Survey Results
# Generated automatically by LLM Simulation Survey System
# Date: {{Sys.Date()}}

# ============================================================================
# SETUP
# ============================================================================

# Load required packages
if (!require("tidyverse")) install.packages("tidyverse")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("psych")) install.packages("psych")
if (!require("car")) install.packages("car")

library(tidyverse)
library(ggplot2)
library(psych)
library(car)

# Set working directory (adjust as needed)
# setwd("your/path/here")

# ============================================================================
# DATA LOADING
# ============================================================================

# Load the data
data <- read_csv("{self.data_filename}")

# Display structure
str(data)
summary(data)

# ============================================================================
# DATA PREPROCESSING
# ============================================================================

# Convert categorical variables to factors
categorical_vars <- c({', '.join(f'"{var}"' for var in categorical_vars)})
data <- data %>%
  mutate(across(all_of(categorical_vars), as.factor))

# Check for missing data
missing_summary <- data %>%
  summarise(across(everything(), ~sum(is.na(.))))
print(missing_summary)

# ============================================================================
# DESCRIPTIVE STATISTICS
# ============================================================================

# Overall descriptive statistics for numeric variables
numeric_vars <- c({', '.join(f'"{var}"' for var in numeric_vars)})
describe(data[numeric_vars])

"""
        
        if grouping_var:
            script += f"""
# Descriptive statistics by group
data %>%
  group_by({grouping_var}) %>%
  summarise(across(all_of(numeric_vars), 
                  list(mean = mean, sd = sd, min = min, max = max),
                  na.rm = TRUE))

"""
        
        script += """
# ============================================================================
# VISUALIZATIONS
# ============================================================================

"""
        
        # Add histograms for numeric variables
        for var in numeric_vars[:3]:  # Limit to first 3 to keep script reasonable
            script += f"""
# Histogram for {var}
ggplot(data, aes(x = {var})) +
  geom_histogram(binwidth = 1, fill = "steelblue", color = "black", alpha = 0.7) +
  theme_minimal() +
  labs(title = "Distribution of {var}",
       x = "{var}",
       y = "Frequency")
ggsave("histogram_{var}.png", width = 8, height = 6)

"""
        
        if grouping_var and numeric_vars:
            script += f"""
# Box plots by group
ggplot(data, aes(x = {grouping_var}, y = {numeric_vars[0]}, fill = {grouping_var})) +
  geom_boxplot(alpha = 0.7) +
  theme_minimal() +
  labs(title = "{numeric_vars[0]} by {grouping_var}",
       x = "{grouping_var}",
       y = "{numeric_vars[0]}")
ggsave("boxplot_{numeric_vars[0]}_by_{grouping_var}.png", width = 8, height = 6)

"""
        
        script += """
# ============================================================================
# INFERENTIAL STATISTICS
# ============================================================================

"""
        
        if grouping_var and numeric_vars:
            script += f"""
# Independent samples t-test (or ANOVA if >2 groups)
groups <- unique(data${grouping_var})

if (length(groups) == 2) {{
  # Two groups: t-test
  t_test_result <- t.test({numeric_vars[0]} ~ {grouping_var}, data = data)
  print(t_test_result)
  
  # Effect size (Cohen's d)
  library(effectsize)
  cohens_d({numeric_vars[0]} ~ {grouping_var}, data = data)
}} else if (length(groups) > 2) {{
  # More than two groups: ANOVA
  anova_result <- aov({numeric_vars[0]} ~ {grouping_var}, data = data)
  print(summary(anova_result))
  
  # Post-hoc tests
  print(TukeyHSD(anova_result))
  
  # Effect size (eta-squared)
  library(effectsize)
  eta_squared(anova_result)
}}

"""
        
        if len(numeric_vars) >= 2:
            script += f"""
# Correlation analysis
cor_matrix <- cor(data[numeric_vars], use = "pairwise.complete.obs")
print(cor_matrix)

# Correlation test for first two variables
cor.test(data${numeric_vars[0]}, data${numeric_vars[1]})

# Correlation heatmap
library(corrplot)
corrplot(cor_matrix, method = "color", type = "upper",
         addCoef.col = "black", tl.col = "black", tl.srt = 45)

"""
        
        script += """
# ============================================================================
# RELIABILITY ANALYSIS
# ============================================================================

# Cronbach's alpha for scale items (if applicable)
# Uncomment and adjust variables as needed
# alpha_result <- psych::alpha(data[c("item1", "item2", "item3")])
# print(alpha_result)

# ============================================================================
# EXPORT RESULTS
# ============================================================================

# Save cleaned data
write_csv(data, "cleaned_data.csv")

# Save summary statistics
sink("summary_statistics.txt")
print(summary(data))
sink()

cat("\\nAnalysis complete! Check the output files.\\n")
"""
        
        return script
    
    def generate_python_script(
        self,
        numeric_vars: List[str],
        categorical_vars: List[str],
        grouping_var: Optional[str] = None
    ) -> str:
        """
        Generate Python analysis script with seaborn/matplotlib visualizations.
        
        Args:
            numeric_vars: List of numeric variable names
            categorical_vars: List of categorical variable names
            grouping_var: Optional grouping variable for comparisons
            
        Returns:
            Python script as string
        """
        script = f'''"""
Analysis Script for LLM Simulation Survey Results
Generated automatically by LLM Simulation Survey System
"""

# ============================================================================
# IMPORTS
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set plot style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# ============================================================================
# DATA LOADING
# ============================================================================

# Load the data
data = pd.read_csv("{self.data_filename}")

# Display basic information
print("Dataset shape:", data.shape)
print("\\nColumn names and types:")
print(data.dtypes)
print("\\nFirst few rows:")
print(data.head())

# ============================================================================
# DATA PREPROCESSING
# ============================================================================

# Convert categorical variables
categorical_vars = {categorical_vars}
for var in categorical_vars:
    if var in data.columns:
        data[var] = data[var].astype('category')

# Check for missing data
print("\\nMissing data summary:")
print(data.isnull().sum())

# Define numeric variables
numeric_vars = {numeric_vars}

# ============================================================================
# DESCRIPTIVE STATISTICS
# ============================================================================

print("\\n" + "="*60)
print("DESCRIPTIVE STATISTICS")
print("="*60)

# Overall descriptive statistics
print("\\nOverall statistics:")
print(data[numeric_vars].describe())

'''
        
        if grouping_var:
            script += f'''
# Statistics by group
print(f"\\nStatistics by {{'{grouping_var}'}}:")
print(data.groupby('{grouping_var}')[numeric_vars].describe())

'''
        
        script += '''
# ============================================================================
# VISUALIZATIONS
# ============================================================================

print("\\nGenerating visualizations...")

'''
        
        # Add histograms
        for i, var in enumerate(numeric_vars[:3]):
            script += f'''
# Histogram for {var}
plt.figure(figsize=(10, 6))
plt.hist(data['{var}'].dropna(), bins=20, color='steelblue', edgecolor='black', alpha=0.7)
plt.xlabel('{var}')
plt.ylabel('Frequency')
plt.title('Distribution of {var}')
plt.grid(True, alpha=0.3)
plt.savefig('histogram_{var}.png', dpi=300, bbox_inches='tight')
plt.close()

'''
        
        if grouping_var and numeric_vars:
            script += f'''
# Box plot by group
plt.figure(figsize=(10, 6))
data.boxplot(column='{numeric_vars[0]}', by='{grouping_var}', ax=plt.gca())
plt.xlabel('{grouping_var}')
plt.ylabel('{numeric_vars[0]}')
plt.title(f'{numeric_vars[0]} by {grouping_var}')
plt.suptitle('')  # Remove default title
plt.savefig('boxplot_{numeric_vars[0]}_by_{grouping_var}.png', dpi=300, bbox_inches='tight')
plt.close()

'''
        
        if len(numeric_vars) >= 2:
            script += f'''
# Correlation heatmap
plt.figure(figsize=(10, 8))
correlation_matrix = data[numeric_vars].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={{"shrink": 0.8}})
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

'''
        
        script += '''
# ============================================================================
# INFERENTIAL STATISTICS
# ============================================================================

print("\\n" + "="*60)
print("INFERENTIAL STATISTICS")
print("="*60)

'''
        
        if grouping_var and numeric_vars:
            script += f'''
# Group comparison for {numeric_vars[0]}
groups = data.groupby('{grouping_var}')['{numeric_vars[0]}'].apply(list)
group_names = list(groups.index)

if len(group_names) == 2:
    # Two groups: t-test
    group1_data = groups[group_names[0]]
    group2_data = groups[group_names[1]]
    
    t_stat, p_value = stats.ttest_ind(group1_data, group2_data)
    
    # Cohen's d
    pooled_std = np.sqrt(((len(group1_data) - 1) * np.std(group1_data, ddof=1)**2 + 
                          (len(group2_data) - 1) * np.std(group2_data, ddof=1)**2) / 
                         (len(group1_data) + len(group2_data) - 2))
    cohens_d = (np.mean(group1_data) - np.mean(group2_data)) / pooled_std
    
    print(f"\\nIndependent t-test:")
    print(f"  t-statistic: {{t_stat:.4f}}")
    print(f"  p-value: {{p_value:.4f}}")
    print(f"  Cohen's d: {{cohens_d:.4f}}")
    
elif len(group_names) > 2:
    # More than two groups: ANOVA
    f_stat, p_value = stats.f_oneway(*groups)
    
    print(f"\\nOne-way ANOVA:")
    print(f"  F-statistic: {{f_stat:.4f}}")
    print(f"  p-value: {{p_value:.4f}}")

'''
        
        if len(numeric_vars) >= 2:
            script += f'''
# Correlation analysis
print("\\nCorrelation analysis:")
for i in range(len(numeric_vars)):
    for j in range(i+1, len(numeric_vars)):
        var1, var2 = numeric_vars[i], numeric_vars[j]
        clean_data = data[[var1, var2]].dropna()
        if len(clean_data) > 2:
            corr, p_val = stats.pearsonr(clean_data[var1], clean_data[var2])
            print(f"  {{var1}} vs {{var2}}: r = {{corr:.3f}}, p = {{p_val:.4f}}")

'''
        
        script += '''
# ============================================================================
# EXPORT RESULTS
# ============================================================================

# Save cleaned data
data.to_csv('cleaned_data.csv', index=False)

# Save summary to text file
with open('summary_statistics.txt', 'w') as f:
    f.write("SUMMARY STATISTICS\\n")
    f.write("="*60 + "\\n\\n")
    f.write(str(data[numeric_vars].describe()))

print("\\nAnalysis complete! Check the output files.")
'''
        
        return script
    
    def generate_spss_syntax(
        self,
        numeric_vars: List[str],
        categorical_vars: List[str],
        grouping_var: Optional[str] = None
    ) -> str:
        """
        Generate SPSS syntax file.
        
        Args:
            numeric_vars: List of numeric variable names
            categorical_vars: List of categorical variable names
            grouping_var: Optional grouping variable for comparisons
            
        Returns:
            SPSS syntax as string
        """
        syntax = f"""* Analysis Syntax for LLM Simulation Survey Results.
* Generated automatically by LLM Simulation Survey System.

* ============================================================================.
* DATA IMPORT.
* ============================================================================.

* Import CSV file.
GET DATA
  /TYPE=TXT
  /FILE="{self.data_filename}"
  /DELIMITERS=","
  /QUALIFIER='"'
  /ARRANGEMENT=DELIMITED
  /FIRSTCASE=2
  /VARIABLES=
    {' '.join(var + ' AUTO' for var in numeric_vars + categorical_vars)}.

EXECUTE.

* ============================================================================.
* DATA PREPROCESSING.
* ============================================================================.

* Set variable labels (customize as needed).
"""
        
        for var in numeric_vars + categorical_vars:
            syntax += f'VARIABLE LABELS {var} "{var}".\n'
        
        syntax += """
* Set measurement levels.
"""
        for var in numeric_vars:
            syntax += f'VARIABLE LEVEL {var} (SCALE).\n'
        
        for var in categorical_vars:
            syntax += f'VARIABLE LEVEL {var} (NOMINAL).\n'
        
        syntax += """
* Check for missing data.
FREQUENCIES VARIABLES=ALL
  /FORMAT=NOTABLE
  /STATISTICS=NONE
  /ORDER=ANALYSIS.

* ============================================================================.
* DESCRIPTIVE STATISTICS.
* ============================================================================.

* Descriptive statistics for numeric variables.
DESCRIPTIVES VARIABLES="""
        syntax += ' '.join(numeric_vars)
        syntax += """
  /STATISTICS=MEAN STDDEV MIN MAX.

"""
        
        if grouping_var:
            syntax += f"""
* Descriptive statistics by group.
MEANS TABLES={' '.join(numeric_vars)} BY {grouping_var}
  /CELLS=MEAN COUNT STDDEV MIN MAX.

"""
        
        syntax += """
* ============================================================================.
* VISUALIZATIONS.
* ============================================================================.

* Histograms for numeric variables.
"""
        for var in numeric_vars[:3]:
            syntax += f"""
GRAPH
  /HISTOGRAM={var}.

"""
        
        if grouping_var and numeric_vars:
            syntax += f"""
* Box plots by group.
GRAPH
  /BOXPLOT={numeric_vars[0]} BY {grouping_var}.

"""
        
        syntax += """
* ============================================================================.
* INFERENTIAL STATISTICS.
* ============================================================================.

"""
        
        if grouping_var and numeric_vars:
            syntax += f"""
* Independent samples t-test (for 2 groups) or ANOVA (for >2 groups).
* First, check number of groups.
FREQUENCIES VARIABLES={grouping_var}.

* T-test (if 2 groups).
T-TEST GROUPS={grouping_var}(1 2)
  /VARIABLES={numeric_vars[0]}
  /CRITERIA=CI(.95).

* One-way ANOVA (if >2 groups).
ONEWAY {numeric_vars[0]} BY {grouping_var}
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /POSTHOC=TUKEY ALPHA(0.05).

"""
        
        if len(numeric_vars) >= 2:
            syntax += f"""
* Correlation analysis.
CORRELATIONS
  /VARIABLES={' '.join(numeric_vars)}
  /PRINT=TWOTAIL NOSIG
  /STATISTICS DESCRIPTIVES
  /MISSING=PAIRWISE.

"""
        
        syntax += """
* ============================================================================.
* RELIABILITY ANALYSIS.
* ============================================================================.

* Cronbach's alpha (customize variable list).
* RELIABILITY
*   /VARIABLES=item1 item2 item3
*   /SCALE('ALL VARIABLES') ALL
*   /MODEL=ALPHA
*   /STATISTICS=DESCRIPTIVE SCALE CORR
*   /SUMMARY=TOTAL.

* ============================================================================.
* END OF SYNTAX.
* ============================================================================.
"""
        
        return syntax
    
    def save_script(self, script: str, filename: str) -> str:
        """
        Save generated script to file.
        
        Args:
            script: Script content
            filename: Output filename
            
        Returns:
            Full path to saved file
        """
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(script)
        return str(filepath)

