import streamlit as st
import pandas as pd
import plotly.express as px

# Load your VIW_FNT dataset
df = pd.read_csv("VIW_FNT.csv")

# Ensure the entire dataframe is treated as strings
df = df.astype(str)

# Streamlit sidebar widgets for filtering
year = st.sidebar.selectbox('Select Year', df['ISO_YEAR'].unique())
week = st.sidebar.selectbox('Select Week', df['ISO_WEEK'].unique())

# Filter the dataset based on selected year and week
filtered_df = df[(df['ISO_YEAR'] == year) & (df['ISO_WEEK'] == week)]

# Create the choropleth map using Plotly Express
fig = px.choropleth(
    filtered_df,
    locations="COUNTRY_CODE",  # This should be the column containing the ISO 3-letter country codes
    color="INF_ALL",  # Column to determine color intensity
    hover_name="COUNTRY_AREA_TERRITORY",  # Column for country names
    hover_data=["INF_ALL"],  # Other columns to show on hover
    title=f"Global Influenza Distribution for Year {year}, Week {week}",
    color_continuous_scale=px.colors.sequential.Plasma,  # You can adjust the color scale here
    projection="natural earth"  # This creates a global map projection
)

# Display the map in Streamlit
st.plotly_chart(fig, use_container_width=True)