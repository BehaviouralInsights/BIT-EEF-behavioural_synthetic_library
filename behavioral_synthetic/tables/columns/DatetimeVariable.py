"""Contains the class DatetimeVariable, which generates synthetic data from datetime data held in a pandas Series.
"""

from datetime import date
from datetime import datetime
import gc

import pandas as pd
import numpy as np
import random

from .VariableType import VariableType

class DatetimeVariable(VariableType):
    """Subclass extending VariableType. Contains methods for producing a pandas series of synthetic datetime data from a pandas series of real datetime data.

        Public methods:
            __init__: Constructor.  Extends VariableType.__init__().
            analyse: Calculates summary statistics of the real data. Overrides VariableType.analyse().
            generate: Generates a column of synthetic data from the summary statistices.  Must be called after analyse() or set() methods.  Overrides VariableType.generate().
            dictionary_out: Outputs a dictionary containing column summary statistics. Must be called after analyse() or set() methods.  Overrides VariableType.dictionary_out().
            set: Sets table definitions that aren't set by the constructor.  Used to create column definitions from stored summary statistics.
            analyse_missingness: Calculates the number of missing and present values in the real data Series.  Inherited from VariableType.
            delete_column: Marks the pandas Series containing real data for deletion and calls the garbage collector. Inherited from VariableType.
    """
    
    def __init__(self, column: pd.Series, average_min_max = True, date_format = "%Y-%m-%d", time_format = "%X", datetime_format = "%Y-%m-%d %X"):
        """Constructor for DatetimeVariable, defining the properties of a datetime column.
        
        Passes column data to the superclass constructor and sets the column type to "datetime" (this may be corrected to the "date" or "time" subtypes subsequently if required).  Determines whether lower and upper bounds of data need to be determined by averaging or not, and also sets the output format for each subtype "datetime", "date" or "time".
        
        Extends VariableType.__init__().

        Args:
            column (pandas.Series): Column data.
            average_min_max (bool, optional): Do maxima and minima get averaged. Defaults to True.
            date_format (str, optional): Format to use if the column is of 'date' subtype. Defaults to "%Y-%m-%d".
            time_format (str, optional): Format to use if the column is of 'time' subtype. Defaults to "%X".
            datetime_format (str, optional): Format to use if the column is of 'datetime' subtype. Defaults to "%Y-%m-%d %X".
        """
        
        super().__init__(column, "datetime")
        self.average_min_max = average_min_max
        self.date_format = date_format
        self.time_format = time_format
        self.datetime_format = datetime_format
    
    def __average_earliest(self) -> datetime:
        """Private method for averaging the earliest time in a column.

        Returns:
            datetime: Averaged earliest time.
        """
        
        earliest = min(self.column.dropna())
        earliest_times = self.column.dropna().nsmallest(n=self.get_THRESHOLD(), keep='first')
        average_time_delta = earliest_times.map(lambda x: (x-earliest)/self.get_THRESHOLD()).sum()
        return pd.to_datetime(earliest + average_time_delta)
    
    def __average_latest(self) -> datetime:
        """Private method for averaging the latest time in a column.

        Returns:
            datetime: Averaged latest time.
        """
        
        latest = max(self.column.dropna())
        latest_times = self.column.dropna().nlargest(n=self.get_THRESHOLD(), keep='first')
        average_time_delta = latest_times.map(lambda x: (x - latest)/self.get_THRESHOLD()).sum()
        return pd.to_datetime(latest + average_time_delta)
    
        
    def analyse(self):
        """Public method that extracts the summary statistics of the column and stores them internally as a frequency table for each value.
        
        This tests that there are enough non-missing values to meet the disclosure threshold through a call to analyse_missingness(), and generates an earliest and latest time either through finding the smallest and largest values or by averaging a set of the smallest and largest values respectively.  It then checks whether both dates and times are present in the data. Details of the summary statistics generated may be found in the documentation for the set() method.
        
        Overrides VariableType.analyse().
        """
        
        def num_rows_with_times(column: pd.Series) -> int:
            just_time = column.dt.time.dropna().astype(str)
            # (if no times were in the original column, pandas will set it to midnight)
            return just_time[(just_time != '00:00:00')].shape[0] # if this is more than 0, then we have (some) times
        
        def num_rows_with_dates(column: pd.Series) -> int:
            just_date = column.dt.date
            # (if no dates were in the original column, pandas will attach today's date)
            todays_date = date.today() 
            todays_date = '{:%Y-%m-%d}'.format(todays_date)
            just_date = just_date.dropna().astype(str)
            return just_date[(just_date != todays_date)].shape[0] # if this is more than 0, then we have (some) dates
                
        self.column = pd.to_datetime(self.column, errors = 'coerce', format='mixed') # mixed is 'risky' according to API, but also the only way to avoid a warning.  If there's a problem, check here first!
        self.length, self.missing, self.non_missing = super().analyse_missingness()
        
        if not self.average_min_max:
            self.t_earliest = min(self.column)
            self.t_latest = max(self.column)
        else:
            self.t_earliest = self.__average_earliest()
            self.t_latest = self.__average_latest()
            
        self.times_present = True if num_rows_with_times(self.column) > 0 else False
        self.dates_present = True if num_rows_with_dates(self.column) > 0 else False
        
        super().delete_column()
        
    def generate(self, new_column_length: int) -> pd.Series:
        """Public method that generates a new column of synthetic data based on stored summary statistics.  Should be called after the analyse() or set() methods.
        
        Synthetic dates, times or datetimes are determined by randomly choosing dates between an earliest and latest value with a chance of any given value being missing.  These are converted into strings whose format depends on which of the three subtypes the real data contains, and output as a pandas Series.
        
        Overrides VariableType.generate()
        
        Args:
            new_column_length (int): Number of rows of synthetic data to generate.

        Returns:
            pd.Series: Column containing synthetic data.
        """
        
        def generate_datetime(min_time, max_time):
            start = pd.to_datetime(min_time)
            end = pd.to_datetime(max_time)
            random_date = start + (end - start) * random.random()
            return random_date
        
        def random_datetime_selection(min_time,max_time, nrow_non_NA, nrow):
            probabilities=[nrow_non_NA/nrow, (nrow-nrow_non_NA)/nrow]
            values=[generate_datetime(min_time, max_time), np.NaN]
            return np.random.choice(values, p=probabilities)
        
        new_column = pd.Series([random_datetime_selection(self.t_earliest, self.t_latest, self.non_missing, self.length) for _ in range(new_column_length)])
        
        new_column = new_column.astype('object')
        new_column = new_column.fillna('nan').replace(pd.NaT, 'nan')
        
        def impose_format(dtime: pd.Timestamp | str, format: str) -> str:
            return 'nan' if dtime == 'nan' else dtime.strftime(format)
        
        if  (not self.times_present) and self.dates_present:
            new_column = new_column.map(lambda x: impose_format(x,self.date_format))
        elif self.times_present and (not self.dates_present):
            new_column = new_column.map(lambda x: impose_format(x,self.time_format))
        else:
            new_column = new_column.map(lambda x: impose_format(x, self.datetime_format))
                
        new_column.name = self.COLUMN_NAME
        
        return new_column.replace('nan', np.NaN)
    
    def dictionary_out(self) -> dict:
        """Public method. Outputs a summary of the column summary statistics in dictionary format.   Should be called after the analyse() or set() methods.
        
        This creates a dictionary from the stored summary statistics and column parameters.
        
        Overrides VariableType.dictionary_out().

        Returns:
            dict: Summary of column properties.
        """
            
        early = self.t_earliest
        late = self.t_latest
        type = "datetime"
        
        if  (not self.times_present) and self.dates_present:
            type = "date"
            return {"Name": self.COLUMN_NAME,"Type": type, "earliest": early.strftime(self.date_format), "latest": late.strftime(self.date_format), "missing_value_freq": round(self.missing/self.length, 7), "format": self.date_format, "averaged_max_and_min": self.average_min_max, "# of values in average_max_min": self.get_THRESHOLD() }
        if self.times_present and (not self.dates_present):
            type = "time"
            return {"Name": self.COLUMN_NAME,"Type": type, "earliest": early.strftime(self.time_format), "latest": late.strftime(self.time_format), "missing_value_freq": round(self.missing/self.length, 7), "format": self.time_format, "averaged_max_and_min": self.average_min_max, "# of values in average_max_min": self.get_THRESHOLD()}
        
        return {"Name": self.COLUMN_NAME,"Type": type, "earliest": early.strftime(self.datetime_format), "latest": late.strftime(self.datetime_format), "missing_value_freq": round(self.missing/self.length, 7), "format": self.datetime_format,"averaged_max_and_min": self.average_min_max, "# of values in average_max_min": self.get_THRESHOLD()}
    
    def set(self, type: str, earliest: str, latest: str, missing_freq: float, number_of_rows: int, no_vals_in_threshold: int):
        """Public method. Reads in a dictionary definition of column properties that are not set by the constructor.
        
        This reads in and/or converts the summary statistics to forms suitable for internal storage.

        Args:
            type (str): 'date', 'time' or 'datetime'.
            earliest (str): Earliest time in column (possibly an average).
            latest (str): Latest time in column (possibly an average).
            missing_freq (float): Frequency of missing values.
            number_of_rows (int): Number of rows present in original table
            no_vals_in_threshold (int): Number of values used to calculate average minimum and maximum if the average_min_max value passed to constructor is True.

        Raises:
            ValueError: If type is not set to 'date', 'time' or 'datetime'.
            ValueError: If no_vals_in_threshold is lower than the internally set THRESHOLD value, this error is thrown as the input (and therefore potentially the output) is likely to be unsafe for disclosure.
        """
        
        self.length = number_of_rows
        self.missing = round(missing_freq*number_of_rows, 0)
        self.non_missing = round((1-missing_freq)*number_of_rows, 0)
        
        match type:
            case 'datetime':
                self.times_present = True
                self.dates_present = True
                self.t_earliest = pd.to_datetime(earliest, format=self.datetime_format)
                self.t_latest = pd.to_datetime(latest, format=self.datetime_format)   
            case 'time':
                self.times_present = True
                self.dates_present = False
                self.t_earliest = pd.to_datetime(earliest, format=self.time_format)
                self.t_latest = pd.to_datetime(latest, format=self.time_format)   
            case 'date':
                self.times_present = False
                self.dates_present = True
                self.t_earliest = pd.to_datetime(earliest, format=self.date_format)
                self.t_latest = pd.to_datetime(latest, format=self.date_format)  
            case _:
                raise ValueError(rf'Invalid value of datetime parameter Type in column {self.COLUMN_NAME}.')
        
        if (no_vals_in_threshold < self.get_THRESHOLD()):
            raise ValueError(f'Warning: external setting of threshold for averaging is {no_vals_in_threshold} but the internal value is {self.get_THRESHOLD()}. The input is unsafe with respect to disclosure.')