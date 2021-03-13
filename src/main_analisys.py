import os
from sklearn import metrics
from termcolor import colored
from sklearn import tree
import matplotlib.pyplot as plt

from main_utils import dendrometer_and_battery_cleaner, generate_decision_tree, generate_reports, generate_validation_data, get_files_with_data,prepare_dataset

PROYECT_PATH=os.getcwd()

xlsx_arr=get_files_with_data()

for data_block in xlsx_arr:

    df,df_columns=prepare_dataset(data_block)

    df,df_validation_X,df_validation_y=generate_validation_data(df,df_columns)

    clf,X_train,X_test,y_train,y_test=generate_decision_tree(df,df_columns)

    #Predict the response for test dataset
    y_pred = clf.predict(X_test)

    print(colored("Test_Accuracy:",'green'),metrics.accuracy_score(y_test, y_pred))

    val_pred = clf.predict(df_validation_X)
    print(colored("Validation_Accuracy:",'yellow'),metrics.accuracy_score(df_validation_y, val_pred))

    generate_reports(X_train,X_test)