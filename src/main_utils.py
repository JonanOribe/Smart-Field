from os import listdir
from os.path import isfile, join
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']

onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
print(onlyfiles)