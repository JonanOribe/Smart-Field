import os
from termcolor import colored
from sklearn import tree
import matplotlib.pyplot as plt
from configparser import ConfigParser

from src.main_utils import dendrometer_and_battery_cleaner, generate_decision_tree, generate_reports, generate_validation_data, get_files_with_data,prepare_dataset,get_predictions
from src.main_future_utils import data_with_additions

#from main_utils import dendrometer_and_battery_cleaner, generate_decision_tree, generate_reports, generate_validation_data, get_files_with_data,prepare_dataset,get_predictions
#from main_future_utils import data_with_additions

config = ConfigParser()
config.read('config.cfg')
FUTURE=int(config['DEFAULT']['future'])

def selection_validation():
    valid=False
    while(valid!=True):
        selection = input("Choose program mode:(dashboard/IA) ")
        if(selection=='dashboard' or selection=='IA'):
            valid=True
            print("You choose: ", selection)
        else:
            print("Is is not an option.Retry")
    program_launcher(selection)

def program_launcher(selection):
    main_str=colored('Launching the program','green')
    option_selected=''

    if(selection=='dashboard'):
        option_selected=colored(' dashboard','green')
        print('{}{}'.format(main_str,option_selected))
        os.system("streamlit run ./src/main_dashboard.py")
    else:
        option_selected=colored(' IA MODEL','green')
        print('{}{}'.format(main_str,option_selected))
        main_process()

def main_process():

    xlsx_arr=get_files_with_data()

    for data_block in xlsx_arr:

        df,df_columns=prepare_dataset(data_block,FUTURE)
        if(FUTURE==0):
            df,df_validation_X,df_validation_y=generate_validation_data(df,df_columns)

            clf,X_train,X_test,y_train,y_test=generate_decision_tree(df,df_columns)

            get_predictions(clf,X_test,df_validation_X,y_test,df_validation_y)

            generate_reports(X_train,X_test)
        else:
            data_with_additions(df)
            pass
        
#main_process()