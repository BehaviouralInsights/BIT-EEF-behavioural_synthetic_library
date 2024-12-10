import pandas as pd
import json

INPUT_DIR = "G:\\Shared drives\\UK002524.000 EEF Synthetic Data\\EEF Synthetic Data Files\Exported Data\\Production\\Post QA files"
FILE_LIST = "G:\\Shared drives\\UK002524.000 EEF Synthetic Data\\EEF Synthetic Data Files\Exported Data\\Production\\JSON files\\full_list.json"

APPEND = "_summary_stats_formatted_with_anon_ids.tsv"
OUT_DIR = "G:\\Shared drives\\UK002524.000 EEF Synthetic Data\\EEF Synthetic Data Files\Exported Data\\Production\\FINAL_SD_OUTPUT_FILES"


with open(FILE_LIST,'r') as f:
    file_names = json.load(f)

for batch in list(file_names.keys()):
    print(batch)
    for base_file in file_names[batch]:
        print(base_file)
        filepath = f"{INPUT_DIR}\\{batch}\\{base_file}{APPEND}"
        outfile = f"{OUT_DIR}\\{batch}\\{base_file}{APPEND}"

        # get first_line
        with open(filepath, 'r') as f:
            first_line = f.readline()

        dataframe = pd.read_csv(filepath, sep='\t', comment='#')

        dataframe = dataframe.drop(dataframe.columns[0], axis=1)

        with open(outfile, 'a') as f:
            f.write(first_line)
            dataframe.to_csv(f, index=False, sep='\t', lineterminator='\n')
    
print('Done')