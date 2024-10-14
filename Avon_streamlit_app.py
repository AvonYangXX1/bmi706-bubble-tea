import pandas as pd
import geopandas as gpd
import plotly.express as px
import streamlit as st

# Load the dataset
def load_data():
    df_fnt = pd.read_csv('VIW_FNT.csv', low_memory=False)
    return df_fnt

# Fill missing values with zeros for numeric columns, assuming NaN means no detections
def clean_data(df):
    df_filled = df.fillna({
        'AH1N12009': 0, 'AH1': 0, 'AH3': 0, 'AH5': 0, 'AH7N9': 0, 'AOTHER_SUBTYPE': 0,
        'ANOTSUBTYPED': 0, 'ANOTSUBTYPABLE': 0, 'INF_A': 0, 'BVIC_2DEL': 0, 'BVIC_3DEL': 0,
        'BVIC_DELUNK': 0, 'BVIC_NODEL': 0, 'BYAM': 0, 'BNOTDETERMINED': 0, 'INF_B': 0,
        'INF_ALL': 0, 'INF_NEGATIVE': 0
    })
    
    # Remove rows where 'HEMISPHERE' is NaN
    df_filled = df_filled.dropna(subset=['HEMISPHERE'])
    
    return df_filled

# Filter data based on the year, week, selected regions, and virus subtype
def filter_data(df, year, week, selection_type, selection_value, subtype):
    # Filter by year and week
    df_filtered = df[(df['ISO_YEAR'] == year) & (df['ISO_WEEK'] == week)]
    
    if selection_type == 'Country':
        df_filtered = df_filtered[df_filtered['COUNTRY_AREA_TERRITORY'].isin(selection_value)]
    elif selection_type == 'Hemisphere':
        df_filtered = df_filtered[df_filtered['HEMISPHERE'].isin(selection_value)]
    elif selection_type == 'WHO Region':
        df_filtered = df_filtered[df_filtered['WHOREGION'].isin(selection_value)]
    
    return df_filtered

def create_choropleth(df_filtered, selected_year_week, subtype):
    # Load the world MAP using GeoPandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    merged_df = world.merge(df_filtered, how="left", left_on="iso_a3", right_on="COUNTRY_CODE")

    merged_df[subtype] = merged_df[subtype].fillna(0)
    fig = px.choropleth(merged_df,
                        geojson=merged_df.geometry,
                        locations=merged_df.index,
                        color=subtype,  # Display the count of positive samples for the selected subtype
                        hover_name="name",
                        hover_data=[subtype],
                        title=f"Positive Samples by {subtype} - {selected_year_week}",
                        labels={subtype: 'Positive Samples (Count)'},
                        color_continuous_scale="Blues")
    fig.update_geos(
        showcoastlines=True,     
        showframe=False,
        visible=True,
        projection_type="natural earth"
    )
    return fig

def create_streamlit_app():
    df_fnt = load_data()
    df_cleaned = clean_data(df_fnt)

    st.title("Visualization of Positive Influenza Samples by Region")
    selected_year = st.slider("Select Year", min_value=1999, max_value=2024, value=2014, step=1)
    selected_week = st.slider("Select Week", min_value=1, max_value=52, value=32, step=1)

    selection_type = st.radio(
        "Select Filter Type",
        options=["Country", "Hemisphere", "WHO Region"],
        index=0
    )

    default_countries = ['United States of America', 'Brazil', 'India', 'China', 'Japan','Italy']

    if selection_type == "Country":
        options = df_cleaned['COUNTRY_AREA_TERRITORY'].unique()
        selected_value = st.multiselect("Select Country/Region", options=options, default=default_countries)
    elif selection_type == "Hemisphere":
        options = df_cleaned['HEMISPHERE'].unique()
        selected_value = st.multiselect("Select Hemisphere", options=options, default=options)
    elif selection_type == "WHO Region":
        options = df_cleaned['WHOREGION'].unique()
        selected_value = st.multiselect("Select WHO Region", options=options, default=options)

    subtypes = ['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'AOTHER_SUBTYPE', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE', 
                'INF_A', 'BVIC_2DEL', 'BVIC_3DEL', 'BVIC_DELUNK', 'BVIC_NODEL', 'BYAM', 'BNOTDETERMINED', 
                'INF_B', 'INF_ALL', 'INF_NEGATIVE']
    default_subtype = subtypes.index('INF_B')

    selected_subtype = st.selectbox("Select Virus Subtype", options=subtypes, index=default_subtype)
    df_filtered = filter_data(df_cleaned, selected_year, selected_week, selection_type, selected_value, selected_subtype)

    fig = create_choropleth(df_filtered, f"{selected_year}-W{selected_week:02d}", selected_subtype)

    st.plotly_chart(fig)

    total_tested = df_filtered[selected_subtype].sum()

    st.metric(label=f"Positive Samples ({selected_subtype})", value=f"{total_tested:,}")
    st.metric(label="Total Samples Tested", value=f"{total_tested:,}")

# Run the app
if __name__ == "__main__":
    create_streamlit_app()
