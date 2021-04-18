import streamlit as st
import numpy as np
import pandas as pd
import json
from main_utils import get_files_with_data,dendrometer_and_battery_cleaner,get_predictions_from_saved_model
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']
TARGET = config['DEFAULT']['target']
PREDICTION_FORMAT_EXAMPLE={
   "TCB":"35.2500",
   "HUMB":"21.2000",
   "SOILT":"21.2200",
   "SOIL1":"267.3500",
   "SOIL2":"171.7700",
   "SOIL3":"126.9200",
   "PAR":"1996.1100",
   "TD":"49020",
   "ANE":"5.2800",
   "WV":"10",
   "PLV":"309.0300"
}

st.set_page_config(layout="wide")
st.title('ALTAR data')

DATE_COLUMN = 'FECHA'
DATA_URL = get_files_with_data()

col1, col2, col3= st.beta_columns((2,1,1))

data = pd.read_excel(data_path+'/'+DATA_URL[0], skiprows=1)
data = data[data['TD'].notna()]
data.drop(['BAT'], axis=1, inplace=True)
data=data.head(500)

sensor_errors=pd.read_csv("sensor_errors.csv").set_index('Error_Type')

col1.subheader('Raw data')
col1.write(data)

grouped_data=sensor_errors.groupby(['Error_Type']).size()
col2.subheader('Sensor´s errors data')
col2.write(sensor_errors)
col3.subheader('Grouped by error type')
col3.bar_chart(grouped_data)

data.drop(['TD','PAR','PLV','WV'], axis=1, inplace=True)
humb_to_filter = st.slider('TCB', float(data['TCB'].min()), float(data['TCB'].max()),(float(data['TCB'].min()), float(data['TCB'].max())))

filtered_data = data[data['TCB'] >= humb_to_filter[0]].set_index('FECHA')
filtered_data = filtered_data[filtered_data['TCB'] <= humb_to_filter[1]]

st.subheader('TCB')
st.line_chart(filtered_data)

user_input = json.loads(st.text_input("Insert new values for prediction:", PREDICTION_FORMAT_EXAMPLE).replace("\'", "\""))
submit = st.button('Launch predictor for '+TARGET)
if submit:
    result=get_predictions_from_saved_model(user_input)
    st.subheader('Predicted value: '+str(result))
