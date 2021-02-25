from os import listdir
import os
from os.path import isfile, join
import xlrd
import csv
from configparser import ConfigParser

PROYECT_PATH=os.getcwd()
config = ConfigParser()
config.read('config.cfg')

data_path = config['DEFAULT']['data_path']

def get_files_with_data():
    return [f for f in listdir(data_path) if '.xlsx' in f]

def csv_from_excel(xlsx_file):
    wb = xlrd.open_workbook(xlsx_file)
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open('your_csv_file.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

# runs the csv_from_excel function:
