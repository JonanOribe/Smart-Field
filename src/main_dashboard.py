import streamlit as st
import numpy as np
import pandas as pd
from main_utils import get_files_with_data
from configparser import ConfigParser
config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']

st.title('ALTAR data')

DATE_COLUMN = 'FECHA'
DATA_URL = get_files_with_data()

@st.cache
def load_data(nrows):
    data = pd.read_excel(data_path+'/'+DATA_URL[0], nrows=nrows, skiprows=1)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(20)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

humb_to_filter = st.slider('TCB', -40.0, 80.0,(25.0, 75.0))

filtered_data = data[data['TCB'] >= humb_to_filter[0]]
filtered_data = filtered_data[filtered_data['TCB'] <= humb_to_filter[1]]

st.subheader('TCB')
st.bar_chart(filtered_data)


