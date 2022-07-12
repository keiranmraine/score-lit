import streamlit as st
import pandas as pd
import plotly.express as px

COUNTRIES = 'https://raw.githubusercontent.com/google/dspl/db79dad685276dbf98ca44b875d1481bc240c5c1/samples/google/canonical/countries.csv'
MUSIC = 'data/music.csv'
COMPOSERS = 'data/composers.csv'

# @st.cache
def load_data():
    with st.spinner('Loading data files...'):
        music_df = pd.read_csv(MUSIC)
        composer_df = pd.read_csv(COMPOSERS)
        location_df = pd.read_csv(COUNTRIES)
    return music_df, composer_df, location_df

def raw_data(df_music, df_composer, df_loc):
    with st.expander("View raw music data"):
        st.table(df_music)
    left_c, right_c = st.columns(2)
    with left_c:
        with st.expander("View raw composer data"):
            st.table(df_composer)
    with right_c:
        with st.expander("View raw location data"):
            st.table(df_loc)

def process_composers(df_music, df_composer, df_loc):
    # unique composers
    uniq_composers = pd.Series(df_music['Composer'].unique(), name="Composer").sort_values()
    # join unique composers and composer_country data file
    composer_country = pd.merge(uniq_composers, df_composer, left_on='Composer', right_on='composer_or_artist')[['Composer','country']]
    # get the number of composers in each country
    c_counts = composer_country['country'].value_counts().reset_index()
    c_counts.columns = ['country', 'composers']  # relabel, it's odd
    ## composers without a country
    df_tmp = pd.merge(uniq_composers, df_composer, left_on='Composer', right_on='composer_or_artist', how="outer", indicator=True)
    no_country = pd.Series(df_tmp[df_tmp['_merge']=='left_only']['Composer'].unique(), name="Composer")
    # then we want to map this, so join the counts to the location data
    location_counts = pd.merge(c_counts, df_loc, left_on='country', right_on='name')
    location_counts.rename(columns=({"country_x": "country", "country_y": "country_code"}), inplace=True)
    return uniq_composers, no_country, location_counts

def plotly_maps(location_counts):
    # plotly - can control point size
    scatter_geo = px.scatter_geo(
        location_counts,
        lon="longitude",
        lat="latitude",
        size="composers",
        hover_name="country",
        hover_data={
            "country_code": True,
            "composers": True,
            "latitude": False,
            "longitude": False,
        },
        labels={
            "country_code": "Code",
            "composers": "Composers"
        },
        fitbounds="locations",
        projection="natural earth")

    scatter_mapbox = px.scatter_mapbox(
        location_counts,
        lon="longitude",
        lat="latitude",
        size="composers",
        hover_name="country",
        hover_data={
            "country_code": True,
            "composers": True,
            "latitude": False,
            "longitude": False,
        },
        labels={
            "country_code": "Code",
            "composers": "Composers"
        },
        zoom=1,
        color_discrete_sequence=["fuchsia"],
        )
    scatter_mapbox.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    scatter_mapbox.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return scatter_geo, scatter_mapbox

st.set_page_config(layout="wide")
st.title('Score-lit')

(df_music, df_composer, df_loc) = load_data()  # spinner
raw_data(df_music, df_composer, df_loc)  # data tables
(uniq_composers, no_country, location_counts) = process_composers(df_music, df_composer, df_loc)


if len(no_country) > 0:
    with st.expander(f"Composers with no country assigned ({len(no_country)})"):
        st.table(no_country)

matched_rows = df_music['Problematic']==1
if len(matched_rows):
    st.subheader("Problematic titles")
    st.table(df_music[matched_rows][['Composer', 'Title']])

sel_composer = st.selectbox(
    "Show music by:",
    pd.concat([pd.Series(["<select>"]), uniq_composers])
)
if sel_composer != "<select>":
    matched_rows = df_music['Composer']==sel_composer
    st.table(df_music[matched_rows])

(scatter_geo, scatter_mapbox) = plotly_maps(location_counts)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Number of composers per country")
    st.write(location_counts[['country','composers']])
with right_column:
    # better than base plotly map, but less control over points
    st.subheader("Builtin map")
    st.map(location_counts)


left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Plotly scatter_geo")
    st.plotly_chart(scatter_geo, use_container_width=True)
with right_column:
    st.subheader("Plotly scatter_mapbox - open-street-map",)
    st.plotly_chart(scatter_mapbox, use_container_width=True)


