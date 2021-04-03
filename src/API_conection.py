
import requests
import json

municipio="09059"
url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/"+municipio

querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqb25hbi5vcmliZUBnbWFpbC5jb20iLCJqdGkiOiIyYTM0ZDFlOS02YzU3LTRjNjQtYWM1Ni0yZWJiNWY0ZmIzMjEiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTYxNzQ0MTc5NSwidXNlcklkIjoiMmEzNGQxZTktNmM1Ny00YzY0LWFjNTYtMmViYjVmNGZiMzIxIiwicm9sZSI6IiJ9.I2epfuKBmHXggrPa-eKFxvgjpUK8IX42hiZ7nCKqNtc"}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data_link=json.loads(response.text)['datos']

response = requests.request("GET", data_link, headers=headers)
print(json.loads(response.text))
