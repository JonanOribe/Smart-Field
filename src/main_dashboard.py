import streamlit as st
import numpy as np
import pandas as pd
from main_utils import get_files_with_data
from configparser import ConfigParser
config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']

st.set_page_config(layout="wide")
st.title('ALTAR data')

DATE_COLUMN = 'FECHA'
DATA_URL = get_files_with_data()

col1, col2, col3= st.beta_columns((2,2,2))

@st.cache
def load_data(nrows):
    data = pd.read_excel(data_path+'/'+DATA_URL[0], nrows=nrows, skiprows=1)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(20)
data_load_state.text("Done! (using st.cache)")

sensor_errors=pd.read_csv("sensor_errors.csv").set_index('Error_Type')

if col1.checkbox('Show raw data'):
    col1.subheader('Raw data')
    col1.write(data)

if col2.checkbox('Show errors data'):
    grouped_data=sensor_errors.groupby(['Error_Type']).size()
    col2.subheader('Sensor´s errors data')
    col2.write(sensor_errors)
    col3.text("")
    col3.text("")
    col3.text("")
    col3.subheader('Grouped by error type')
    col3.bar_chart(grouped_data)

humb_to_filter = st.slider('TCB', -40.0, 80.0,(-25.0, 75.0))

filtered_data = data[data['TCB'] >= humb_to_filter[0]].set_index('FECHA')
filtered_data = filtered_data[filtered_data['TCB'] <= humb_to_filter[1]]

st.subheader('TCB')
st.line_chart(filtered_data)


