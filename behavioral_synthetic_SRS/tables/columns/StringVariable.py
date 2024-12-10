from typing import Dict, List

import pandas as pd
import numpy as np

from .VariableType import VariableType
from .general_functions import paste0

class StringVariable(VariableType):
    
    def __init__(self, column: pd.Series):
        super().__init__(column, "string")
        self.PLACEHOLDER_TEXT = "sample text"
        self.PATTERN_THRESHOLD = 0.2
        
    def __with_pattern_analyse(self):
        
        def pad_list_with_spaces(col_list: List, pad_len: int) -> List:
            if len(col_list) < pad_len:
                for i in range(pad_len-len(col_list)):
                    col_list.append(' ')
                    
            return col_list
       
        self.column = self.column.dropna().apply(list)
        self.column = self.column.apply(lambda x: pad_list_with_spaces(x, self.max_character_length))
        
       
        new_column_names = paste0('position', range(1,(self.max_character_length+1)))
      
        letter_dict = {}
        for i, name in enumerate(new_column_names):
            letter_dict[name] = [value[i] for value in self.column.to_list()]
        column_split = pd.DataFrame(letter_dict)   
        
        #Cross tabulate each column and extract values and associated frequencies
        frequencies = column_split.apply(pd.Series.value_counts, normalize=True)
        self.frequencies = frequencies.fillna(0)
        
    
        
    def analyse(self):
        self.column = self.column.replace('', np.NaN)
        self.length, self.missing, self.non_missing = super().analyse_missingness()
        
        self.column = self.column.astype(str)
        self.column = self.column.replace('nan', np.NaN).replace('', np.NaN)
        self.av_character_length = self.column.dropna().apply(len).mean()
        self.sd_character_length = self.column.dropna().apply(len).std()
        self.max_character_length = self.column.dropna().apply(len).max()
        self.min_character_length = self.column.dropna().apply(len).min()
        
        #Define a rule for determining whether a pattern exists 
        self.text_pattern = False if (self.sd_character_length > self.PATTERN_THRESHOLD*self.av_character_length) else True
        if self.text_pattern: 
            self.__with_pattern_analyse()
            
        super()._delete_column()
        
    def __no_pattern_generate(self, new_column_length: int) -> pd.Series:
        
        def str_of_len(random_len: int, placeholder: str) -> str:
            output = ''
            while len(output) < random_len:
                output += placeholder
            return f'{output[0:random_len-1]}'
            
        def random_length_str(max_len: int, min_len: int, placeholder: str) -> str:
            return str_of_len(np.random.default_rng().integers(min_len, max_len+1), placeholder)
        
        def random_string_selection(max_character_length, min_character_length, placeholder_text,nrow_non_NA, nrow):
            probabilities=[nrow_non_NA/nrow, (nrow-nrow_non_NA)/nrow]
            values=[random_length_str(max_character_length, min_character_length, placeholder_text), np.NaN]
            return np.random.choice(values, p=probabilities)
                                           
        new_column = [random_string_selection(self.max_character_length, self.min_character_length, self.PLACEHOLDER_TEXT,self.non_missing, self.length) for _ in range(new_column_length)]
        new_column = pd.Series(new_column).replace('nan', np.NaN)
        return new_column
    
    def __with_pattern_generate(self, new_column_length: int) -> pd.Series:
            
        def random_pattern(frequencies, max_character_length):
            return ''.join([np.random.choice(frequencies.axes[0].tolist(), p=frequencies.iloc[:, i].tolist()) for i in range(max_character_length)])
        
        def random_string_selection(frequencies, max_character_length ,nrow_non_NA, nrow):
            probabilities=[nrow_non_NA/nrow, (nrow-nrow_non_NA)/nrow]
            values=[random_pattern(frequencies, max_character_length), np.NaN]
            return np.random.choice(values, p=probabilities)
        
        new_column = pd.Series([random_string_selection(self.frequencies, self.max_character_length, self.non_missing, self.length) for _ in range(new_column_length)])
    
        return new_column.replace('nan', np.NaN)
    
    def generate(self, new_column_length: int) -> pd.Series:
        
        if self.text_pattern:
            new_column = self.__with_pattern_generate(new_column_length)
        else:
            new_column = self.__no_pattern_generate(new_column_length)
            
        new_column.name = self.COLUMN_NAME
        
        return new_column
    
    def __with_pattern_dictionary(self):
        
        def get_character_freq(i, frequencies):
            return dict(zip(frequencies.axes[0].tolist(), map(lambda x: round(x, 7), frequencies.iloc[:, i])))
            
        pattern_dict = {"Name": self.COLUMN_NAME, "Type": "text", "Pattern": True, "Max_length" : self.max_character_length}
        
        for i in range(self.max_character_length):
            pattern_dict[f'character_number_{i}']=get_character_freq(i, self.frequencies)
            
        pattern_dict['missing_value_freq'] = round(self.missing/self.length, 7)
        
       
            
        return pattern_dict
    
    def __no_pattern_dictionary(self):
        return  {"Name": self.COLUMN_NAME,"Type": "text", "Pattern": False, "Max_length": self.max_character_length, "Min_length": self.min_character_length, "missing_value_freq": round(self.missing/self.length, 7)}
    
    def dictionary_out(self) -> Dict:
        if self.text_pattern:
            return self.__with_pattern_dictionary()
        else:
            return self.__no_pattern_dictionary()
        
    def set_pattern(self, pattern: bool, character_frequencies: Dict[str, Dict], max_length: int, missing_freq: float, number_of_rows: int):
        
        self.text_pattern = pattern
        
        # reconstruct pattern frequency table
        # get the column titles:
        column_list = list(character_frequencies['character_number_0'].keys()) #should always be at least one character present...
        # get the column values:
        dictionary_list = {value:[] for value in column_list}
        for value in list(character_frequencies.values()):
            for key, freq in value.items():
                dictionary_list[key].append(freq)
        # store as a dataframe, but need to transpose index and headings so storage is consistent with what the analysis method produces
        self.frequencies=pd.DataFrame.from_dict(dictionary_list, orient='index')
        
        
        self.max_character_length = max_length
        
        self.length = number_of_rows
        self.missing = round(missing_freq*number_of_rows, 0)
        self.non_missing = round((1-missing_freq)*number_of_rows, 0)
        
    def set_no_pattern(self, pattern: bool, min_length: int, max_length: int, missing_freq: float, number_of_rows: int):
        self.text_pattern = pattern
        self.min_character_length = min_length
        self.max_character_length = max_length
        
        self.length = number_of_rows
        self.missing = round(missing_freq*number_of_rows, 0)
        self.non_missing = round((1-missing_freq)*number_of_rows, 0)
        
            
        
        
      