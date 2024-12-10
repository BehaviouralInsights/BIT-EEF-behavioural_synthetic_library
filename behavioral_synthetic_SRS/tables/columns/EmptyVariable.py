from typing import Dict

import pandas as pd
import numpy as np

from .VariableType import VariableType

class EmptyVariable(VariableType):
    """Class defining the EmptyVariable datatype, which processes real data and generates synthetic data for an empty column of a table.

    Args:
        VariableType (abstract): Base class.
    """
    
    def __init__(self, column: pd.Series):
        """Constructor for EmptyVariable, defining the properties of an empty column.

        Args:
            column (pandas.Series): The column from which synthetic data is to be generated.
        """
        super().__init__(column, "empty")
        
    def analyse(self):
        """Public method that extracts the properties of the column and stores them internally.
        
        In this case there is nothing to store.
        """
        super()._delete_column()
    
    def generate(self, new_column_length: int) -> pd.Series:
        """Public method that generates a new column of synthetic data based on the properties obtained by the analyse() method.  Should be called *after* analyse().

        This just generates a column full of np.NaN values.

        Args:
            new_column_length (int): The number of rows required in the output column.

        Returns:
            Pandas.Series: A Pandas Series consisting of np.NaN values.
        """
        new_column = pd.Series([np.NaN for _ in range(new_column_length)])
        new_column.name = self.COLUMN_NAME
        return new_column
    
    def dictionary_out(self) -> Dict:
        """Outputs a summary of the column properties in dictionary format.  Should be called *after* analyse().

        Returns:
            dict: Summary of column properties. 
        """
        return {"Name": self.COLUMN_NAME, "Type": "empty", "all_values": "NaN"}