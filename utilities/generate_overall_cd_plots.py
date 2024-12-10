import json
import numpy as np
from matplotlib import pyplot as plt

def clean_data(data, directory, correlation_file):
    
    cleaned_data = []
    for set in list(data.keys()):
        dataset=data[set]
        for item in dataset:
            if 'p_value' not in list(item.keys()):
                message = f'The p-value for {item["Comparison_column_1"]} and {item["Comparison_column_2"]} correlations in set {set} is missing:' +'\n' +f' {item}'
                with open(f"{directory}\\..\\{correlation_file.split('.')[0]}_WARNING_notes.txt", "a") as file:
                    file.write(message + "\n")
            else:
                cleaned_data.append(item)
    
    return cleaned_data

def extract_correlations(input_directory, output_directory, correlation_file):
    
    with open(f"{input_directory}\\{correlation_file}", 'r') as file:
        data=json.load(file)
        
    cleaned_data = clean_data(data, output_directory, correlation_file)
    
    return [item['p_value'] for item in cleaned_data]

def get_cumulative_distribution(data_list):
    
    fractional_distance = []
    for i in range(len(data_list)):
        fractional_distance.append((i+1)/len(data_list))

    return {"X":fractional_distance, "Y": np.sort(data_list)}

def plot_cumulative_distribution(data, directory, batch_number):
    try:
        #based on https://stackoverflow.com/posts/22588814/revisions
        Comparison_X = data["X"]
        Comparison_Y = data["X"]  #both are set equal to the X paramater to get linear curve with gradient 1, the ideal case
        
        file_prefix = f"BATCH{batch_number}"
    
        output = f"{directory}\\{file_prefix}_cumulative_distribution.pdf"
        #with PdfPages(f"{directory}\\{file_prefix}_cumulative_distribution.pdf") as output:
        plt.step(data['X'], data['Y'], label = 'synthetic data')
        plt.step(Comparison_X,Comparison_Y, label = 'ideal case')
        plt.title(file_prefix)
        plt.xlabel("Fraction")
        plt.ylabel("p-value")
        plt.legend()
        plt.grid(True)
        plt.savefig(output, format="pdf")
        plt.close()   
        
        return {
            "successful": True
        }
    except Exception as e:
        return {
            "successful": False,
            "error": e
        }
        
        
NUMBER_OF_BATCHES = 13
BATCH_LOCATION = "G:\\Shared drives\\UK002524.000 EEF Synthetic Data\\EEF Synthetic Data Files\\Exported Data\\Production\\Post QA files"
OUTPUT_BASE = "G:\\Shared drives\\UK002524.000 EEF Synthetic Data\\EEF Synthetic Data Files\\Exported Data\\Production\\bulk_cd_graphs"
all_data = [] #{"X":[], "Y": []}
    
for batch in range(1, NUMBER_OF_BATCHES+1):
    print(batch)
    input_directory = f"{BATCH_LOCATION}\\BATCH{batch}"
    input_file = "corr_p_values.json"
    output_directory = f"{OUTPUT_BASE}\\BATCH{batch}"
    
    cleaned_data = extract_correlations(input_directory, output_directory, input_file)
    all_data.extend(cleaned_data)
    
    plot_status = plot_cumulative_distribution(get_cumulative_distribution(cleaned_data), output_directory, batch)
    if not plot_status["successful"]:
        print(f"Failed to generate figure for batch {batch} with error message: {plot_status['error']}")
    
print('all')
plot_status = plot_cumulative_distribution(get_cumulative_distribution(all_data), OUTPUT_BASE, "_all")
if not plot_status["successful"]:
    print(f"Failed to generate figure for batch {batch} with error message: {plot_status['error']}")
    
print('done')
           
    
    