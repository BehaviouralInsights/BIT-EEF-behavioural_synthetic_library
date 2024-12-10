"""Contains the class BasicTable, which serves as a base class for specific Table types.
"""

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
    """Abstract base class for all table types. Stores the heuristics for column type identification.

        Public methods:
            __init__: Abstract class constructor.
            delete_table: Deletes the private dataframe variable in order to save memory. Used by some subclasses.
            analyse: Abstract method.  Placeholder for subclass method analysing table properties.
            generate: Abstract method. Placeholder for subclass method generating a dataframe of synthetic data.
            dictionary_out: Abstract method. Placeholder for subclass method that outputs a description of the table in terms of column summary statistics.
            identify_variable_type: Contains heuristics used in automatically detecting column types.  Used by some subclasses.
    """
    
    @abstractmethod
    def __init__(self, table: pd.DataFrame, table_name: str, table_type: str):
        """Abstract constructor for tables.  
        
        Assigns table data to internal variables and strips whitespace from beginings and ends of strings.

        Args:
            table (pandas.DataFrame): Dataframe containing table from which sythetic data is to be generated.
            table_name (str): Name of the table.
            table_type (str): Type of the table.
        """
        
        self.TABLE_TYPE = table_type
        self.TABLE_NAME = table_name
        self.TABLE_ROWS = len(table.index)
        self.table = self.__strip_table_whitespace(table)
        
        
    def __strip_table_whitespace(self, table: pd.DataFrame) -> pd.DataFrame:
        """Private method for removing leading and trailing whitespace from strings in table.
        
        This locates variables in the table that might be strings, and strips leading and trailing whitespace from them using lambda functions.

        Args:
            table (pandas.DataFrame): Table data to be stripped.

        Returns:
            pandas.DataFrame: Stripped data.
        """
        
        for column in table.columns: # written to optimise memory
            column_data = table[[column]].copy(deep=True)
            column_data = column_data.map(lambda x: x.strip() if isinstance(x, str) else x)
            #cols = original_data.select_dtypes(['object']).columns
            if column_data[column].dtype == object:
                column_data = column_data.astype(str).apply(lambda x: x.str.strip())
            table[column]=column_data
            del [[column_data]] #delete working column from memory
            gc.collect() #garbage collect to make sure it's gone
        return table
             
    def delete_table(self):
        """Marks unneeded real table dataframe for deletion and calls the garbage collector.  Used by some subclasses."""
        
        del [[self.table]]
        gc.collect
        
    @abstractmethod
    def analyse(self, decimal_precision: int):
        """Abstract placeholder for public method for using heuristics to analyse a table.

        Args:
            decimal_precision (int): decimal precision of numerical columns in table.

        Raises:
            NotImplementedError: Is a placeholder method.
        """
        
        raise NotImplementedError
    
    @abstractmethod
    def generate(self, new_column_length: int) -> pd.DataFrame:
        """Abstract placeholder for public method for generating synthetic version of a table.

        Args:
            new_column_length (int): Number of rows in each column

        Raises:
            NotImplementedError: Is a placeholder method.

        Returns:
            pd.DataFrame: Dataframe containing synthetic data.
        """
        
        raise NotImplementedError
    
    @abstractmethod
    def dictionary_out(self) -> dict:
        """Abstract placeholder for public method outputting a dictionary description of a table.

        Raises:
            NotImplementedError: Is a placeholder method.

        Returns:
            dict: Dictionary containing a description of the table in terms of summary statistics.
        """
        
        raise NotImplementedError
    
    def __check_if_datetime(self, column: pd.Series) -> bool:
        """Private method defining the heuristic for detecting datetime

        Args:
            column (pandas.Series): Column data.

        Returns:
            bool: True if column is datetime, False otherwise.
        """
        
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
    
    def __check_if_numeric(self, column: pd.Series) -> bool:
        """Private method defining the heuristic for detecting numerical columns.

        Args:
            column (pandas.Series): Column data.

        Returns:
            bool: True if column is numeric, false if otherwise.
        """
        
        try:
            pd.to_numeric(column)
        except (RuntimeError, TypeError, NameError, IOError, ValueError):
            return False
        else:
            return True

    
    def identify_variable_type(self, column_name: str, decimal_precision: int) -> EmptyVariable | CategoricalVariable | StringVariable | NumericalVariable | DatetimeVariable:
        """Public method containing heuristics used to automatically identify column types and return an initialised column value of the appropriate type. Usually called by subclasses.
        
        A series of heuristic tests is applied in a specific order to a column, ruling out possibilities in turn.  If all identifications fail, the column is assumered to consist of strings.

        Args:
            column_name (str): Name of the column in the stored dataframe.
            decimal_precision (int): Numerical precision of numerical variables.

        Returns:
            EmptyVariable | CategoricalVariable | StringVariable | NumericalVariable | DatetimeVariable: Initialised column type value.
        """
        
        #TODO: Pull out the magic numbers and replace wit private constants.
        column = self.table[column_name]
        # Is the column empty? If so, it will be classified as 'NA':
        if (column.dropna().empty == True):
            return EmptyVariable(column)
        # Is the variable categorical? We check the number of unique values:
        if ((column.dropna().shape[0] >= 300 and column.dropna().nunique()<100) or (column.dropna().nunique()<len(column)*0.3 and column.dropna().shape[0] < 300)):
            return CategoricalVariable(column)
        # If no numbers are present, we classify it as a string:
        elif(column.astype(str).str.contains(r"[0-9]").any() == False):
            return StringVariable(column)
        # We then check if it's numeric, or predominantly numeric with some exceptions:
        elif(self.__check_if_numeric(column) == True): 
            type = NumericalVariable(column, decimal_precision)
            return type #NumericalVariable(column, decimal_precision)
        elif(column.astype(str).str.contains(r"[a-zA-Z]").any() == True and 
             column[column.astype(str).str.contains(r"[a-zA-Z]")].nunique()<11 and 
             self.__check_if_numeric(column[column.astype(str).str.contains(r"[^a-zA-Z]")]) == True):
            type = NumericalVariable(column, decimal_precision)
            return type # NumericalVariable(column, decimal_precision)
        # next, we check if it's a date or a time, or predominantly datetime with some exceptions:
        elif(self.__check_if_datetime(column) == True):
            return DatetimeVariable(column)
        elif(column.astype(str)[column.astype(str).str.contains(r"[0-9]") == False].nunique() < 11 and
             self.__check_if_datetime(column[column.astype(str).str.contains(r"[0-9]") == True]) == True):
            return DatetimeVariable(column)
        # If none of the above apply, we classify the variable as string:
        else:
            return StringVariable(column)
