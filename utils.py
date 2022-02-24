import os
import re
import time
import json
import pickle
import datetime
import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None  # default='warn'

class Utils:

    def __init__(self, mypath):
        
        self.mypath = mypath
        
    def open_json(self, filename):
        with open(f'{filename}', 'r', encoding='utf-8') as f:
            d = json.load(f)
        return(d)

    def save_json(self, data, filename):
        with open(f'{filename}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
    def get_all_filenames(self, path):
        onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return onlyfiles
    
    def get_all_filepaths(self, path):
        onlyfiles = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return onlyfiles
    
    def flatten_list(self, main_list):
        flat_list = [item for sublist in main_list for item in sublist]
        return flat_list
    
        
mypath = os.path.dirname(os.path.abspath(__file__))
utils = Utils(mypath)