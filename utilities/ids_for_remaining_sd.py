from behavioral_synthetic.tables.columns.general_functions import index_to_column, group_ids,individual_ids
import json
import pandas as pd
import numpy as np

def generate_anon_ids(no_meta_data_file, with_meta_data_file):
    try:
        dataframe = pd.read_csv(no_meta_data_file, sep='\t', comment='#')
        dataframe.to_csv(with_meta_data_file, sep='\t')

        #handling the anon/unique id columns:
        id_column_list = ["Project_Row_ID", "Anon_Pupil_ID", "Anon_School_ID", "Anon_Teacher_ID", "Anon_Class_ID"]
        no_rows = len(dataframe.index)
        print(no_rows)
        for col in id_column_list:
            if not dataframe[col].isna().all():
                print(col)
                if col == "Project_Row_ID":
                    dataframe[col] = index_to_column(dataframe) #, "Project_Row_ID")
                elif col == "Anon_Pupil_ID":
                    dataframe[col] = individual_ids(4, 7, no_rows, False, True)
                elif col == "Anon_School_ID":
                    group_size = int(max(5,min(no_rows/50, 250 )))
                    print(group_size)
                    dataframe[col] = group_ids(4, 6, group_size, no_rows, False, True)
                elif col == "Anon_Teacher_ID":
                    group_size = int(max(5, min(no_rows/100, 80 )))
                    print(group_size)
                    dataframe[col] = group_ids(1, 2, group_size, no_rows, False, True)
                elif col == "Anon_Class_ID":
                    group_size = int(max(5, min(no_rows/100, 500 ))) # orginally set to have a max of 999, seems that slows it down in large cases
                    print(group_size)
                    dataframe[col] = group_ids(1, 3, group_size, no_rows, False, True)

        dataframe.to_csv(with_meta_data_file, sep='\t')
    
        return {
            "successful": True
        }
    except Exception as e:
        return {
            "successful": False,
            "error": e
        }
   




BATCH_NUMBER=13

SOURCE_DIRECTORY = f"G:\\Shared drives\\UK002524.000 EEF Synthetic Data\\EEF Synthetic Data Files\\Exported Data\\Production\\JSON files\\BATCH{BATCH_NUMBER}"
TARGET_DIRECTORY = f"G:\\Shared drives\\UK002524.000 EEF Synthetic Data\\EEF Synthetic Data Files\\Exported Data\\Production\\TSV files\\BATCH{BATCH_NUMBER}"
METADATA_TARGET_DIRECTORY= f"G:\\Shared drives\\UK002524.000 EEF Synthetic Data\\EEF Synthetic Data Files\\Exported Data\\Production\\Post QA files\\BATCH{BATCH_NUMBER}"

files_base = [
"Maths in Context",
]


append = "_summary_stats_formatted"

files = [f"{file}{append}" for file in files_base]

for file in files:

    no_meta_data_file = f"{TARGET_DIRECTORY}\\{file}.tsv"
    with_meta_data_file = f"{METADATA_TARGET_DIRECTORY}\\{file}_with_anon_ids.tsv"

    id_gen_status  = generate_anon_ids(no_meta_data_file, with_meta_data_file)
    if not id_gen_status["successful"]:
        #write_log(f"WARNING: problem adding ids to synthetic data: {id_gen_status['error']}",qa_logfile)
        print(f"WARNING: problem adding ids to synthetic data: {id_gen_status['error']}")
        
print('DONE')