import streamlit as st
import numpy as np
import pandas as pd
import json
import pydeck as pdk
from PIL import Image
from main_utils import get_files_with_data,dendrometer_and_battery_cleaner,get_predictions_from_saved_model
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')

DATA_PATH = config['DEFAULT']['data_path']
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
   "WV_0":"0",
   "WV_1":"0",
   "WV_2":"0",
   "WV_3":"0",
   "WV_4":"0",
   "WV_5":"0",
   "WV_6":"0",
   "WV_7":"0",
   "WV_8":"0",
   "WV_9":"0",
   "WV_10":"1",
   "WV_11":"0",
   "WV_12":"0",
   "WV_13":"0",
   "WV_14":"0",
   "WV_15":"0",
   "PLV":"309.0300"
}

st.set_page_config(layout="wide")
img = Image.open('./statics/Smart Field.png')
st.image(img)

sensors_location=pd.read_csv("./data/sensors_positions.csv")
df = pd.DataFrame(data=sensors_location)
layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        pickable=True,
        opacity=0.6,
        filled=True,
        radius_scale=2,
        radius_min_pixels=10,
        radius_max_pixels=500,
        line_width_min_pixels=0.01,
        get_position='[Longitude, Latitude]',
        get_fill_color=[245, 245, 22],
        get_line_color=[209, 209, 17],
    )

# Set the viewport location
view_state = pdk.ViewState(latitude=41.781222, longitude=-3.771944, zoom=16, min_zoom= 10)

# Render
r = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/satellite-streets-v12',
                 initial_view_state=view_state, tooltip={"html": "<b>IDSensor: </b> {IDSensor} <br /> "
                                                                 "<b>Longitude: </b> {Longitude} <br /> "
                                                                 "<b>Latitude: </b>{Latitude} <br /> "
                                                                 "<b>Status: </b>{Status}"})

# output of clicked point should be input to a reusable list
selectedID = st.selectbox("Choose ID", df['IDSensor'])
r
filtered_selection=df[df['IDSensor']==selectedID].values
st.write('Values: '+str(filtered_selection))

DATA_URL = get_files_with_data()


data = pd.read_excel(DATA_PATH+'/'+DATA_URL[0], skiprows=1)
data = data[data['TD'].notna()]
data.drop(['BAT'], axis=1, inplace=True)
data=data.head(500)

sensor_errors=pd.read_csv("./sensor_errors/sensor_errors.csv").set_index('Error_Type')

st.subheader('Raw data')
st.write(data)

col2, col3= st.columns([2,2])

grouped_data=sensor_errors.groupby(['Error_Type']).size()
col2.subheader('Sensor´s errors data')
col2.write(sensor_errors)
col3.subheader('Grouped by error type')
col3.bar_chart(grouped_data)

data.drop(['TD','PAR','PLV','WV'], axis=1, inplace=True)
humb_to_filter = st.slider('TCB(Surface temperature)', float(data['TCB'].min()), float(data['TCB'].max()),(float(data['TCB'].min()), float(data['TCB'].max())))

filtered_data = data[data['TCB'] >= humb_to_filter[0]].set_index('FECHA')
filtered_data = filtered_data[filtered_data['TCB'] <= humb_to_filter[1]]

st.subheader('Filtered by TCB')
st.line_chart(filtered_data)

user_input = json.loads(st.text_input("Insert new values for prediction:", PREDICTION_FORMAT_EXAMPLE).replace("\'", "\""))
submit = st.button('Launch predictor for '+TARGET)
if submit:
    result=get_predictions_from_saved_model(user_input)
    st.subheader('Predicted value: '+str(result))
