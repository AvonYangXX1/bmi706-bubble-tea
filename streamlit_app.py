import altair as alt # type: ignore
import pandas as pd # type: ignore
import streamlit as st # type: ignore

@st.cache_data
def load_data():
    fid_df = pd.read_csv("VIW_FID.csv",low_memory=False,encoding = 'utf_8_sig')

    flu_df = pd.read_csv("VIW_FNT - VIW_FNT.csv",low_memory=False,encoding = 'utf_8_sig')
    flu_df = flu_df.dropna(subset=['FLUSEASON','ISOYW'],axis=0)
    flu_df.loc[flu_df['ISOYW']=='MK','ISO2'] = 'MK'
    flu_df.loc[flu_df['ISOYW']=='MK','ISOYW'] = flu_df.loc[flu_df['ISOYW']=='MK','MMWRYW']
    flu_df = flu_df.astype({'ISOYW': 'float64'})

    return fid_df, flu_df


fid_df, flu_df = load_data()



## vis 3
year = st.slider('Year',min_value=flu_df['ISO_YEAR'].min(),max_value=flu_df['ISO_YEAR'].max(),value=2012)

all_options_who_region = st.checkbox("Select all options for WHO Region",value=True)

container_who_region = st.container()
 
if all_options_who_region:
    who_region = container_who_region.multiselect("WHO Region",
         flu_df['WHOREGION'].dropna().unique(),flu_df['WHOREGION'].dropna().unique())
else:
    who_region = container_who_region.multiselect("WHO Region",
        flu_df['WHOREGION'].dropna().unique())

##influenza_a_types = ['AH1N12009','AH1','AH3','AH5']

#flu_df_melted_influ_subtypes = 
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
