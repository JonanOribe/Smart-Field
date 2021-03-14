from os import listdir
import os
from os.path import isfile, join
import csv
from configparser import ConfigParser
import sweetviz
import pandas as pd
from sklearn import metrics
from termcolor import colored
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

PROYECT_PATH=os.getcwd()
config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']
TARGET = config['DEFAULT']['target']
FORMAT = config['DEFAULT']['format']
COLUMNS_TO_DROP=config['DEFAULT']['columns_to_drop']
COLUMNS_TO_DROP_FUTURE=config['DEFAULT']['columns_to_drop_future']
DENDROMETER_AJUST_VALUE=int(config['DEFAULT']['dendrometer_ajust_value'])
TREE_MAX_DEPTH=int(config['DEFAULT']['tree_max_depth'])

def from_str_to_array(future):
    if(future==0):
        return COLUMNS_TO_DROP.split(',')
    else:
        return COLUMNS_TO_DROP_FUTURE.split(',')

def get_files_with_data():
    return [f for f in listdir(data_path) if (FORMAT in f and not 'lock.' in f)]

def dendrometer_and_battery_cleaner(df,future):
    df.drop(from_str_to_array(future), axis = 1, inplace = True)
    df=df[df['TD'].notna()]
    df['TD']=df['TD'].apply(dendrometer_ajust)
    return df

def generate_decision_tree(df,df_columns):
    feature_cols = [a for a in df_columns if a not in [TARGET]]
    X = df[feature_cols]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    clf = RandomForestClassifier(max_depth=TREE_MAX_DEPTH,random_state=0)

    return clf.fit(X_train,y_train.astype('int')),X_train,X_test,y_train.astype('int'),y_test.astype('int')

def generate_reports(X_train,X_test):
    report = sweetviz.compare([X_train, "Train"], [X_test, "Test"], "TCB")
    report.show_html("informe_datos.html",open_browser=False)

def generate_validation_data(df,df_columns):
    df_validation=df.sample(n = 3000, replace = False)
    feature_cols = [a for a in df_columns if a not in [TARGET]]
    df_validation_X = df[feature_cols]
    df_validation_y = df[TARGET].astype('int')
    return df.drop(df_validation.index),df_validation_X,df_validation_y

def dendrometer_ajust(dendrometer_value):
    return int(str(dendrometer_value)[:DENDROMETER_AJUST_VALUE])

def prepare_dataset(data_block,future=0):
    file_path='{}{}{}'.format(PROYECT_PATH,'/data/',data_block)
    df=pd.read_excel(file_path, skiprows=1)
    df=dendrometer_and_battery_cleaner(df,future)
    return ajust_columns(df,future)

def ajust_columns(df,future):
    df_columns=df.columns
    if(future==1):
        df_columns=df_columns.drop(labels=['FECHA'])
    df[df_columns] = df[df_columns].apply(pd.to_numeric)
    return df,df_columns

def get_predictions(clf,X_test,df_validation_X):
    y_pred = clf.predict(X_test)
    print(colored("Test_Accuracy:",'green'),metrics.accuracy_score(y_test, y_pred))
    val_pred = clf.predict(df_validation_X)
    print(colored("Validation_Accuracy:",'yellow'),metrics.accuracy_score(df_validation_y, val_pred))