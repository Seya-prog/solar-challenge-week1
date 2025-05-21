# Solar Potential Analysis Dashboard

## Overview
This interactive Streamlit dashboard visualizes solar potential data across different countries, focusing on metrics like GHI (Global Horizontal Irradiance), DNI (Direct Normal Irradiance), and DHI (Diffuse Horizontal Irradiance).

## Features
- **Country Selection**: Choose one or more countries to analyze
- **Metric Selection**: Switch between different solar metrics (GHI, DNI, DHI)
- **Interactive Elements**: Sliders and dropdown menus for customizing the visualizations
- **Statistical Analysis**: Comparison between countries with statistical tests
- **Visual Appeal**: Clean, professional design with intuitive navigation

## How to Run
1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```
   cd solar-challenge-week1
   streamlit run app/main.py
   ```

3. Access the dashboard in your web browser at the URL provided by Streamlit (typically http://localhost:8501)

## Dashboard Structure
- `app/main.py`: Main Streamlit application script
- `app/utils.py`: Utility functions for data processing and visualization

## User Guide
1. Use the sidebar to select countries and metrics
2. Explore the visualizations in the main panel
3. Adjust the temporal aggregation for different time-scale analyses
4. Check the statistical comparison section for quantitative insights

## Deployment
This dashboard can be deployed to Streamlit Community Cloud for public access.
