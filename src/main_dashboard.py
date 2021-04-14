import streamlit as st
import numpy as np
import pandas as pd
from main_utils import get_files_with_data
from configparser import ConfigParser
config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']

st.title('ALTAR data')

DATE_COLUMN = 'fecha'
DATA_URL = get_files_with_data()

@st.cache
def load_data(nrows):
    data = pd.read_excel(data_path+'/'+DATA_URL[0], nrows=nrows, skiprows=1)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    print(data.columns)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
