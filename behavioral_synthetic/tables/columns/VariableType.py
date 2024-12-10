"""Contains the class VariableType, an abstract base class for the column variable type classes.
"""
from abc import ABC, abstractmethod
import numpy as np
from  typing import Tuple
import gc

import pandas as pd

class VariableType(ABC):
    """Base class for all column variable classes. Stores code used by all column type classes.
    
        Public methods:
        __init__: Constructor method.
        analyse_missingness: Calculates the number of missing and present values in the real data Series.
        delete_column: Marks the pandas Series containing real data for deletion and calls the garbage collector.
        analyse: Abstract method. Placeholder for subclass analysis method.
        generate: Abstract method. Placeholder for subclass synthetic data generation method.
        dictionary_out: Abstract method. Placeholder for subclass summary statistics output method.
        get_THRESHOLD(): outputs value of disclosure threshold constant.
    """
    
    __THRESHOLD = 10 # minium safe number of records for averaging.
    
    @abstractmethod
    def __init__(self, column: pd.Series, column_type: str):
        """Abstract constructor for column type classes.
        
        Passes input variables to internal variables.

        Args:
            column (pandas.Series): The input data column.
            column_type (str): The type of the data column.
        """
        self.column = column
        self.COLUMN_TYPE = column_type
        self.COLUMN_NAME = column.name
        
    #@classmethod
    def analyse_missingness(self) -> Tuple[int, int, int]:
        """Public method that analyses the frequencies of missing and present values in the column. Called by subclass methods.
        
        Tests for safe disclosure and then calculates the number of missing and non-missing values based on the number of null variables located by pandas.

        Raises:
            ValueError: If the number of non-null entries in a column is less than the disclosure variable __THRESHOLD.

        Returns:
            Tuple[int, int, int]: The tuple (column_length, missing_values, non_missing_values) whose names are fairly self-explanatory.
        """
        column_length = self.column.shape[0]
        if self.column.replace("",np.NaN).dropna().size < self.__THRESHOLD:
           raise ValueError(f'Insuffucient number of values in series to produce disclosure safe values (less than {self.__THRESHOLD})')
        missing_values = self.column.isnull().sum()
        non_missing_values = column_length - missing_values
        return column_length, missing_values, non_missing_values
    
    def delete_column(self):
        """Public method that marks the column containing real data for deletion before calling the garbage collector.  Use after column has been analysed, typically as part of a subclass method.
        """
        del [[self.column]]
        gc.collect()
    
    @abstractmethod
    def analyse(self):
        """Abstract method. Placeholder for public method used to analyse column properties.

        Raises:
            NotImplementedError: If analyse() is accessed via this class rather than a subclass.
        """
        raise NotImplementedError
    
    @abstractmethod
    def generate(self, new_column_length: int) -> pd.Series:
        """Abstract method. Placeholder for public method used to generate synthetic data for a column.  An implemented version should be called after analyse().

        Args:
            new_column_length (int): The number of rows required in the output column.

        Raises:
            NotImplementedError: If generate() is accessed via this class rather than a subclass.

        Returns:
            pandas.Series: Pandas Series containing the synthetic data column.
        """
        raise NotImplementedError
    
    @abstractmethod
    def dictionary_out(self) -> dict:
        """Abstract methods. Placeholder for public method used to output the properties of a column used to generate synthetic data.  An implemented version should be called after analyse().

        Raises:
            NotImplementedError: If dictionary_out()is accessed via this class rather than a subclass.

        Returns:
            dict: Dictionary containing the properties of the column.
        """
        raise NotImplementedError
    
    def get_THRESHOLD(self) -> int:
        """Returns the value of the threshold for disclosure."""
        return self.__THRESHOLD