import os
import pandas as pd
from sklearn import metrics
from termcolor import colored
from sklearn import tree
import matplotlib.pyplot as plt

from main_utils import dendrometer_and_battery_cleaner, generate_decision_tree, generate_reports, generate_validation_data, get_files_with_data

PROYECT_PATH=os.getcwd()

xlsx_arr=get_files_with_data()

for data_block in xlsx_arr:
    file_path='{}{}{}'.format(PROYECT_PATH,'/data/',data_block)
    df=pd.read_excel(file_path, skiprows=1)
    df=dendrometer_and_battery_cleaner(df)
    df_columns=df.columns
    df[df_columns] = df[df_columns].apply(pd.to_numeric)

    df,df_validation_X,df_validation_y=generate_validation_data(df,df_columns)

    clf,X_train,X_test,y_train,y_test=generate_decision_tree(df,df_columns)

    #Predict the response for test dataset
    y_pred = clf.predict(X_test)
    # Model Accuracy, how often is the classifier correct?
    print(colored("Test_Accuracy:",'green'),metrics.accuracy_score(y_test.astype('int'), y_pred.astype('int')))
    #print(y_test.astype('int'))
    #print(y_pred.astype('int'))

    val_pred = clf.predict(df_validation_X)
    print(colored("Validation_Accuracy:",'yellow'),metrics.accuracy_score(df_validation_y.astype('int'), val_pred.astype('int')))
    #print(df_validation_y.astype('int'))
    #print(val_pred.astype('int'))
    generate_reports(X_train,X_test)