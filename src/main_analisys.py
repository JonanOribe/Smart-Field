import pandas as pd
from main_utils import get_files_with_data

csv_arr=get_files_with_data()

for data_block in csv_arr:
    df=pd.DataFrame(data_block,sep=';')
    print(df)