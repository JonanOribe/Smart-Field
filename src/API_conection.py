
import requests
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')
aemet_api=config['DEFAULT']['aemet_api']

municipio="09059"
url = '{}{}'.format("https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/",municipio)

querystring = {"api_key":aemet_api}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data_link=json.loads(response.text)['datos']

response = requests.request("GET", data_link, headers=headers)
print(json.loads(response.text))
