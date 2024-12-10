"""Contains the class CategoricalVariable, which generates synthetic data from categorical real data held in a pandas Series.
"""
import gc

import pandas as pd
import numpy as np

from .VariableType import VariableType

class CategoricalVariable(VariableType):
    """Subclass extending VariableType.  Contains methods for producing a pandas series of synthetic categorical data from a pandas series of real categorical data.

        Public methods:
            __init__: Constructor.  Extends VariableType.__init__().
            analyse: Calculates summary statistics of the real data. Overrides VariableType.analyse().
            generate: Generates a column of synthetic data from the summary statistices.  Must be called after analyse() or set() methods.  Overrides VariableType.generate().
            dictionary_out: Outputs a dictionary containing column summary statistics. Must be called after analyse() or set() methods.  Overrides VariableType.dictionary_out().
            set: Sets table definitions that aren't set by the constructor.  Used to create column definitions from stored summary statistics.
            analyse_missingness: Calculates the number of missing and present values in the real data Series.  Inherited from VariableType.
            delete_column: Marks the pandas Series containing real data for deletion and calls the garbage collector. Inherited from VariableType.
    """
    
    def __init__(self, column: pd.Series):
        """Constructor function for CategoricalVariable, defining the properties of a categorical column.
        
        Passes column data to superclass constructor and sets column type to "categorical", as well as storing the data type of column variables.
        
        Extends VariableType.__init__().

        Args:
            column (pandas.Series): The column from which synthetic data is to be generated.
        """
        
        super().__init__(column, "categorical")
        self.dtypes = column.dtypes
           
    def analyse(self):
        """Public method that extracts the summary statistics of the column and stores them internally as a frequency table for each value.
        
        This tests that there are enough non-missing values to meet the disclosure threshold, and generates internal lists of values and corresponding probabilities.  The orginal column is then marked for deletion and the garbage collector called.  Details of the summary statistics generated may be found in the documentation for the set() method.
        
        Overrides VariableType.analyse().

        Raises:
            ValueError: If the number of non-null and non-blank entries in a column is less than the disclosure variable THRESHOLD.
        """
        
        # note we don't need to analyse for missingness as this will automatically account for it
        self.column=self.column.astype('object')
        
        if self.column.replace("", np.NaN).dropna().size < self.get_THRESHOLD():
            raise ValueError(f'Insuffucient number of values in series to produce disclosure safe results (less than {self.get_THRESHOLD()})')
        
        self.column.fillna('nan', inplace=True)
        cross_tabulation = self.column.value_counts(dropna = False, normalize=True)
        self.values = cross_tabulation.axes[0].tolist()
        self.probabilities = cross_tabulation.tolist()
        super().delete_column()
        
    def generate(self, new_column_length: int) -> pd.Series:
        """Public method that generates a new column of synthetic data based on stored summary statistics.  Should be called after the analyse() or set() methods.
        
        Values are randomly drawn with replacement from frequencies that include missing values and placed in a pandas Series.
        
        Overrides VariableType.generate().

        Args:
            new_column_length (int): The number of rows required in the output column.

        Returns:
            Pandas.Series: A Pandas Series of object, float64 or Int64 dtype, depending on the properties of the original column.
        """
        
        new_column = pd.Series(np.random.choice(self.values, new_column_length,  p=self.probabilities)).replace('nan', np.NaN)
        new_column.name = self.COLUMN_NAME
        #new_column = new_column.astype(str(self.dtypes))  Seems to be causing problems IOT 2024-05-14
        return new_column
    
    def dictionary_out(self) -> dict:
        """Public method. Outputs a summary of the column summary statistics in dictionary format.   Should be called after the analyse() or set() methods.
        
        This creates a dictionary from the stored summary statistics and column parameters.
        
        Overrides VariableType.dictionary_out().

        Returns:
            dict: Summary of column properties. Floating point values are rounded at 7 decimal places.
        """
            
        dictionary = dict(zip(self.values, [round(p,7) for p in self.probabilities]))
        dictionary['Type'] = 'categorical'
        dictionary['Name'] = self.COLUMN_NAME        
        return dictionary
    
    def set(self, frequencies: dict[str | int | float, float]):
        """Public method. Reads in a dictionary definition of column properties that are not set by the constructor.
        
        This reads in and/or converts the summary statistics to forms suitable for internal storage.

        Args:
            frequencies (dict[str  |  int, float]): Data on categorical variable frequencies in the form {VALUE1: FREQUENCY1, VALUE1: FREQUENCY2, ... }.
        """
        
        self.values = [ value for value in frequencies.keys()]
        self.probabilities = [frequencies[value] for value in frequencies]
        # renormalise probabilities in case of unusual behaviour 2024-05-14
        total = sum(self.probabilities)
        self.probabilities = [value/total for value in self.probabilities]