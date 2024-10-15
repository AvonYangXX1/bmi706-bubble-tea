import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    #fid_df = pd.read_csv("VIW_FID.csv",low_memory=False,encoding = 'utf_8_sig')

    flu_df = pd.read_csv("VIW_FNT.csv",low_memory=False,encoding = 'utf_8_sig')

# Streamlit sidebar widgets for filtering
year = st.sidebar.selectbox('Select Year', df['ISO_YEAR'].unique())
week = st.sidebar.selectbox('Select Week', df['ISO_WEEK'].unique())

# Filter the dataset based on selected year and week
filtered_df = df[(df['ISO_YEAR'] == year) & (df['ISO_WEEK'] == week)]

    # a new df
    new_df_flu = flu_df[id_vars+influenza_a_types+influenza_b_types+statistics]

    # select the data with spec_processed_nb not na or 0
    new_df_flu = new_df_flu.dropna(subset=['SPEC_PROCESSED_NB'],axis=0)
    new_df_flu = new_df_flu[new_df_flu['SPEC_PROCESSED_NB']!=0]

    # fill na
    new_df_flu[influenza_a_types+influenza_b_types] = new_df_flu[influenza_a_types+influenza_b_types].fillna(0)
    new_df_flu['INF_A'] = new_df_flu['INF_A'].fillna(new_df_flu[influenza_a_types].sum(axis=1))
    new_df_flu['INF_B'] = new_df_flu['INF_B'].fillna(new_df_flu[influenza_b_types].sum(axis=1))
    new_df_flu['INF_ALL'] = new_df_flu['INF_ALL'].fillna(new_df_flu[['INF_A','INF_B']].sum(axis=1))

    # filter some problematic rows with positive rate > 100% or with errors in calculation of INF_ALL
    for flu_type in influenza_a_types + influenza_b_types + ['INF_A', 'INF_B', 'INF_ALL']:
        condition = new_df_flu[flu_type] > new_df_flu['SPEC_PROCESSED_NB']
        new_df_flu = new_df_flu[~condition]

    for flu_type in influenza_a_types:
        condition = new_df_flu[flu_type] > new_df_flu['INF_A']
        new_df_flu = new_df_flu[~condition]

    for flu_type in influenza_b_types:
        condition = new_df_flu[flu_type] > new_df_flu['INF_B']
        new_df_flu = new_df_flu[~condition]

    condition = new_df_flu['INF_A']+new_df_flu['INF_B'] != new_df_flu['INF_ALL']
    new_df_flu = new_df_flu[~condition]

    # calculate positive rate
    new_df_flu_positive = pd.DataFrame(index=new_df_flu.index)
    for col in influenza_a_types+influenza_b_types+statistics:
        new_df_flu_positive[col] = new_df_flu[col] / new_df_flu['SPEC_PROCESSED_NB']
    
    # melt df
    melted_counts = new_df_flu.melt(id_vars=id_vars,var_name='subtype', value_name='count', 
                            value_vars=influenza_a_types+influenza_b_types+statistics)

    melted_positive_rates = new_df_flu_positive.melt(var_name='subtype', value_name='positive_rate', 
                                    value_vars=influenza_a_types+influenza_b_types+statistics)
    
    melted_new_df = melted_counts.copy()
    melted_new_df['positive_rate'] = melted_positive_rates['positive_rate']

    return flu_df, melted_new_df

# define some variables
influenza_a_types = ['AH1N12009','AH1','AH3','AH5','AH7N9','ANOTSUBTYPED','ANOTSUBTYPABLE','AOTHER_SUBTYPE']
influenza_b_types = ['BVIC_2DEL','BVIC_3DEL','BVIC_NODEL','BVIC_DELUNK','BYAM','BNOTDETERMINED']
statistics = ['SPEC_PROCESSED_NB','INF_A','INF_B','INF_ALL']
# non_influenza_respiratory_virus_types = ['ADENO','BOCA','HUMAN_CORONA','METAPNEUMO','PARAINFLUENZA','RHINO','RSV','OTHERRESPVIRUS']
id_vars = ['WHOREGION','FLUSEASON','HEMISPHERE','ITZ','COUNTRY_CODE','COUNTRY_AREA_TERRITORY','ISO_WEEKSTARTDATE', 'ISO_YEAR', 'ISO_WEEK']

