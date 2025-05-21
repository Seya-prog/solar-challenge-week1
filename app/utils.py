import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, List, Tuple, Optional

def load_data(country: str) -> pd.DataFrame:
    """
    Load data for a specific country from the data directory.
    
    Args:
        country: Name of the country (lowercase)
        
    Returns:
        DataFrame with the country's data
    """
    file_path = f"../data/{country}_clean.csv"
    try:
        df = pd.read_csv(file_path)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        # Add Country column 
        df['Country'] = country.capitalize()
        return df
    except Exception as e:
        print(f"Error loading data for {country}: {e}")
        return pd.DataFrame()

def process_data(dfs: Dict[str, pd.DataFrame], metric: str, aggregation: str) -> pd.DataFrame:
    """
    Process and combine data from multiple countries.
    
    Args:
        dfs: Dictionary mapping country names to their DataFrames
        metric: Metric to analyze (GHI, DNI, DHI)
        aggregation: Type of temporal aggregation (None, Daily, Monthly)
        
    Returns:
        Combined and processed DataFrame
    """
    combined_df = pd.DataFrame()
    
    for country, df in dfs.items():
        if not df.empty:
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    if combined_df.empty:
        return combined_df
    
    # Add date column for aggregation
    combined_df['Date'] = combined_df['Timestamp'].dt.date
    
    # Apply aggregation if needed
    if aggregation == "Daily":
        agg_df = combined_df.groupby(['Country', 'Date'])[metric].mean().reset_index()
        return agg_df
    elif aggregation == "Monthly":
        combined_df['Month'] = combined_df['Timestamp'].dt.to_period('M')
        agg_df = combined_df.groupby(['Country', 'Month'])[metric].mean().reset_index()
        agg_df['Month'] = agg_df['Month'].astype(str)
        return agg_df
    else:
        return combined_df

def create_boxplot(df: pd.DataFrame, metric: str) -> plt.Figure:
    """
    Create a boxplot visualization for the given metric.
    
    Args:
        df: DataFrame containing the data
        metric: Metric to visualize
        
    Returns:
        Matplotlib figure with the boxplot
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Country', y=metric, data=df, ax=ax)
    ax.set_title(f'{metric} Distribution by Country')
    ax.set_ylabel(f'{metric} (W/m²)')
    plt.tight_layout()
    return fig

def create_table(df: pd.DataFrame, metric: str, aggregation: str, n: int = 10) -> pd.DataFrame:
    """
    Create a table of top values for the selected metric.
    
    Args:
        df: DataFrame containing the data
        metric: Metric to analyze
        aggregation: Type of temporal aggregation
        n: Number of top values to include
        
    Returns:
        DataFrame with the top n values
    """
    if aggregation == "Daily":
        top_df = df.groupby(['Country', 'Date'])[metric].mean().reset_index()
        top_df = top_df.sort_values(by=metric, ascending=False).head(n)
        return top_df
    elif aggregation == "Monthly":
        if 'Month' not in df.columns:
            df['Month'] = df['Timestamp'].dt.to_period('M')
        top_df = df.groupby(['Country', 'Month'])[metric].mean().reset_index()
        top_df = top_df.sort_values(by=metric, ascending=False).head(n)
        top_df['Month'] = top_df['Month'].astype(str)
        return top_df
    else:
        # For raw data, sample or take top n values
        return df.nlargest(n, metric)
