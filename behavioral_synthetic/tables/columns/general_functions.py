"""This module contains functions that are generally helpful when generating synthetic data.
"""

import pandas as pd
import string
import secrets
import random
import subprocess
import os

RSCRIPT_TO_RUN="QA_code.R"

def read_data(x: str) -> pd.DataFrame:
    """Reads in data from a file to a Pandas dataframe.  File suffixes handled are: csv, txt, tsv, xls, xlsx, sas7bdat, sav, dta, pkl.
    
    Uses file suffixes to determine which pandas read function to call.

    Args:
        x (str): File path.

    Raises:
        Exception: Unsupported file type.

    Returns:
        pd.DataFrame: Dateframe containing file data.
    """
    
    if (x.endswith(('csv', 'txt'))):
        return pd.read_csv(x) 
    elif (x.endswith(('tsv'))):
        return pd.read_csv(x, sep='\t')
    elif (x.endswith(('xlsx', 'xls'))):
        dictionary = pd.read_excel(x, sheet_name = None) 
        if (len(dictionary.keys()) == 1):
            name_of_sheet = list(dictionary.keys())
            name_of_sheet = name_of_sheet[0]
            simple_data_frame = dictionary[name_of_sheet]
            return simple_data_frame
        else:
            return dictionary
    elif (x.endswith('sas7bdat')):
        return pd.read_sas(x) 
    elif (x.endswith('sav')):
        return pd.read_spss(x) 
    elif (x.endswith('dta')):
        return pd.read_stata(x)  
    elif (x.endswith('pkl')):
        return pd.read_pickle(x) 
    else:
        raise Exception("Sorry, file type not supported. Try converting to csv, xlsx, txt or pkl.")
    

def paste0(string: str, values: list) -> list[str]:
    """This imitates the R function 'paste0' (essentially appending values to strings).

    Args:
        string (str): string to be appended
        values (list): endings to be appended

    Returns:
        list[str]: list consisting of the string plus all endings.
    """
    
    texts = [string + str(num1) for num1 in values]
    return texts

def index_to_column(dataframe: pd.DataFrame) -> pd.Series:
    index_list = dataframe.index.to_list()
    return pd.Series(index_list)

def unique_id(min_length: int, max_length: int, letters: bool, numbers: bool) -> str:
    if not (letters or numbers):
        raise ValueError("one or both of 'letters' and 'numbers' must be true")
    elif (letters and numbers):
        alphabet = string.ascii_letters + string.digits
    elif (letters and not numbers):
        alphabet = string.ascii_letters
    elif (numbers and not letters):
        alphabet = '123456789' #string.digits (remove 0 so leading zeroes aren't an issue)
    
    if min_length == max_length:
        length = min_length
    else:
        length = random.randrange(min_length, max_length + 1)
        
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def individual_ids(min_length: int, max_length: int, column_length: int, letters: bool, numbers: bool) -> pd.Series:
    id_set = set()
    set_size = 0
    while set_size < column_length:
        id = unique_id(min_length, max_length, letters, numbers)
        id_set.add(id)
        set_size = len(id_set)
        
    return pd.Series([element for element in id_set])

def group_ids(min_length: int, max_length: int, group_size: int, column_length: int, letters: bool, numbers: bool) -> pd.Series:
    id_set = set()
    set_size = 0
    while set_size < group_size:
        id = unique_id(min_length, max_length, letters, numbers)
        id_set.add(id)
        set_size = len(id_set)
        
    id_list = list(id_set)
    return pd.Series([random.choice(id_list) for _ in range(column_length)])    

def run_Rscript(settings: dict):
    
   # os.environ["R_LIBS"]=settings["R_LIBARIES_LOCATION"]
    pwd = os.getcwd()
    
    return subprocess.run(['Rscript', '--vanilla', RSCRIPT_TO_RUN, settings["INPUT_DIR"], settings["OUTPUT_DIR"], settings["JSON_FILE_LOC"], pwd],  capture_output=True, cwd=pwd)