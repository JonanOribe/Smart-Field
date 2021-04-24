from os import listdir
import os
from os.path import isfile, join
import csv
import matplotlib.pyplot as plt
from configparser import ConfigParser
import sweetviz
import pandas as pd
import numpy as np
from joblib import dump, load
from sklearn import metrics
from termcolor import colored
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

PROYECT_PATH=os.getcwd()
config = ConfigParser()
config.read('config.cfg')

DATA_PATH = config['DEFAULT']['data_path']
model_path = config['DEFAULT']['model_path']
TARGET = config['DEFAULT']['target']
FORMAT = config['DEFAULT']['format']
TEST_SIZE=float(config['DEFAULT']['test_size'])
COLUMNS_TO_DROP=config['DEFAULT']['columns_to_drop']
COLUMNS_TO_DROP_FUTURE=config['DEFAULT']['columns_to_drop_future']
DENDROMETER_AJUST_VALUE=int(config['DEFAULT']['dendrometer_ajust_value'])
TREE_MAX_DEPTH=int(config['DEFAULT']['tree_max_depth'])
ANOMALY_TCB_POSITIVE=int(config['DEFAULT']['anomaly_TCB_positive'])
ANOMALY_TCB_NEGATIVE=float(config['DEFAULT']['anomaly_TCB_negative'])
ANOMALY_HUMB=int(config['DEFAULT']['anomaly_HUMB'])
ANOMALY_TD=int(config['DEFAULT']['anomaly_TD'])
DEBUG_SENSORS=eval(config['DEFAULT']['DEBUG_SENSORS'])

model_name='{}{}{}'.format(model_path,TARGET,'.joblib')

def from_str_to_array(future):
    if(future==0):
        return COLUMNS_TO_DROP.split(',')
    else:
        return COLUMNS_TO_DROP_FUTURE.split(',')

def get_files_with_data():
    return [f for f in listdir(DATA_PATH) if (FORMAT in f and not 'lock.' in f)]

def dendrometer_and_battery_cleaner(df,future):
    df.drop(from_str_to_array(future), axis = 1, inplace = True)
    df=df[df['TD'].notna()]
    df['TD']=df['TD'].apply(dendrometer_ajust)
    return df

def generate_decision_tree(df,df_columns):
    feature_cols = [a for a in df_columns if a not in [TARGET]]
    X = df[feature_cols]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=1)
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
    anomaly_detector(df_validation_X,'Trainig: ')
    anomaly_detector(df_validation,'Predict: ')
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

def get_predictions(clf,X_test,df_validation_X,y_test,df_validation_y):
    y_pred = clf.predict(X_test)
    print(colored("Test_Accuracy:",'green'),metrics.accuracy_score(y_test, y_pred))
    val_pred = clf.predict(df_validation_X)
    print(colored("Validation_Accuracy:",'yellow'),metrics.accuracy_score(df_validation_y, val_pred))
    dump(clf, model_name)

def get_predictions_from_saved_model(val):
    target_name=model_name.replace('.joblib','').split('_')[1]
    dataframe = pd.DataFrame(val, index=[0])
    dataframe.drop(target_name, axis = 1, inplace = True)
    clf = load(model_name)
    y_pred = clf.predict(dataframe)
    return y_pred

def anomaly_detector(df,phase):
    errors_data=[]
    sensor_error_default_text='Error detected on sensor '
    errors_dict= {
      "TCB": 0,
      "HUMB": 0,
      "TD": 0
    }
    for index, row in df.iterrows():
        if(row['TCB']>ANOMALY_TCB_POSITIVE or float(row['TCB'])<ANOMALY_TCB_NEGATIVE):
            sensor_error_TCB='{}{}{}{}{}{}{}{}{}{}'.format(phase,sensor_error_default_text,'TCB on index ',str(index),'.Range should to be between ',ANOMALY_TCB_POSITIVE,' and ',ANOMALY_TCB_NEGATIVE,' but output equals to ',row['TCB'])
            errors_dict['TCB']+=1
            errors_data.append([index,'TCB',row['TCB']])
            print(colored(sensor_error_TCB,'yellow')) if(DEBUG_SENSORS==True) else None
        if(row['HUMB']>ANOMALY_HUMB):
            sensor_error_HUMB='{}{}{}{}{}{}{}{}'.format(phase,sensor_error_default_text,'HUMB on index ',str(index),'.Range should be under ',ANOMALY_HUMB,' but is ',row['HUMB'])
            errors_dict['HUMB']+=1
            errors_data.append([index,'HUMB',row['HUMB']])
            print(colored(sensor_error_HUMB,'yellow')) if(DEBUG_SENSORS==True) else None
        if(ANOMALY_TD>row['TD'] or row['TD']==''):
            sensor_error_TD='{}{}{}{}{}{}{}{}'.format(phase,sensor_error_default_text,'TD on index ',str(index),'.Range should be over ',ANOMALY_TD,' but is ',row['TD'])
            errors_dict['TD']+=1
            errors_data.append([index,'TD',row['TD']])
            print(colored(sensor_error_TD,'yellow')) if(DEBUG_SENSORS==True) else None
    print(colored('{}{}{}'.format(phase,'Total errors from the device equals to ',str(errors_dict)),'red'))

    df_errors=pd.DataFrame(errors_data,columns = ['Index', 'Error_Type','Value'])
    df_errors.to_csv('./sensor_errors.csv', index = False)
