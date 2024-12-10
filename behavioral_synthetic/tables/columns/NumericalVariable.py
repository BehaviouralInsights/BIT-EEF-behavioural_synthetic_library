"""Contains the class NumericalVariable, which generates synthetic data from numerical real data held in a pandas Series.
"""

import pandas as pd
import numpy as np

from .VariableType import VariableType

class NumericalVariable(VariableType):
    """Subclass extending VariableType.  Contains methods for producing a pandas series of synthetic numerical data from a pandas series of real numerical data.

        Public methods:
            __init__: Constructor.  Extends VariableType.__init__().
            analyse: Calculates summary statistics of the real data. Overrides VariableType.analyse().
            generate: Generates a column of synthetic data from the summary statistices.  Must be called after analyse() or set() methods.  Overrides VariableType.generate().
            dictionary_out: Outputs a dictionary containing column summary statistics. Must be called after analyse() or set() methods.  Overrides VariableType.dictionary_out().
            set: Sets table definitions that aren't set by the constructor.  Used to create column definitions from stored summary statistics.
            analyse_missingness: Calculates the number of missing and present values in the real data Series.  Inherited from VariableType.
            delete_column: Marks the pandas Series containing real data for deletion and calls the garbage collector. Inherited from VariableType.
    """
    
    def __init__(self, column: pd.Series, decimal_precision: int, average_min_max=True):
        """Constructor function for NumericalVariable, defining the properties of a numerical column.

        Passes column data to superclass constructor and sets column type to "numerical".  Sets the decimal precision and whether maximum and minimum values will be determined as usual or from averaging across a set of largest or smallest values respectively.
        
         Extends VariableType.__init__().

        Args:
            column (pandas.Series): The column from which synthetic data is to be generated.
            decimal_precision (int): The numerical precision of the output.
            average_min_max (bool, optional): Are the minimum and maximum values to be averaged from THRESHOLD (currently set to 10) values in line with typical disclosure practise (True) or from single values, which is permissible if there are structural reasons for the maximum and the minimum (False). Defaults to True.
        """
        
        super().__init__(column, "numeric")
        self.decimal_precision = decimal_precision
        self.average_min_max = average_min_max # do we average the max and minimum or not?
        
    def __average_min(self) -> float:
        """Private method generating an averaged minimum over the THRESHOLD smallest non-missing values.

        Returns:
            float: The averaged minimum.
        """
        
        if self.non_missing < self.get_THRESHOLD():
            raise ValueError(f'Insuffucient number of values in series to produce disclosure safe average minimum (less than {self.get_THRESHOLD()})')
        smallest = self.column.dropna().nsmallest(n=self.get_THRESHOLD(), keep='first')
        return smallest.mean()
    
    def __average_max(self):
        """Private method generating an averaged maximum over the THRESHOLD largest non-missing values.

        Returns:
            float: The averaged maximum.
        """
        
        if self.non_missing < self.get_THRESHOLD():
            raise ValueError(f'Insuffucient number of values in series to produce disclosure safe average maximum (less than {self.get_THRESHOLD()})')
        smallest = self.column.dropna().nlargest(n=self.get_THRESHOLD(), keep='first')
        return smallest.mean()
    
    def analyse(self):
        """Public method that extracts the summary statistics of the column and stores them internally.
        
        This tests that there are enough non-missing values to meet the disclosure threshold, and generates internal summary statistics describing the column data.  The orginal column is then marked for deletion and the garbage collector called.  Details of the summary statistics generated may be found in the documentation for the set() method.
        
        Overrides VariableType.analyse().
        """
        
        temp = pd.to_numeric(self.column, errors = "coerce" )
        self.column = temp.copy(deep=True)
        self.length, self.missing, self.non_missing = super().analyse_missingness()
        
        self.is_integer = True if str(self.column.dtypes) == 'int64' or all(y.is_integer() or pd.isnull(y) for y in self.column) else False
        self.decimal_precision = 0 if self.is_integer else self.decimal_precision
        
        # calculate numerical properties
        self.mean = self.column.dropna().mean()
        self.standard_deviation = self.column.dropna().std()
        if self.average_min_max:
            self.max_value = self.__average_max()
            self.min_value = self.__average_min()
        else:
            self.max_value = self.column.dropna().max()
            self.min_value = self.column.dropna().min()
        
        # enforce structural positivity and negativity of all values
        nrow_negative_values = self.column[self.column < 0].dropna().shape[0] 
        nrow_positive_values = self.column[self.column > 0].dropna().shape[0] 
        self.all_values_negative = True if (nrow_negative_values > 0 & nrow_positive_values == 0) else False
        self.all_values_positive = True if (nrow_positive_values > 0 & nrow_negative_values == 0) else False
        
        super().delete_column() # frees up memory.
        
    def generate(self, new_column_length: int) -> pd.Series:
        """Public method that generates a new column of synthetic data based on stored summary statistics.  Should be called after the analyse() or set() methods.
        
        Values are generated from the summary statistics according to the frequency of missing data and the mean and standard deviation of the non-missing data.  If all real data values were positive (negative), then values below (above) zero are truncated at the minimum (maximum) value.  If the real data was integer, it is converted to Int64 type, otherwise to Float64, and output in a pandas Series.

        Overrides VariableType.generate().

        Args:
            new_column_length (int): The number of rows required in the output column.

        Returns:
            Pandas.Series: A Pandas Series of float64 or Int64 dtype, depending on whether the input is real numbers or integers respectively.
        """
        
        # randomly reproduce missingness
        def random_numerical_selection(x_mean, x_sd, nrow_non_NA, nrow):
            rng = np.random.default_rng()
            probabilities=[nrow_non_NA/nrow, (nrow-nrow_non_NA)/nrow]
            values=[rng.normal(x_mean, x_sd), np.NaN]
            return rng.choice(values, p=probabilities)
        
        new_column = [random_numerical_selection(self.mean, self.standard_deviation, self.non_missing, self.length) for _ in range(new_column_length)]
        
        new_column = pd.Series(new_column)
        
        # impose structural positivity or negativitry on randomly generated values
        if self.all_values_negative:
            new_column.loc[(new_column > 0)] = self.max_value
        if self.all_values_positive:
            new_column.loc[(new_column < 0)] = self.min_value
            
        # impose caps on min/max
        new_column.loc[(new_column > self.max_value)] = self.max_value # this may enforce structural positivity and negativity by default, but will leave code for that in for now.
        new_column.loc[(new_column < self.min_value)] = self.min_value  
            
        new_column = new_column.replace(np.NaN, 'nan') # we do this because otherwise different NaN types cause a headache.
        
        # impose integerness or floatness on the column    
        if self.is_integer:
            new_column.fillna(pd.NA, inplace=True)
            new_column = new_column.map(lambda x: int(x) if x!='nan' else pd.NA)
            new_column = new_column.astype('Int64')
        else:
            new_column = new_column.map(lambda x: round(x, int(self.decimal_precision)) if x!='nan' else np.NaN)
            new_column = new_column.astype('float64')
            
        new_column.name=self.COLUMN_NAME
            
        return new_column
    
    def dictionary_out(self) -> dict:
        """Public method. Outputs a summary of the column summary statistics in dictionary format.   Should be called after the analyse() or set() methods.
        
        This creates a dictionary from the stored summary statistics and column parameters.
        
        Overrides VariableType.dictionary_out().

        Returns:
            dict: Summary of column properties. Floating point values are rounded at 7 decimal places.
        """
        
        return {"Name": self.COLUMN_NAME, "Type": "numeric", "decimal_precision": self.decimal_precision, "mean": round(self.mean,7), "standard_deviation": round(self.standard_deviation,7), "minimum": round(self.min_value,7), "maximum": round(self.max_value,7), "is_integer": self.is_integer, "missing_value_freq": round(self.missing/self.length, 7), "averaged_max_and_min": self.average_min_max, "# of values in average_max_min": self.get_THRESHOLD()}
    
    def set(self,  mean: float, standard_deviation: float, maximum: float, minimum: float, is_integer: bool, no_vals_in_threshold: int, missing_freq: float, number_of_rows: int):
        """Public method. Reads in a dictionary definition of column properties that are not set by the constructor.
        
        This reads in and/or converts the summary statistics to forms suitable for internal storage.


        Args:
            mean (float): mean value of non-missing column values.
            standard_deviation (float): standard deviation of non-missing column values.
            maximum (float): maximum value of non-missing column values (possibly averaged).
            minimum (float): minimum value of non-missing column values (possibly averaged).
            is_integer (bool): True if values are integers, False otherwise.
            no_vals_in_threshold (int): Number of values used to calculate average minimum and maximum if the average_min_max value passed to constructor is True.
            missing_freq (float): Proportion of values in column that are missing.
            number_of_rows (int): The number of rows in the original table.

        Raises:
            ValueError: If no_vals_in_threshold is lower than the internally set THRESHOLD value, this error is thrown as the input (and therefore potentially the output) is likely to be unsafe for disclosure.
        """
        
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.max_value = maximum
        self.min_value = minimum
        self.is_integer = is_integer
        
        self.all_values_negative = True if (minimum < 0 and maximum <= 0) else False # include both in case they accidentally get swapped by something!
        self.all_values_positive = True if (minimum >= 0 and maximum > 0) else False
        
        self.length = number_of_rows
        self.missing = round(missing_freq*number_of_rows, 0)
        self.non_missing = round((1-missing_freq)*number_of_rows, 0)
        
        if (no_vals_in_threshold < self.get_THRESHOLD()):
            raise ValueError(f'Warning: external setting of threshold for averaging is {no_vals_in_threshold} but the internal value is {self.get_THRESHOLD()}. The input is unsafe with respect to disclosure.')
    