from os import listdir
import sys, os
from os.path import isfile, join
import csv
from configparser import ConfigParser
import sweetviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

PROYECT_PATH=os.getcwd()
sys.path.insert(0, PROYECT_PATH + '/src/')

from main_utils import dendrometer_ajust, dendrometer_and_battery_cleaner, generate_decision_tree, generate_reports, generate_validation_data, get_files_with_data,from_str_to_array

config = ConfigParser()
config.read('config.cfg')

DATA_PATH = config['DEFAULT']['data_path']
TARGET = config['DEFAULT']['target']
FORMAT = config['DEFAULT']['format']
COLUMNS_TO_DROP=config['DEFAULT']['columns_to_drop']
DENDROMETER_AJUST_VALUE=int(config['DEFAULT']['dendrometer_ajust_value'])
TREE_MAX_DEPTH=int(config['DEFAULT']['tree_max_depth'])

def test_dendrometer_ajust():
    dendrometer_values=[34567,45321,33687,44433]
    for dendrometer_value in dendrometer_values:
        val=dendrometer_ajust(dendrometer_value)
        final_val=int(str(val)[:DENDROMETER_AJUST_VALUE])
        assert final_val<(10**(DENDROMETER_AJUST_VALUE)) and not final_val<(10**(DENDROMETER_AJUST_VALUE-1))

def test_config_params():
    arr_to_test=[DATA_PATH,TARGET,FORMAT,COLUMNS_TO_DROP,DENDROMETER_AJUST_VALUE,TREE_MAX_DEPTH]
    for config_to_test in arr_to_test:
        assert len(str(config_to_test))>0

def test_from_str_to_array():
    assert len(from_str_to_array(0))>0

def test_get_files_with_data():
    assert FORMAT in get_files_with_data()[0]