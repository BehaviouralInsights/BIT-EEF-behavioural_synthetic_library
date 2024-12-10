from abc import ABC, abstractmethod
import numpy as np
from  typing import Tuple, Dict
import gc

import pandas as pd

class VariableType(ABC):
    """Abstract base class for all column types.

    Args:
        ABC(helper): defines abstract classes in Python.

    Raises:
        ValueError: If the number of non-null entries in a column is less than the disclosure variable THRESHOLD.
        NotImplementedError: If analyse() is accessed via this class rather than a subclass.
        NotImplementedError: If generate() is accessed via this class rather than a subclass.
        NotImplementedError: If dictionary_out()is accessed via this class rather than a subclass.

    Returns:
        _type_: _description_
    """
    
    THRESHOLD = 10 # minium safe number of records for averaging.
    
    @abstractmethod
    def __init__(self, column: pd.Series, column_type: str):
        """Abstract constructor setting common attributes used by all column types.

        Args:
            column (pandas.Series): The input data column.
            column_type (str): The type of the data column.
        """
        self.column = column
        self.COLUMN_TYPE = column_type
        self.COLUMN_NAME = column.name
        
    #@classmethod
    def analyse_missingness(self) -> Tuple[int, int, int]:
        """Public method that analyses the frequencies of missing and present values in the column.

        Raises:
            ValueError: If the number of non-null entries in a column is less than the disclosure variable THRESHOLD.

        Returns:
            Tuple[int, int, int]: The tuple (column_length, missing_values, non_missing_values) whose names are fairly self-explanatory.
        """
        column_length = self.column.shape[0]
        #print(self.column)
        #print(self.column.replace("", np.NaN).dropna())
        if self.column.replace("",np.NaN).dropna().size < self.THRESHOLD:
           raise ValueError(f'Insuffucient number of values in series to produce disclosure safe values (less than {self.THRESHOLD})')
        missing_values = self.column.isnull().sum()
        non_missing_values = column_length - missing_values
        return column_length, missing_values, non_missing_values
    
    def _delete_column(self):
        """Private method that deletes the original input column from memory.  Use after column has been analysed.
        """
        del [[self.column]]
        gc.collect()
    
    @abstractmethod
    def analyse(self):
        """Placeholder for public method used to analyse column properties.

        Raises:
            NotImplementedError: If analyse() is accessed via this class rather than a subclass.
        """
        raise NotImplementedError
    
    @abstractmethod
    def generate(self, new_column_length: int) -> pd.Series:
        """Placeholder for public method used to generate synthetic data for a column.  Should be called after analyse().

        Args:
            new_column_length (int): The number of rows required in the output column.

        Raises:
            NotImplementedError: If generate() is accessed via this class rather than a subclass.

        Returns:
            pandas.Series: Pandas Series containing the synthetic data column.
        """
        raise NotImplementedError
    
    @abstractmethod
    def dictionary_out(self) -> Dict:
        """Placeholder for public method used to output the properties of a column used to generate synthetic data.  Should be called after analyse().

        Raises:
            NotImplementedError: If dictionary_out()is accessed via this class rather than a subclass.

        Returns:
            dict: Dictionary containing the properties of the column.
        """
        raise NotImplementedError