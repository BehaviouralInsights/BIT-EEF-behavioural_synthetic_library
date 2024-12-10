"""Contains the class EmptyVariable, which defines the properties of an empty column held in a pandas Series.
"""

import pandas as pd
import numpy as np

from .VariableType import VariableType

class EmptyVariable(VariableType):
    """Subclass extending VariableType.  Contains methods for producing a pandas series of synthetic empty column data from a pandas series of empty column data.

        Public methods:
            __init__: Constructor.  Extends VariableType.__init__().
            analyse: Calculates summary statistics of the real data. Overrides VariableType.analyse().
            generate: Generates a column of synthetic data from the summary statistices.  Must be called after analyse() or set() methods.  Overrides VariableType.generate().
            dictionary_out: Outputs a dictionary containing column summary statistics. Must be called after analyse() or set() methods.  Overrides VariableType.dictionary_out().
            delete_column: Marks the pandas Series containing real data for deletion and calls the garbage collector. Inherited from VariableType.
            
            (analyse_missingness is not a meaningful method for this class and has been overriden such that for all meaningful purposes it doesn't 'exist'.)
    """
    
    def __init__(self, column: pd.Series):
        """Constructor function for EmptyVariable, defining the properties of an empty column.
        
        Passes column data to superclass constructor and sets column type to "empty".
        
        Extends VariableType.__init__().
        
        Args:
            column (pandas.Series): The column from which synthetic data is to be generated.
        """
        
        super().__init__(column, "empty")
        
    def analyse(self):
        """Public method that extracts the summary statistics of the column and stores them internally as a frequency table for each value.
        
        In this case there is nothing to store, so it calls the inherited delete_column() method to mark the column for deletion and invoke the garbage collector.
        
        Overrides VariableType.analyse().
        """
        
        super().delete_column()
    
    def generate(self, new_column_length: int) -> pd.Series:
        """Public method that generates a new column of synthetic data based on stored summary statistics.  Should be called after the analyse() or set() methods.
        
        A pandas Series of the required length consisting entirly of np.NaN values is generated and assigned the same name as the real data column.
        
        Overrides VariableType.generate().
        
        Args:
            new_column_length (int): The number of rows required in the output column.

        Returns:
            Pandas.Series: A Pandas Series consisting of np.NaN values.
        """
        
        new_column = pd.Series([np.NaN for _ in range(new_column_length)])
        new_column.name = self.COLUMN_NAME
        return new_column
    
    def dictionary_out(self) -> dict:
        """Public method. Outputs a summary of the column summary statistics in dictionary format.   Should be called after the analyse() or set() methods.
        
        This creates a dictionary entry containing column name, type and values of "NaN".
        
        Overrides VariableType.dictionary_out().

        Returns:
            dict: Summary of column properties. 
        """
        
        return {"Name": self.COLUMN_NAME, "Type": "empty", "all_values": "NaN"}
    
    @property
    def analyse_missingness(self):
        # Here we try to block inheritance of the method by emulating its non-existence, as it makes no sense as part of this class.
        raise AttributeError(r"'EmptyVariable' object has has no attribute 'analyse_missingness'")
    
    