import os
import pandas as pd
from main_utils import csv_from_excel, get_files_with_data
PROYECT_PATH=os.getcwd()
xlsx_arr=get_files_with_data()

for data_block in xlsx_arr:
    file_path='{}{}{}'.format(PROYECT_PATH,'/data/',data_block)
    df=pd.read_excel(file_path)
    print(df)