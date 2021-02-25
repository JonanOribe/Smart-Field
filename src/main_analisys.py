import os
import pandas as pd
from main_utils import dendometer_and_battery_cleaner, get_files_with_data

PROYECT_PATH=os.getcwd()

xlsx_arr=get_files_with_data()

for data_block in xlsx_arr:
    file_path='{}{}{}'.format(PROYECT_PATH,'/data/',data_block)
    df=pd.read_excel(file_path, skiprows=1)
    df=dendometer_and_battery_cleaner(df)
    df_columns=df.columns
    df[df_columns] = df[df_columns].apply(pd.to_numeric)
    print(df.corr())