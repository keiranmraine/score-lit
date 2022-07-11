import streamlit as st
import pandas as pd
import plotly.express as px

COUNTRIES = 'https://raw.githubusercontent.com/google/dspl/db79dad685276dbf98ca44b875d1481bc240c5c1/samples/google/canonical/countries.csv'
MUSIC = 'data/music.csv'
COMPOSERS = 'data/composers.csv'

st.set_page_config(layout="wide")
st.title('Score-lit')

@st.cache
def load_data():
    music_df = pd.read_csv(MUSIC)
    composer_df = pd.read_csv(COMPOSERS)
    location_df = pd.read_csv(COUNTRIES)
    return music_df, composer_df, location_df

data_load_state = st.text('Loading data...')
# Load n rows of data into the dataframe.
(df_music, df_composer, df_loc) = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

left_column, right_column = st.columns(2)
with left_column:
    with st.expander("View raw country data"):
        st.write(df_loc)

with right_column:
    with st.expander("View raw music data"):
        st.write(df_music)


composer_country = pd.merge(df_music[['Composer','Title']], df_composer, left_on='Composer', right_on='composer_or_artist')[['Composer','country']]
c_counts = composer_country['country'].value_counts().reset_index()
c_counts.columns = ['country', 'composers']

st.write("Need to add a list of composers without country")

# then we want to map this, so join the counts to the location data
location_counts = pd.merge(c_counts, df_loc, left_on='country', right_on='name')
location_counts.rename(columns=({"country_x": "country", "country_y": "country_code"}), inplace=True)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Number of composers per country")
    st.write(location_counts)
with right_column:
    # better than base plotly map, but less control over points
    st.subheader("Builtin map")
    st.map(location_counts)


# plotly - can control point size
fig = px.scatter_geo(
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

figb = px.scatter_mapbox(
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
    zoom=0,
    color_discrete_sequence=["fuchsia"],
    )
figb.update_layout(
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
figb.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Plotly scatter_geo")
    st.plotly_chart(fig, use_container_width=True)
with right_column:
    st.subheader("Plotly scatter_mapbox - open-street-map",)
    st.plotly_chart(figb, use_container_width=True)


