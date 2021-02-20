from os import listdir
from os.path import isfile, join
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']

def get_files_with_data():
    return [f for f in listdir(data_path) if '.csv' in f]