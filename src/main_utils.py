from os import listdir
import os
from os.path import isfile, join
import csv
from configparser import ConfigParser

PROYECT_PATH=os.getcwd()
config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']

def get_files_with_data():
    return [f for f in listdir(data_path) if ('.xlsx' in f and not 'lock.' in f)]

def dendometer_and_battery_cleaner(df):
    df.drop(['Unnamed: 0', 'Batería de la estacion'], axis = 1, inplace = True)
    return df[df['Dendrómetro'].notna()]