flu_df, melted_new_df = load_data()



## vis 3
# year slider
year = st.slider('Year',min_value=flu_df['ISO_YEAR'].min(),max_value=flu_df['ISO_YEAR'].max(),value=2012)

# checkbox of "select all" for multiselection of WHO region
region_list = flu_df['WHOREGION'].dropna().unique()
all_options_who_region = st.checkbox("Select all options for WHO Region",value=True)
container_who_region = st.container()
if all_options_who_region:
    who_region = container_who_region.multiselect("WHO Region",
         region_list,region_list)
else:
    who_region = container_who_region.multiselect("WHO Region",
        region_list)

# multiselect of subtypes
subtype_list = influenza_a_types + influenza_b_types + ['INF_A','INF_B','INF_ALL']
subtype = st.multiselect('Subtype',subtype_list,default=['AH1N12009'])

filtered_melted_new_df = melted_new_df[(melted_new_df['ISO_YEAR']==year) & (melted_new_df['WHOREGION'].isin(who_region)) & (melted_new_df['subtype'].isin(subtype))]
# plot: use week start date to plot
filtered_melted_new_df['ISO_WEEKSTARTDATE'] = pd.to_datetime(filtered_melted_new_df['ISO_WEEKSTARTDATE'])
chart = alt.Chart(filtered_melted_new_df).mark_line().encode(
     x=alt.X(
         'yearweek(ISO_WEEKSTARTDATE):T',
         title='Year',
         axis=alt.Axis(
             format='%Y', 
             tickCount='year',
             labelAngle=0
         )
     ),
     y=alt.Y('count:Q', title='Count')
 ).properties(
     width=800,
     height=400,
     title='Data Points by Year'
)

st.altair_chart(chart, use_container_width=True)

#以上为一些可供使用的template
#以下为上次的作业部分
# ### P2.2 ###
# # replace with st.radio
# sex = st.radio('Sex',['M','F'])
# ### P2.2 ###


# ### P2.3 ###
# # replace with st.multiselect
# # (hint: can use current hard-coded values below as as `default` for selector)
# countries = st.multiselect('Countries',df["Country"].unique(),default=[
#     "Austria",
#     "Germany",
#     "Iceland",
#     "Spain",
#     "Sweden",
#     "Thailand",
#     "Turkey",
# ])
# ### P2.3 ###


# ### P2.4 ###
# # replace with st.selectbox
# cancer = st.selectbox('Cancer',df['Cancer'].unique())
# ### P2.4 ###


# ### P2.5 ###
# ages = [
#     "Age <5",
#     "Age 5-14",
#     "Age 15-24",
#     "Age 25-34",
#     "Age 35-44",
#     "Age 45-54",
#     "Age 55-64",
#     "Age >64",
# ]

# filtered_df = df[(df['Year']==year) & (df['Sex']==sex) & (df['Country'].isin(countries)) & (df['Cancer']==cancer)]

# del df

# brush = alt.selection_interval(encodings=['x'],name='select_age')

# chart = (alt.Chart().mark_rect().encode(
#     x=alt.X("Age", sort=ages),
#     y=alt.Y("Country"),
#     color=alt.Color('Rate:Q',
#                     scale=alt.Scale(type='log', domain=[0.01,1000], 
#                     clamp=True, 
#                     scheme="blues",reverse=True),
#                     title='Mortality rate per 100k',
#                     ),
#     tooltip=["Rate:Q"],
# ).properties(
#     title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
# ).add_params(brush))

# pop = (alt.Chart().mark_bar().encode(
#     x=alt.X('sum(Pop):Q'),
#     y=alt.Y('Country:N',sort='-x'),
#     color=alt.value("#87CEFA"),
#     tooltip=[alt.Tooltip("sum(Pop):Q"),
#         alt.Tooltip("Country:N")]
# ).transform_filter(brush))

# combined = alt.vconcat(chart, pop, data=filtered_df)

# ### P2.5 ###

# st.altair_chart(combined, use_container_width=True)


# countries_in_subset = filtered_df["Country"].unique()
# if len(countries_in_subset) != len(countries):
#      if len(countries_in_subset) == 0:
#          st.write("No data avaiable for given subset.")
#      else:
#          missing = set(countries) - set(countries_in_subset)
#          st.write("No data available for " + ", ".join(missing) + ".")
