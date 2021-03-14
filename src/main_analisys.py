import os
from sklearn import tree
import matplotlib.pyplot as plt
from configparser import ConfigParser

from main_utils import dendrometer_and_battery_cleaner, generate_decision_tree, generate_reports, generate_validation_data, get_files_with_data,prepare_dataset,get_predictions
from main_future_utils import data_with_additions

config = ConfigParser()
config.read('config.cfg')
FUTURE=int(config['DEFAULT']['future'])

PROYECT_PATH=os.getcwd()

xlsx_arr=get_files_with_data()

for data_block in xlsx_arr:

    df,df_columns=prepare_dataset(data_block,FUTURE)
    if(FUTURE==0):
        df,df_validation_X,df_validation_y=generate_validation_data(df,df_columns)

        clf,X_train,X_test,y_train,y_test=generate_decision_tree(df,df_columns)

        get_predictions(clf,X_test,df_validation_X)

        generate_reports(X_train,X_test)
    else:
        data_with_additions(df)
        pass