import os
import sys
from termcolor import colored
from src.main_analisys import selection_validation

if __name__ == "__main__":
    if(len(sys.argv)>1):
        selection_validation(sys.argv[0])
    else:
        selection_validation()

