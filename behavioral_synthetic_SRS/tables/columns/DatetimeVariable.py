from datetime import date
import gc
from typing import Dict, Union

import pandas as pd
import numpy as np
import random

from .VariableType import VariableType

class DatetimeVariable(VariableType):
    
    def __init__(self, column: pd.Series, average_min_max = True, date_format = "%Y-%m-%d", time_format = "%X", datetime_format = "%Y-%m-%d %X"):
        super().__init__(column, "datetime")
        self.average_min_max = average_min_max
        self.date_format = date_format
        self.time_format = time_format
        self.datetime_format = datetime_format
    
    def __average_earliest(self):
        earliest = min(self.column.dropna())
        earliest_times = self.column.dropna().nsmallest(n=self.THRESHOLD, keep='first')
        average_time_delta = earliest_times.map(lambda x: (x-earliest)/self.THRESHOLD).sum()
        return pd.to_datetime(earliest + average_time_delta)
    
    def __average_latest(self):
        latest = max(self.column.dropna())
        latest_times = self.column.dropna().nlargest(n=self.THRESHOLD, keep='first')
        average_time_delta = latest_times.map(lambda x: (x - latest)/self.THRESHOLD).sum()
        return pd.to_datetime(latest + average_time_delta)
    
        
    def analyse(self):
        
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
                
        #self.column = pd.to_datetime(self.column, errors = 'coerce', format='mixed') # mixed is 'risky' according to API, but also the only way to avoid a warning.  If there's a problem, check here first!
        self.column = pd.to_datetime(self.column, errors = 'coerce', infer_datetime_format=True)
        #print(self.column)
        self.length, self.missing, self.non_missing = super().analyse_missingness()
        
        if not self.average_min_max:
            self.t_earliest = min(self.column)
            self.t_latest = max(self.column)
        else:
            self.t_earliest = self.__average_earliest()
            self.t_latest = self.__average_latest()
            
        self.times_present = True if num_rows_with_times(self.column) > 0 else False
        self.dates_present = True if num_rows_with_dates(self.column) > 0 else False
        
        super()._delete_column()
        
    def generate(self, new_column_length: int) -> pd.Series:
        
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
        
        def impose_format(dtime: Union[pd.Timestamp, str], format: str) -> str:
            return 'nan' if dtime == 'nan' else dtime.strftime(format)
        
        if  (not self.times_present) and self.dates_present:
            new_column = new_column.map(lambda x: impose_format(x,self.date_format))
        elif self.times_present and (not self.dates_present):
            new_column = new_column.map(lambda x: impose_format(x,self.time_format))
        else:
            new_column = new_column.map(lambda x: impose_format(x, self.datetime_format))
                
        new_column.name = self.COLUMN_NAME
        
        return new_column.replace('nan', np.NaN)
    
    def dictionary_out(self) -> Dict:
        early = self.t_earliest
        late = self.t_latest
        type = "datetime"
        
        if  (not self.times_present) and self.dates_present:
            type = "date"
            return {"Name": self.COLUMN_NAME,"Type": type, "earliest": early.strftime(self.date_format), "latest": late.strftime(self.date_format), "missing_value_freq": round(self.missing/self.length, 7), "format": self.date_format, "averaged_max_and_min": self.average_min_max, "# of values in average_max_min": self.THRESHOLD }
        if self.times_present and (not self.dates_present):
            type = "time"
            return {"Name": self.COLUMN_NAME,"Type": type, "earliest": early.strftime(self.time_format), "latest": late.strftime(self.time_format), "missing_value_freq": round(self.missing/self.length, 7), "format": self.time_format, "averaged_max_and_min": self.average_min_max, "# of values in average_max_min": self.THRESHOLD}
        
        return {"Name": self.COLUMN_NAME,"Type": type, "earliest": early.strftime(self.datetime_format), "latest": late.strftime(self.datetime_format), "missing_value_freq": round(self.missing/self.length, 7), "format": self.datetime_format,"averaged_max_and_min": self.average_min_max, "# of values in average_max_min": self.THRESHOLD}
    
    def set(self, type: str, earliest: str, latest: str, missing_freq: float, number_of_rows: int, no_vals_in_threshold: int):
        
        self.length = number_of_rows
        self.missing = round(missing_freq*number_of_rows, 0)
        self.non_missing = round((1-missing_freq)*number_of_rows, 0)
        
    
        if type ==  'datetime':
            self.times_present = True
            self.dates_present = True
            self.t_earliest = pd.to_datetime(earliest, format=self.datetime_format)
            self.t_latest = pd.to_datetime(latest, format=self.datetime_format)   
        elif type ==  'time':
            self.times_present = True
            self.dates_present = False
            self.t_earliest = pd.to_datetime(earliest, format=self.time_format)
            self.t_latest = pd.to_datetime(latest, format=self.time_format)   
        elif type ==  'date':
            self.times_present = False
            self.dates_present = True
            self.t_earliest = pd.to_datetime(earliest, format=self.date_format)
            self.t_latest = pd.to_datetime(latest, format=self.date_format)  
        else:
            raise ValueError(rf'Invalid value of datetime parameter Type in column {self.COLUMN_NAME}.')
        
        if (no_vals_in_threshold < self.THRESHOLD):
            raise ValueError(f'Warning: external setting of threshold for averaging is {no_vals_in_threshold} but the internal value is {self.THRESHOLD}. The input is unsafe with respect to disclosure.')