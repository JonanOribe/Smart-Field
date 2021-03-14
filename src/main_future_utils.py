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

PRE_COLUMNS=config['DEFAULT']['pre_columns']

def from_str_to_array_future(columns):
    return columns.split(',')

def data_with_additions(df):
    counter_times=0
    df_len=len(df)
    array_of_columns=from_str_to_array_future(PRE_COLUMNS)
    for columns in array_of_columns:
        df[columns]=''

    for index, row in df.iterrows():
        if(counter_times>15):
            hours_difference=(df['FECHA'].iloc[counter_times-1].hour - df['FECHA'].iloc[counter_times-15].hour)
            minutes_difference=(df['FECHA'].iloc[counter_times-1].minute - df['FECHA'].iloc[counter_times-15].minute)
            column_position=0
            if(hours_difference==2 and minutes_difference==0):
                for columns in array_of_columns:
                    df.at[index, columns]=df.iloc[counter_times-15][column_position]
                    column_position+=1
        counter_times+=1
    print(df)
    df.to_csv('./datos_future.csv', sep=';')