import gc
from typing import Dict, Union

import pandas as pd
import numpy as np

from .VariableType import VariableType

class CategoricalVariable(VariableType):
    """Class defining the NumericalVariable datatype, which processes real data and generates synthetic data for a numerical column of a table.

    Args:
        VariableType (abstract): Base class.
        
    Raises:
        ValueError: If the number of non-null and non-blank entries in a column is less than the disclosure variable THRESHOLD.
        
        THRESHOLD is defined in the base VariableType class.
    """
    def __init__(self, column: pd.Series, disclosure = True):
        """Constructor function for Categorical Variable, defining the properties of a categorical column.

        Args:
            column (pandas.Series): The column from which synthetic data is to be generated.
        """
        super().__init__(column, "categorical")
        self.dtypes = column.dtypes
        self.disclosure = disclosure
        self.column_size = column.size
           
    def analyse(self):
        """Public method that extracts the properties of the column and stores them internally as a frequency table for each value.

        Raises:
            ValueError: If the number of non-null and non-blank entries in a column is less than the disclosure variable THRESHOLD.
        """
        
        # note we don't need to analyse for missingness as this will automatically account for it
        self.column=self.column.astype('object')
        
        if self.column.replace("", np.NaN).dropna().size < self.THRESHOLD:
            raise ValueError(f'Insuffucient number of values in series to produce disclosure safe results (less than {self.THRESHOLD})')
        
        self.column.fillna('nan', inplace=True)
        cross_tabulation = self.column.value_counts(dropna = False, normalize=True)
        self.values = cross_tabulation.axes[0].tolist()
        self.probabilities = cross_tabulation.tolist()
        
        if self.disclosure:
            # primary disclosure  (eliminate small counts)
            self.count = [self.column_size*prob for prob in self.probabilities]
            for i, value in enumerate(self.values):
               # if value !='nan':
                if self.probabilities[i] < self.THRESHOLD/self.column.size:
                    self.probabilities[i] = 0.0
                    self.count[i] = None
                        
            # secondary disclosure (renormalise in absences of small counts)
        
            total_prob = sum(self.probabilities)
            if total_prob == 0.0:
                pass
            else:
                #total_prob = sum(self.probabilities)
                new_probs = [prob/total_prob for prob in self.probabilities]
                self.probabilities = new_probs
            
        
        super()._delete_column()
        
    def generate(self, new_column_length: int) -> pd.Series:
        """Public method that generates a new column of synthetic data based on the properties obtained by the analyse() method.  Should be called *after* analyse().
        
        Values are randomly drawn with replacement from a frequency table that includes missing values.

        Args:
            new_column_length (int): The number of rows required in the output column.

        Returns:
            Pandas.Series: A Pandas Series of object, float64 or Int64 dtype, depending on the properties of the original column.
        """
        new_column = pd.Series(np.random.choice(self.values, new_column_length,  p=self.probabilities)).replace('nan', np.NaN)
        new_column.name = self.COLUMN_NAME
        new_column = new_column.astype(str(self.dtypes))
        return new_column
    
    def dictionary_out(self) -> Dict:
        """Outputs a summary of the column properties in dictionary format.  Should be called *after* analyse().

        Returns:
            dict: Summary of column properties. Floating point values are rounded at 7 decimal places."""
        dictionary = dict(zip(self.values, [round(p,7) for p in self.probabilities]))
        dictionary['Type'] = 'categorical'
        dictionary['Name'] = self.COLUMN_NAME
        
            
        
        if self.disclosure:
            dictionary['Counts'] = dict(zip(self.values, [round(c,7) if c is not None else c for c in self.count]))
            dictionary['Disclosure'] = self.disclosure
            dictionary['Note'] = f"All values with a frequency of less than {self.THRESHOLD/self.column_size} have had that frequency repressed (here, set to zero), and the frequencies have been recalculated to prevent secondary disclosure." 
            #" 'nan' values are not considered disclosive."
        
        return dictionary
    
    def set(self, frequencies: Dict[Union[str, int], float]):
        self.values = [ value for value in frequencies.keys()]
        self.probabilities = [frequencies[value] for value in frequencies]