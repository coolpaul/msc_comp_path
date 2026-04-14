import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import chi2_contingency
from scipy.stats import mannwhitneyu
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score, fbeta_score
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import SplineTransformer
from great_tables import GT, style, loc
from IPython.display import display
from plotnine import ggplot, aes, geom_boxplot, theme_minimal, labs, theme, element_text, scale_fill_manual

def describe_dataframe(df):
    """
    Comprehensive diagnostic tool for DataFrames.
    Calculates stats, plots correlations, and prints VIF results internally.
    """
    
    # Basic Info & Summary Stats 
    print("\n" + "="*40)
    print("        DATAFRAME STRUCTURE")
    print("="*40)
    df.info()
    
    uniques = df.nunique()
    summary = df.describe(include='all').T
    # Calculate missing percentage per column
    missing_pcts = (df.isnull().sum() / len(df)) * 100
    # Use .map() or direct assignment to ensure indices match correctly
    summary['missing_pct'] = summary.index.map(missing_pcts)
    
    # Numerical Data
    num_df = df.select_dtypes(include=['number'])
    vif_result = None
    
    print("\n" + "="*40)
    print("      NUMERICAL RELATIONSHIPS")
    print("="*40)
    
    if num_df.shape[1] >= 2:
        # Plotting Heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(num_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Matrix")
        plt.show()

        # Calculating VIF
        vif_input = num_df.dropna().astype(float)
        
        if not vif_input.empty and vif_input.shape[1] > 1:
            X = add_constant(vif_input)
            
            # Calculate VIF for each column EXCEPT the constant
            vif_list = []
            for i in range(1, X.shape[1]):
                vif_val = variance_inflation_factor(X.values, i)
                vif_list.append({"feature": X.columns[i], "VIF": vif_val})
            
            # Create DataFrame from the list of dictionaries
            vif_result = pd.DataFrame(vif_list).sort_values(by="VIF", ascending=False)
            print("\nVariance Inflation Factor (VIF):")
            print(vif_result.to_string(index=False))
            
    elif num_df.shape[1] == 1:
        print(f"Only one numerical column detected: '{num_df.columns[0]}'.")
        print("Correlation and VIF require at least two numerical columns.")
    else:
        print("No numerical columns found for analysis.")

    # Return objects for further use
    return {
        "uniques": uniques,
        "summary": summary,
        "vif": vif_result
    }

def convert_snake_case(df):
    '''function to convert names in a dataframe to snake case'''
    df.columns = (df.columns
        .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True) # Handle camelCase
        .str.replace(r'\W+', '_', regex=True)               # Replace non-alphanumeric
        .str.lower()
        .str.strip('_'))
    return df
