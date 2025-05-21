import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import sys

# Add the src directory to the path to be able to import from there if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import utility functions from utils.py
from utils import load_data, process_data, create_boxplot, create_table

# Set page config
st.set_page_config(
    page_title="Solar Potential Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve the appearance
st.markdown("""
<style>
.main {
    padding: 2rem;
}
.stPlot {
    margin-top: 1rem;
}
h1, h2, h3 {
    margin-bottom: 1rem;
}
.stDataFrame {
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("☀️ Solar Potential Analysis Dashboard")
st.markdown("### Interactive Visualization of Solar Data Across Countries")

# Sidebar with country selection and other options
st.sidebar.header("Dashboard Controls")

# Function to load data
@st.cache_data
def load_country_data(country):
    """Load and return the data for a specific country"""
    file_path = f"data/{country}_clean.csv"
    try:
        df = pd.read_csv(file_path)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        # Add Country column
        df['Country'] = country.capitalize()
        return df
    except Exception as e:
        st.error(f"Error loading data for {country}: {e}")
        return None

# Country selection
available_countries = ["benin", "sierraleone", "togo"]
default_countries = available_countries.copy()
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=available_countries,
    default=default_countries
)

# Load data for selected countries
country_data = {}
combined_df = pd.DataFrame()

if selected_countries:
    for country in selected_countries:
        df = load_country_data(country)
        if df is not None:
            country_data[country] = df
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    if not combined_df.empty:
        # Convert timestamp to date for easier aggregation
        combined_df['Date'] = combined_df['Timestamp'].dt.date
        
        # Sidebar controls for data analysis
        metric_options = ["GHI", "DNI", "DHI"]
        selected_metric = st.sidebar.selectbox("Select Metric", options=metric_options, index=0)
        
        # Temporal aggregation options
        aggregation_options = ["None", "Daily", "Monthly"]
        selected_aggregation = st.sidebar.selectbox("Temporal Aggregation", options=aggregation_options, index=1)
        
        # Main dashboard layout with three columns
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("📊 Metric Distribution by Country")
            
            if selected_aggregation == "None":
                # Create boxplot for raw data
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.boxplot(x='Country', y=selected_metric, data=combined_df, ax=ax)
                st.pyplot(fig)
            else:
                # Aggregate data based on selection
                if selected_aggregation == "Daily":
                    agg_df = combined_df.groupby(['Country', 'Date'])[selected_metric].mean().reset_index()
                elif selected_aggregation == "Monthly":
                    combined_df['Month'] = combined_df['Timestamp'].dt.to_period('M')
                    agg_df = combined_df.groupby(['Country', 'Month'])[selected_metric].mean().reset_index()
                
                # Create boxplot for aggregated data
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.boxplot(x='Country', y=selected_metric, data=agg_df, ax=ax)
                st.pyplot(fig)
        
        with col2:
            st.header("📈 Time Series Analysis")
            
            # Time series plot
            if selected_aggregation == "None":
                # Sample data for better visualization if raw data is used
                sample_size = 1000  # Adjust based on performance
                sampled_df = combined_df.sample(n=min(sample_size, len(combined_df)))
                plot_df = sampled_df.sort_values('Timestamp')
            elif selected_aggregation == "Daily":
                plot_df = combined_df.groupby(['Country', 'Date'])[selected_metric].mean().reset_index()
                plot_df = plot_df.sort_values('Date')
            elif selected_aggregation == "Monthly":
                combined_df['Month'] = combined_df['Timestamp'].dt.to_period('M')
                plot_df = combined_df.groupby(['Country', 'Month'])[selected_metric].mean().reset_index()
                plot_df['Month'] = plot_df['Month'].astype(str)
                plot_df = plot_df.sort_values('Month')
            
            # Create line plot
            fig, ax = plt.subplots(figsize=(10, 6))
            for country in selected_countries:
                country_df = plot_df[plot_df['Country'] == country.capitalize()]
                if selected_aggregation == "None":
                    ax.scatter(country_df['Timestamp'], country_df[selected_metric], label=country.capitalize(), alpha=0.5, s=10)
                elif selected_aggregation == "Daily":
                    ax.plot(country_df['Date'], country_df[selected_metric], label=country.capitalize())
                elif selected_aggregation == "Monthly":
                    ax.plot(country_df['Month'], country_df[selected_metric], label=country.capitalize(), marker='o')
            
            ax.set_xlabel('Time')
            ax.set_ylabel(f'{selected_metric} (W/m²)')
            ax.set_title(f'{selected_metric} Over Time by Country')
            if selected_aggregation != "None":
                plt.xticks(rotation=45)
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)
        
        # Statistical Comparison Section
        st.header("📊 Statistical Comparison")
        
        # Statistical tests if multiple countries are selected
        if len(selected_countries) > 1:
            st.subheader(f"Statistical Tests for {selected_metric}")
            
            # Prepare data for statistical tests
            data_for_test = []
            country_names = []
            
            for country in selected_countries:
                if country in country_data:
                    df = country_data[country]
                    if selected_aggregation == "None":
                        values = df[selected_metric].dropna().values
                    elif selected_aggregation == "Daily":
                        daily_avg = df.groupby(df['Timestamp'].dt.date)[selected_metric].mean()
                        values = daily_avg.values
                    elif selected_aggregation == "Monthly":
                        df['Month'] = df['Timestamp'].dt.to_period('M')
                        monthly_avg = df.groupby('Month')[selected_metric].mean()
                        values = monthly_avg.values
                    
                    data_for_test.append(values)
                    country_names.append(country.capitalize())
            
            # Kruskal-Wallis test for more than 2 groups
            if len(data_for_test) > 2:
                try:
                    stat, p_value = stats.kruskal(*data_for_test)
                    st.write(f"**Kruskal-Wallis Test (Overall Comparison):**")
                    st.write(f"p-value: {p_value:.6f}")
                    if p_value < 0.05:
                        st.write("➡️ There is a statistically significant difference between at least two countries.")
                    else:
                        st.write("➡️ No statistically significant difference detected between countries.")
                except Exception as e:
                    st.error(f"Error performing Kruskal-Wallis test: {e}")
            
            # Pairwise Mann-Whitney U tests
            st.write("**Pairwise Comparisons (Mann-Whitney U test):**")
            for i in range(len(data_for_test)):
                for j in range(i+1, len(data_for_test)):
                    try:
                        stat, p_value = stats.mannwhitneyu(data_for_test[i], data_for_test[j], alternative='two-sided')
                        result = f"{country_names[i]} vs {country_names[j]}: p-value = {p_value:.6f}"
                        if p_value < 0.05:
                            result += " (Significant difference)"
                        else:
                            result += " (No significant difference)"
                        st.write(result)
                    except Exception as e:
                        st.error(f"Error comparing {country_names[i]} and {country_names[j]}: {e}")
        
        # Top Regions Table
        st.header("📋 Top Regions Analysis")
        
        # Create a table showing top average values by region/time
        if selected_aggregation == "Daily":
            top_df = combined_df.groupby(['Country', 'Date'])[selected_metric].mean().reset_index()
            top_df = top_df.sort_values(by=selected_metric, ascending=False).head(10)
            st.write(f"Top 10 Days with Highest {selected_metric} Values")
            st.dataframe(top_df)
        elif selected_aggregation == "Monthly":
            combined_df['Month'] = combined_df['Timestamp'].dt.to_period('M')
            top_df = combined_df.groupby(['Country', 'Month'])[selected_metric].mean().reset_index()
            top_df = top_df.sort_values(by=selected_metric, ascending=False).head(10)
            top_df['Month'] = top_df['Month'].astype(str)
            st.write(f"Top 10 Months with Highest {selected_metric} Values")
            st.dataframe(top_df)
        else:
            # For raw data, we can sample or aggregate by some other dimension
            sampled_df = combined_df.sample(n=min(10000, len(combined_df)))
            top_values = sampled_df.nlargest(10, selected_metric)
            st.write(f"Sample of Top {selected_metric} Measurements")
            st.dataframe(top_values[['Country', 'Timestamp', selected_metric]])
else:
    st.warning("Please select at least one country to display data.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This dashboard visualizes solar potential data across different countries. "
    "Use the controls to explore the data and gain insights into solar energy potential."
)
st.sidebar.markdown("### Instructions")
st.sidebar.info(
    "1. Select one or more countries\n"
    "2. Choose a metric (GHI, DNI, DHI)\n"
    "3. Select temporal aggregation level\n"
    "4. Explore the visualizations and statistics"
)
