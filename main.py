from src.main_analisys import main_process
import os
from termcolor import colored

main_str=colored('Launching the program','green')
option_selected=''
if __name__ == "__main__":
    # execute only if run as a script
    selection = input("Choose program mode:(DASHBOARD/IA) ")
    print("You choose? ", selection)
    if(selection=='DASHBOARD'):
        option_selected=colored(' DASHBOARD','green')
        print('{}{}'.format(main_str,option_selected))
        os.system("streamlit run ./src/main_dashboard.py")
    else:
        option_selected=colored(' IA MODEL','green')
        print('{}{}'.format(main_str,option_selected))
        main_process()