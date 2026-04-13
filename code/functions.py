import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import chi2_contingency
from scipy.stats import mannwhitneyu
from statsmodels.stats.outliers_influence import variance_inflation_factor
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
    summary = df.describe(include='all').T  # include='all' handles strings too
    summary['missing_pct'] = (df.isnull().sum() / len(df)) * 100

    # Correlation Matrix (Numerical Only)
    num_df = df.select_dtypes(include=['number'])
    
    if not num_df.empty:
        corr_matrix = num_df.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Matrix")
        plt.show()

        # VIF Calculation
        X = num_df.dropna().astype(float) 
        if X.shape[1] > 1: # VIF needs at least 2 columns
            vif_data = pd.DataFrame()
            vif_data["feature"] = X.columns
            vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
        else:
            print("\nNot enough numerical columns for VIF.")
    else:
        print("\nNo numerical columns found for Correlation/VIF.")
    
    return df.info(), df.nunique(), summary, vif_data.sort_values(by="VIF", ascending=False) 

def convert_snake_case(df):
    '''function to convert names in a dataframe to snake case'''
    df.columns = (df.columns
        .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True) # Handle CamelCase
        .str.replace(r'\W+', '_', regex=True)               # Replace non-alphanumeric
        .str.lower()
        .str.strip('_'))
    return df
