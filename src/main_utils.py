from os import listdir
import os
from os.path import isfile, join
import csv
from configparser import ConfigParser
import sweetviz
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function

PROYECT_PATH=os.getcwd()
config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']

def get_files_with_data():
    return [f for f in listdir(data_path) if ('.xlsx' in f and not 'lock.' in f)]

def dendometer_and_battery_cleaner(df):
    df.drop(['FECHA', 'BAT'], axis = 1, inplace = True)
    return df[df['TD'].notna()]

def generate_decision_tree(df,df_columns):
    #split dataset in features and target variable
    feature_cols = [a for a in df_columns if a not in ['SOILT']]
    X = df[feature_cols] # Features
    y = df['SOILT'] # Target variable
    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test
    # Create Decision Tree classifer object
    clf = DecisionTreeClassifier()

    # Train Decision Tree Classifer
    return clf.fit(X_train,y_train.astype('int')),X_train,X_test,y_train,y_test

def generate_reports(X_train,X_test):
    report = sweetviz.compare([X_train, "Train"], [X_test, "Test"], "TCB")
    report.show_html("informe_datos.html")

def generate_validation_data(df,df_columns):
    df_validation=df.sample(n = 600, replace = False)
    feature_cols = [a for a in df_columns if a not in ['SOILT']]
    df_validation_X = df[feature_cols] # Features
    df_validation_y = df['SOILT'] # Target variable
    return df.drop(df_validation.index),df_validation_X,df_validation_y