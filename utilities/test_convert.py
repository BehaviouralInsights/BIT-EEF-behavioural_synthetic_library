from convert_from_srs import convert_SRStxt_to_JSON
from os import listdir
from os.path import isfile, join

def get_files_in_directory(directory: str) -> list:
    return [file for file in listdir(directory) if isfile(join(directory, file))]

def is_file_in_directory(file: str, files_in_dir) -> list:
    return any(file in filename for filename in files_in_dir)

OVERWRITE = False
BASE_DIRECTORY="G:\\Shared drives\\UK002524.000 EEF Synthetic Data\\EEF Synthetic Data Files\\Exported Data\\Production\\JSON files"

for batch in range(1,14):
    WORKDIR=f"{BASE_DIRECTORY}\\BATCH{batch}"
    file_list = get_files_in_directory(WORKDIR)
    txt_list = [file for file in file_list if ".txt" in file]
    json_list = [file for file in file_list if ".json" in file]
    
    for file in txt_list:
        data_name = file.split('.')[0]
        if any(data_name in file for file in json_list) and not OVERWRITE:
            print(f"File {data_name} already present and OVERWRITE set to False -- ignoring this file.")
            continue
        else:
            print(f"Creating or overwriting file {data_name}")
            INPUT_PATH=f"{WORKDIR}\\{data_name}.txt"
            OUTPUT_PATH=f"{WORKDIR}\\{data_name}.json"
            convert_SRStxt_to_JSON(INPUT_PATH, OUTPUT_PATH)
            
    print(f'Batch {batch} done.')
    
print("All batches done.")