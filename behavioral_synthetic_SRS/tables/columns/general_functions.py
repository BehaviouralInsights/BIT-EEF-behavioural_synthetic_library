import pandas as pd

def read_data(x):
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
    
def prepend(list, str): 
    str += '{0}'
    list = [str.format(i) for i in list] 
    return(list) 

def paste0(string, values):
    #This function helps us create new column names and imitates the R function 'paste0' (essentially appending values to strings).
    texts = [string + str(num1) for num1 in values]
    return texts

