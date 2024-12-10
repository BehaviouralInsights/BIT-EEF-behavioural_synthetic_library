from typing import Dict

import pandas as pd
import numpy as np

from .VariableType import VariableType

class NumericalVariable(VariableType):
    """Class defining the NumericalVariable datatype, which processes real data and generates synthetic data for a numerical column of a table.

    Args:
        VariableType (abstract): Base class.
        
    Raises:
        ValueError: If the number of non-null entries in a column is less than the disclosure variable THRESHOLD when calculating the average minimum.
        ValueError: If the number of non-null entries in a column is less than the disclosure variable THRESHOLD when calculating the average maximum. 
        
        THRESHOLD is defined in the base VariableType class.    
    """
    
    def __init__(self, column: pd.Series, decimal_precision: int, average_min_max=True, disclosure = True):
        """Constructor function for NumericalVariable, defining the properties of a numerical column.

        Args:
            column (pandas.Series): The column from which synthetic data is to be generated.
            decimal_precision (int): The numerical precision of the output.
            average_min_max (bool, optional): Are the minimum and maximum values to be averaged from THRESHOLD (currently set to 10) values in line with typical disclosure practise (True) or from single values, which is permissible if there are structural reasons for the maximum and the minimum (False). Defaults to True.
        """
        super().__init__(column, "numeric")
        self.decimal_precision = decimal_precision
        self.average_min_max = average_min_max # do we average the max and minimum or not?
        self.disclosure = disclosure
        
    def _average_min(self) -> float:
        """Private method generating an averaged minimum over the THRESHOLD smallest non-missing values.

        Returns:
            float: The averaged minimum.
        """
        if self.non_missing < self.THRESHOLD:
            raise ValueError(f'Insuffucient number of values in series to produce disclosure safe average minimum (less than {self.THRESHOLD})')
        smallest = self.column.dropna().nsmallest(n=self.THRESHOLD, keep='first')
        return smallest.mean()
    
    def _average_max(self):
        """Private method generating an averaged maximum over the THRESHOLD largest non-missing values.

        Returns:
            float: The averaged maximum.
        """
        if self.non_missing < self.THRESHOLD:
            raise ValueError(f'Insuffucient number of values in series to produce disclosure safe average maximum (less than {self.THRESHOLD})')
        smallest = self.column.dropna().nlargest(n=self.THRESHOLD, keep='first')
        return smallest.mean()
    
    def analyse(self):
        """Public method that extracts the properties of the column and stores them internally.
        
        Extracts mean, standad deviation, maximum and minimum, as well as missingness values.
        """
        temp = pd.to_numeric(self.column, errors = "coerce" )
        self.column = temp.copy(deep=True)
        self.length, self.missing, self.non_missing = super().analyse_missingness()
        
        self.is_integer = True if str(self.column.dtypes) == 'Int64' or all([isinstance(y, int) or pd.isnull(y) for y in self.column]) else False
        self.decimal_precision = 0 if self.is_integer else self.decimal_precision
        
        # calculate numerical properties
        self.mean = self.column.dropna().mean()
        self.standard_deviation = self.column.dropna().std()
        if self.average_min_max:
            self.max_value = self._average_max()
            self.min_value = self._average_min()
        else:
            self.max_value = self.column.dropna().max()
            self.min_value = self.column.dropna().min()
        
        # enforce structural positivity and negativity of all values
        nrow_negative_values = self.column[self.column < 0].dropna().shape[0] 
        nrow_positive_values = self.column[self.column > 0].dropna().shape[0] 
        self.all_values_negative = True if (nrow_negative_values > 0 & nrow_positive_values == 0) else False
        self.all_values_positive = True if (nrow_positive_values > 0 & nrow_negative_values == 0) else False
        
        super()._delete_column() # frees up memory.
        
    def generate(self, new_column_length: int) -> pd.Series:
        """Public method that generates a new column of synthetic data based on the properties obtained by the analyse() method.  Should be called *after* analyse().

        This is done by randomly generating non-missing values from the probabiltiy distribution given by the mean and standard deviation; missing values have a chance of occuring equal to that in the original data.

        Args:
            new_column_length (int): The number of rows required in the output column.

        Returns:
            Pandas.Series: A Pandas Series of Float64 or Int64 dtype, depending on whether the input is real numbers or integers respectively.
        """
        
        # randomly reproduce missingness
        def random_numerical_selection(x_mean, x_sd, nrow_non_NA, nrow):
            probabilities=[nrow_non_NA/nrow, (nrow-nrow_non_NA)/nrow]
            values=[np.random.normal(x_mean, x_sd), np.NaN]
            return np.random.choice(values, p=probabilities)
        
        new_column = [random_numerical_selection(self.mean, self.standard_deviation, self.non_missing, self.length) for _ in range(new_column_length)]
        
        new_column = pd.Series(new_column)
        
        # impose structural positivity or negativitry on randomly generated values
        if self.all_values_negative:
            new_column.loc[(new_column > 0)] = self.max_value
        if self.all_values_positive:
            new_column.loc[(new_column < 0)] = self.min_value
            
        new_column = new_column.replace(np.NaN, 'nan') # we do this because otherwise different NaN types cause a headache.
        
        # impose integerness or floatness on the column    
        if self.is_integer:
            new_column.fillna(pd.NA, inplace=True)
            new_column = new_column.map(lambda x: int(x) if x!='nan' else pd.NA)
            new_column = new_column.astype('Int64')
        else:
            new_column = new_column.map(lambda x: round(x, self.decimal_precision) if x!='nan' else np.NaN)
            new_column = new_column.astype('Float64')
            
        new_column.name=self.COLUMN_NAME
            
        return new_column
    
    def dictionary_out(self) -> Dict:
        """Outputs a summary of the column properties in dictionary format.  Should be called *after* analyse().

        Returns:
            dict: Summary of column properties. Floating point values are rounded at 7 decimal places.
        """
        dictionary = {
            "Name": self.COLUMN_NAME, "Type": "numeric", "decimal_precision": self.decimal_precision, 
            "mean": round(self.mean,7), "standard_deviation": round(self.standard_deviation,7), 
            "minimum": round(self.min_value,7), "maximum": round(self.max_value,7), 
            "is_integer": self.is_integer, "missing_value_freq": round(self.missing/self.length, 7), 
            "averaged_max_and_min": self.average_min_max, "# of values in average_max_min": self.THRESHOLD}
        
        if self.disclosure:
            dictionary["count for mean/standard deviation"] = int(self.non_missing)
            dictionary["count for missing"] = int(self.missing)
            dictionary["Disclosure"] = self.disclosure
            #dictionary["Note"]= "Missing values probably aren't disclosive."
            if dictionary["count for missing"] < self.THRESHOLD:
                dictionary["missing_value_freq"] = round(0.0,7)
                dictionary["count for missing"] = None
            
        return dictionary   
    
    def set(self,  mean: float, standard_deviation: float, maximum: float, minimum: float, is_integer: bool, no_vals_in_threshold: int, missing_freq: float, number_of_rows: int):
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.max_value = maximum
        self.min_value = minimum
        self.is_integer = is_integer
        
        self.length = number_of_rows
        self.missing = round(missing_freq*number_of_rows, 0)
        self.non_missing = round((1-missing_freq)*number_of_rows, 0)
        
        if (no_vals_in_threshold < self.THRESHOLD):
            raise ValueError(f'Warning: external setting of threshold for averaging is {no_vals_in_threshold} but the internal value is {self.THRESHOLD}. The input is unsafe with respect to disclosure.')
    