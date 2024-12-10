from abc import ABC, abstractmethod
import gc
import warnings


import pandas as pd

from .columns.NumericalVariable import NumericalVariable
from .columns.CategoricalVariable import CategoricalVariable
from .columns.DatetimeVariable import DatetimeVariable
from .columns.EmptyVariable import EmptyVariable
from .columns.StringVariable import StringVariable

class BasicTable(ABC):
    
    @abstractmethod
    def __init__(self, table: pd.DataFrame, table_name: str, table_type: str):
        self.TABLE_TYPE = table_type
        self.TABLE_NAME = table_name
        self.TABLE_ROWS = len(table.index)
        self.table = self._strip_table_whitespace(table)
        
        
    def _strip_table_whitespace(self, table: pd.DataFrame) -> pd.DataFrame:
        for column in table.columns: # written to optimise memory
            column_data = table[[column]].copy(deep=True)
            #column_data = column_data.map(lambda x: x.strip() if isinstance(x, str) else x)
            column_data = column_data.apply(lambda x: x.strip() if isinstance(x, str) else x)
            #cols = original_data.select_dtypes(['object']).columns
            if column_data[column].dtype == object:
                column_data = column_data.astype(str).apply(lambda x: x.str.strip())
            table[column]=column_data
            del [[column_data]] #delete working column from memory
            gc.collect() #garbage collect to make sure it's gone
        return table
             
    def delete_table(self):
        del [[self.table]]
        gc.collect
        
    @abstractmethod
    def analyse(self, decimal_precision: int):
        raise NotImplementedError
    
    @abstractmethod
    def generate(self, new_column_length: int) -> pd.DataFrame:
        raise NotImplementedError
    
    @abstractmethod
    def dictionary_out(self) -> dict:
        raise NotImplementedError
    
    def _check_if_datetime(self, column):
        try:
            # this would normally issue "UserWarning: Could not infer format, so each element will be parsed individually, falling back to `dateutil`. To ensure parsing is consistent and as-expected, please specify a format."
            # However, we're only interested in whether it thinks the column as a whole is datetime rather than parsing specific values so we can suppress this without worry.
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                pd.to_datetime(column)
        except (RuntimeError, TypeError, NameError, IOError, ValueError):
            return False
        else:
            return True
    
    def _check_if_numeric(self, column):
        try:
            pd.to_numeric(column)
        except (RuntimeError, TypeError, NameError, IOError, ValueError):
            return False
        else:
            return True

    
    def _identify_variable_type(self, column_name, decimal_precision):
        
        column = self.table[column_name]
        # Is the column empty? If so, it will be classified as 'NA':
        if (column.dropna().empty == True):
            return EmptyVariable(column)
        # Is the variable categorical? We check the number of unique values:
        #if ((column.dropna().shape[0] >= 300 and column.dropna().nunique()<100) or (column.dropna().nunique()<len(column)*0.3 and column.dropna().shape[0] < 300)):
        #if ((column.dropna().shape[0] >= 300 and column.dropna().nunique()<270) or (column.dropna().nunique()<len(column)*0.9 and column.dropna().shape[0] < 300)):
        if column.dropna().nunique()<len(column)*0.3:
            return CategoricalVariable(column)
        # If no numbers are present, we classify it as a string:
        elif(column.astype(str).str.contains(r"[0-9]").any() == False):
            return StringVariable(column)
        # We then check if it's numeric, or predominantly numeric with some exceptions:
        elif(self._check_if_numeric(column) == True): 
            type = NumericalVariable(column, decimal_precision)
            return type #NumericalVariable(column, decimal_precision)
        elif(column.astype(str).str.contains(r"[a-zA-Z]").any() == True and 
             column[column.astype(str).str.contains(r"[a-zA-Z]")].nunique()<11 and 
             self._check_if_numeric(column[column.astype(str).str.contains(r"[^a-zA-Z]")]) == True):
            type = NumericalVariable(column, decimal_precision)
            return type # NumericalVariable(column, decimal_precision)
        # next, we check if it's a date or a time, or predominantly datetime with some exceptions:
        elif(self._check_if_datetime(column) == True):
            return DatetimeVariable(column)
        elif(column.astype(str)[column.astype(str).str.contains(r"[0-9]") == False].nunique() < 11 and
             self._check_if_datetime(column[column.astype(str).str.contains(r"[0-9]") == True]) == True):
            return DatetimeVariable(column)
        # If none of the above apply, we classify the variable as string:
        else:
            return StringVariable(column)
