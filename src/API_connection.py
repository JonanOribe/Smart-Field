
import requests
import json
import pandas as pd
import os
from os import listdir
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')
aemet_api=config['DEFAULT']['aemet_api']
data_path = config['DEFAULT']['data_path']
municipality = config['DEFAULT']['municipality']
PROYECT_PATH=os.getcwd()

def get_files_with_data_for_codmun():
    return [f for f in listdir(data_path) if ('codmun' in f and not 'lock.' in f)]

path='{}{}{}'.format(PROYECT_PATH,'/data/',get_files_with_data_for_codmun()[0])
df=pd.read_excel(path,dtype=str,skiprows=2)

df=df[df['NOMBRE']==municipality]

municipality_code='{}{}'.format(df['CPRO'].item(),df['CMUN'].item())
url = '{}{}'.format("https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/",municipality_code)

querystring = {"api_key":aemet_api}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data_link=json.loads(response.text)['datos']

response = requests.request("GET", data_link, headers=headers)
print(json.loads(response.text))
