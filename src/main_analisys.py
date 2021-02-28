import os
import pandas as pd
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from termcolor import colored 

from main_utils import dendometer_and_battery_cleaner, generate_decision_tree, generate_reports, get_files_with_data

PROYECT_PATH=os.getcwd()

xlsx_arr=get_files_with_data()

for data_block in xlsx_arr:
    file_path='{}{}{}'.format(PROYECT_PATH,'/data/',data_block)
    df=pd.read_excel(file_path, skiprows=1)
    df=dendometer_and_battery_cleaner(df)
    df_columns=df.columns
    df[df_columns] = df[df_columns].apply(pd.to_numeric)

    clf,X_train,X_test,y_train,y_test=generate_decision_tree(df,df_columns)

    #Predict the response for test dataset
    y_pred = clf.predict(X_test)
    # Model Accuracy, how often is the classifier correct?
    print(colored("Accuracy:",'green'),metrics.accuracy_score(y_test.astype('int'), y_pred.astype('int')))
    generate_reports(X_train,X_test)