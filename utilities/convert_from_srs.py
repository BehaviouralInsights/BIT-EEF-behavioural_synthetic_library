import pandas as pd
import re
import json

# Currently exports numerical and categorical data, as this seems to be what we actually find in the data for the most part.

#Base table definition dictionary
table_summary =  {
    "Table_name": "Dummy_name",
    "Table_type": "Dummy_type",
    "Number_of_rows": 0,
    "Column_details": ""}


#Dictionary mapping how variables were named in the SRS output file, and how they are named in sample_output.json
Values_to_rename ={
            "COLUMN NAME": "Name",
            "COLUMN TYPE" : "Type",
            "COLUMN NA" : "all_values",
            "DECIMAL PRECISION" : "decimal_precision",
            "MEAN" : "mean",
            "STANDARD DEVIATION" : "standard_deviation",
            "MINIMUM" : "minimum",
            "MAXIMUM" : "maximum",
            "IS INTEGER" : "is_integer",
            "MISSING FREQUENCY" : "missing_value_freq",
            "AVERAGED MAXIMUM AND MINIMUM" : "averaged_max_and_min"
            }

#Dictionary mapping variables that did not appear in the text file, but were in the sample_output.json (the values are also taken from sample_output.json)
fields_to_add = {"numeric": {"# of values in average_max_min": 10},
    "text": {"Pattern": False,
            "Max_length": 21,
            "Min_length": 2,
            "missing_value_freq": 0.0}
}


def import_data(input_file):
    """Import the SRS output file as a dataframe."""
    file = pd.read_csv(input_file, delimiter='\t', encoding='unicode_escape' )
    pd.set_option('display.max_colwidth', None) #otherwise data set name will be truncated
   
    # Read in variable names and remove the lines that are table summaries. 
    table_summary["Table_name"] = file.iloc[0].to_string().split("TABLE NAME:")[1].strip()
    table_summary["Table_type"] = file.iloc[1].to_string().split(":")[1].strip()
    table_summary["Number_of_rows"] = int(file.iloc[2].to_string().split(":")[1].strip())
    
    # drop the table summary as no longer needed
    file.drop(index = [0,1,2,3], inplace = True)
    
    #Rename some columns to make them more consistent and easier to process below
    file = file.map(lambda x: x.replace("AVERAGED MAXIMUM AND MINIMUM", "AVERAGED MAXIMUM AND MINIMUM:") if isinstance(x, str) else x)
    file = file.map(lambda x: x.replace("MISSING VALUES FREQUENCY", "MISSING FREQUENCY") if isinstance(x, str) else x)
    file = file.map(lambda x: x.replace("COLUMN VALUE", "COLUMN NA") if isinstance(x, str) else x)
    
    return file


def create_dict_list(df: pd.DataFrame) -> list:
    """Takes the dataframe and creates a list of dictionaries for each column by splitting the values on ':'.
    Removes the fields included as explanation for the SRS

    Args:
        df (_type_): Output of import_data()
    """    
    dict_list = []
    current_dict = {}
    for index, row in df.iterrows():
        if re.match(r"#\s?BEGIN COLUMN", row.iloc[0]):
            current_dict = {}
        elif re.match(r"#\s?END COLUMN", row.iloc[0]):
            dict_list.append(current_dict)

#Create a dictionary for each separate column and append to the list
        else:
            if ":" not in row.iloc[0]:
                print("Error: Invalid row format -", row)
                break
            elif "VALUE" in row.iloc[0] and "FREQUENCY" in row.iloc[0]:
                key, value = row.iloc[0].split("FREQUENCY:", 1)
                current_dict[key.strip()] = value.strip()
            else:
                key, value = row.iloc[0].split(":", 1)
                current_dict[key.strip()] = value.strip()
    
    for i in dict_list:
        
        i.pop('FREQUENCIES', None)
        i.pop('NOTE', None)
        
        #Remove the phrase 'VALUE' from the key, and convert the frquency values from strings to floats
        list_of_keys_to_drop = [key for key in i.keys() if "VALUE" in key]
        clean_key_value_pairs = {key.replace("VALUE: ", ""): float(value) for key, value in i.items() if "VALUE" in key}
        i.update(clean_key_value_pairs)
        for key in list_of_keys_to_drop:
            i.pop(key, None)

        
    return dict_list


def clean_key_names(dict_list: list, Renaming_dict: dict=Values_to_rename) -> list:
    """Changes the names in the list of dictionaries to those used in sample_outuput.json

    Args:
        dict_list (list): output of create_dict_list()
        Renaming_dict (dict, optional): A dictionary of names to change. Defaults to Values_to_rename.

    Returns:
        dict: _description_
    """    
    cleaned_list = []
    for i in dict_list:
        cleaned_dict = {Renaming_dict[key]: value for key, value in i.items() if key in Renaming_dict.keys()}
        add_dict = {key: value for key, value in i.items() if key not in Renaming_dict.keys()}
        cleaned_dict.update(add_dict)
        cleaned_list.append(cleaned_dict)
    
    return cleaned_list


def type_specific_cleaning(dict_list: list, fields_to_add: dict) -> dict:
    """Other ad-hoc cleaning that is specific to the data type of the column. 

    Args:
        dict_list (list): _description_
        fields_to_add (dict): _description_

    Returns:
        dict: _description_
    """    
    cleaned_list = []
    for i in dict_list:
        if i['Type'] == 'numeric':
            #Mean and standard deviation were on the same row in the text file - split them into separate fields
            i['standard_deviation'] = i['mean'].split( 'STANDARD')[1].split(":")[1].strip()
            i['mean'] = i['mean'].split( 'STANDARD')[0].strip()
            
            #Add the fields that were in sample_output.json but not in the SRS output
            i.update(fields_to_add['numeric'])
            
            #Make sure all the numeric fields are floats
            clean_num = {key: float(value) for key, value in i.items() if key in ['mean', 'standard_deviation', 'decimal_precision', 'minimum', 'maximum', 'missing_value_freq']}
            i.update(clean_num)
        elif i['Type'] == 'text' or i['Type'] == "\"text\"":
            #Add the fields that were in sample_output.json but not in the SRS output
            i['Type'] = 'text'
            i.update(fields_to_add['text'])
        cleaned_list.append(i)
    return cleaned_list

def filter_for_type(y, type):
    #Helper function to check out how cleaning has gone
    return [x for x in y if x['Type'] == type]

def save_json_to_file(json_obj, file_path):
    #Function to save output as json
    with open(file_path, 'w') as file:
        json.dump(json_obj, file, indent=4)
        

def convert_SRStxt_to_JSON(input_file, output_file):
    data = import_data(input_file)
    dict_list = create_dict_list(data)
    cleaned_list = clean_key_names(dict_list)
    cleaned_list = type_specific_cleaning(cleaned_list, fields_to_add)
    table_summary["Column_details"] = cleaned_list
    #save_json_to_file(cleaned_list, OUTPUT_PATH)
    save_json_to_file(table_summary, output_file)
    print(f"{table_summary['Table_name']} summary statistics converted!")