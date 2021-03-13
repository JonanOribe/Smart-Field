from os import listdir
import os
from os.path import isfile, join
import csv
from configparser import ConfigParser
import sweetviz
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

PROYECT_PATH=os.getcwd()
config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']
TARGET = config['DEFAULT']['target']
FORMAT = config['DEFAULT']['format']
FUTURE=int(config['DEFAULT']['future'])
COLUMNS_TO_DROP_FUTURE=config['DEFAULT']['columns_to_drop_future']
DENDROMETER_AJUST_VALUE=int(config['DEFAULT']['dendrometer_ajust_value'])
TREE_MAX_DEPTH=int(config['DEFAULT']['tree_max_depth'])
