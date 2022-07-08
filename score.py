import streamlit as st
import pandas as pd

st.title('Score-lit')

@st.cache
def load_data(nrows):
    data = pd.read_csv("data/music.csv", nrows=nrows)
    return data

data_load_state = st.text('Loading data...')
# Load n rows of data into the dataframe.
data = load_data(10)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

with st.expander("View Raw Data"):
    st.write(data)

c_counts = data['Composer'].value_counts()

st.subheader('Composer instances')
left_column, right_column = st.columns(2)
with left_column:
    st.write(c_counts)
with right_column:
    st.bar_chart(c_counts)