"""Contains the class StringVariable, which generates synthetic data from string real data held in a pandas Series.
"""

import pandas as pd
import numpy as np

from .VariableType import VariableType
from .general_functions import paste0

class StringVariable(VariableType):
    """Subclass extending VariableType.  Contains methods for producing a pandas series of synthetic categorical data from a pandas series of real categorical data.

        Public methods:
            __init__: Constructor.  Extends VariableType.__init__().
            analyse: Calculates summary statistics of the real data. Overrides VariableType.analyse().
            generate: Generates a column of synthetic data from the summary statistices.  Must be called after analyse() or set() methods.  Overrides VariableType.generate().
            dictionary_out: Outputs a dictionary containing column summary statistics. Must be called after analyse() or set() methods.  Overrides VariableType.dictionary_out().
            set_pattern: Sets table definitions that aren't set by the constructor for strings with patterns.  Used to create column definitions from stored summary statistics.
            set_no_patterns: Sets table definitions that aren't set by the constructor for unpatterned strings.  Used to create column definitions from stored summary statistics.
            analyse_missingness: Calculates the number of missing and present values in the real data Series.  Inherited from VariableType.
            delete_column: Marks the pandas Series containing real data for deletion and calls the garbage collector. Inherited from VariableType.
    """
    
    def __init__(self, column: pd.Series):
        """Constructor function for StringVariable, defining the properties of a string column.
        
        Passes column data to superclass constructor and sets column type to "string".  Sets a pair of internal constants, one used to generate placeholder text and the other the sensitivity of heuristics for determining whether a string column does or doesn't possess a pattern.
        
        Extends VariableType.__init__().

        Args:
            column (pandas.Series): The column from which synthetic data is to be generated.
        """
        
        super().__init__(column, "string")
        self.PLACEHOLDER_TEXT = "sample text" # maybe replace with lorem ipsum generator?
        self.PATTERN_THRESHOLD = 0.2 # scale value that determines whether the column is patterned or unpatterned.
        
    def __with_pattern_analyse(self):
        """Private method used to get letter frequencies per position if the strings have a pattern.
        """
        
        self.column = self.column.dropna().apply(list)
        new_column_names = paste0('position', range(1,(self.max_character_length+1)))
        column_split = pd.DataFrame(self.column.to_list(), columns=[new_column_names])
        
        #Cross tabulate each column and extract values and associated frequencies
        frequencies = column_split.apply(pd.Series.value_counts, normalize=True)
        self.frequencies = frequencies.fillna(0)
    
        
    def analyse(self):
        """Public method that extracts the summary statistics of the column and stores them internally as a frequency table for each value.
        
        This tests that there are enough non-missing values to meet the disclosure threshold, determines whether strings in the column are likely to have a common pattern, and generates internal lists of values and corresponding probabilities.  The orginal column is then marked for deletion and the garbage collector called.  Details of the summary statistics generated may be found in the documentation for the set_pattern() and the set_no_patterns() methods.
        
        Overrides VariableType.analyse()
        """
        
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
            
        super().delete_column()
        
    def __no_pattern_generate(self, new_column_length: int) -> pd.Series:
        """Private method used to generate synthetic data columns when there is no pattern present in the strings.

        Args:
            new_column_length (int): number of rows in the column.

        Returns:
            pandas.Series: synthetic data output.
        """
        
        def str_of_len(random_len: int, placeholder: str) -> str:
            output = ''
            while len(output) < random_len:
                output += placeholder
            return f'{output[0:random_len-1]}'
            
        def random_length_str(max_len: int, min_len: int, placeholder: str) -> str:
            return str_of_len(np.random.default_rng().integers(min_len, max_len+1), placeholder)
        
        def random_string_selection(max_character_length: int, min_character_length: int, placeholder_text: str, nrow_non_NA: int, nrow:int) -> str:
            probabilities=[nrow_non_NA/nrow, (nrow-nrow_non_NA)/nrow]
            values=[random_length_str(max_character_length, min_character_length, placeholder_text), np.NaN]
            return np.random.choice(values, p=probabilities)
                                           
        new_column = [random_string_selection(self.max_character_length, self.min_character_length, self.PLACEHOLDER_TEXT,self.non_missing, self.length) for _ in range(new_column_length)]
        new_column = pd.Series(new_column).replace('nan', np.NaN)
        return new_column
    
    def __with_pattern_generate(self, new_column_length: int) -> pd.Series:
        """Private method used to generate synthetic data columns when there is no pattern present in the strings.

        Args:
            new_column_length (int): Number of rows in the column.

        Returns:
            pd.Series: Column containing synthetic data.
        """
            
        def random_pattern(frequencies: pd.DataFrame, max_character_length: int) -> str:
            return ''.join([np.random.choice(frequencies.axes[0].tolist(), p=frequencies.iloc[:, i].tolist()) for i in range(max_character_length)])
        
        def random_string_selection(frequencies: pd.DataFrame, max_character_length:int, nrow_non_NA: int, nrow: int) -> str:
            probabilities=[nrow_non_NA/nrow, (nrow-nrow_non_NA)/nrow]
            values=[random_pattern(frequencies, max_character_length), np.NaN]
            return np.random.choice(values, p=probabilities)
        
        new_column = pd.Series([random_string_selection(self.frequencies, self.max_character_length, self.non_missing, self.length) for _ in range(new_column_length)])
    
        return new_column.replace('nan', np.NaN)
    
    def generate(self, new_column_length: int) -> pd.Series:
        """Public method that generates a new column of synthetic data based on stored summary statistics.  Should be called after the analyse() or set() methods.
        
        Missing values are generated according to their frequency.  Non-missing values in patterned columns are generated according to the frequency of characters in each position in the column. Non-missing values in unpattered columns consist of strings of random length (determined from the mean and standard deviation of the lengths of the strings in the real data) assembled from the placeholder text defined internally.
        
        Overrides VariableType.generate()
        
        Args:
            new_column_length (int): The number of rows required in the output column.

        Returns:
            Pandas.Series: A Pandas Series of object dtype.

        """
        
        if self.text_pattern:
            new_column = self.__with_pattern_generate(new_column_length)
        else:
            new_column = self.__no_pattern_generate(new_column_length)
            
        new_column.name = self.COLUMN_NAME
        
        return new_column
    
    def __with_pattern_dictionary(self) -> dict:
        """Private method that generates the output dictionary for patterned text.

        Returns:
            dict: A dictionary containing summary stats for the patterned text column.
        """
        
        def get_character_freq(i: int, frequencies: pd.DataFrame) -> dict:
            return dict(zip(frequencies.axes[0].tolist(), map(lambda x: round(x, 7), frequencies.iloc[:, i])))
            
        pattern_dict = {"Name": self.COLUMN_NAME, "Type": "text", "Pattern": True, "Max_length" : self.max_character_length}
        
        for i in range(self.max_character_length):
            pattern_dict[f'character_number_{i}']=get_character_freq(i, self.frequencies)
            
        pattern_dict['missing_value_freq'] = round(self.missing/self.length, 7)
        
        return pattern_dict
    
    def __no_pattern_dictionary(self) -> dict:
        """Private method that generates the output dictionary for non-patterned text.
        
        Returns:
            dict: A dictonary containing summary stats for non-patterned text.
        """
        
        return  {"Name": self.COLUMN_NAME,"Type": "text", "Pattern": False, "Max_length": self.max_character_length, "Min_length": self.min_character_length, "missing_value_freq": round(self.missing/self.length, 7)}
    
    def dictionary_out(self) -> dict:
        """Public method. Outputs a summary of the column summary statistics in dictionary format.   Should be called after the analyse() or set() methods.
        
        This creates a dictionary from the stored summary statistics and column parameters.
        
        Overrides VariableType.dictionary_out().

        Returns:
            dict: Summary of column properties. Floating point values are rounded at 7 decimal places.
        """
             
        if self.text_pattern:
            return self.__with_pattern_dictionary()
        else:
            return self.__no_pattern_dictionary()
        
    def set_pattern(self, pattern: bool, character_frequencies: dict[str, dict], max_length: int, missing_freq: float, number_of_rows: int):
        """Public method. Reads in a dictionary definition of column properties that are not set by the constructor for patterned strings.
        
        This reads in and/or converts the summary statistics to forms suitable for internal storage.

        Args:
            pattern (bool): do the strings follow a pattern (should be True).
            character_frequencies (dict[str, dict]): frequency patterns of characters in each position.
            max_length (int): maximum length of the patterned strings
            missing_freq (float): missing value frequency
            number_of_rows (int): number of rows in the original table
        """
        
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
        """Public method. Reads in a dictionary definition of column properties that are not set by the constructor for unpatterned strings.
        
        This reads in and/or converts the summary statistics to forms suitable for internal storage.
        
        Args:
            pattern (bool): do the strings follow a pattern (should be False)
            min_length (int): minimum length of the string
            max_length (int): maximum length of the string
            missing_freq (float): missing value frequency
            number_of_rows (int): number of rows in the original table
        """
        
        self.text_pattern = pattern
        self.min_character_length = min_length
        self.max_character_length = max_length
        
        self.length = number_of_rows
        self.missing = round(missing_freq*number_of_rows, 0)
        self.non_missing = round((1-missing_freq)*number_of_rows, 0)
        
            
        
        
      