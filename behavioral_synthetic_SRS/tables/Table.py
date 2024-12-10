import gc

import pandas as pd
from typing import Dict, List

from .BasicTable import BasicTable

from .columns.NumericalVariable import NumericalVariable
from .columns.CategoricalVariable import CategoricalVariable
from .columns.DatetimeVariable import DatetimeVariable
from .columns.EmptyVariable import EmptyVariable
from .columns.StringVariable import StringVariable

class Table(BasicTable):
    
    def __init__(self, table: pd.DataFrame, table_name: str):
        super().__init__(table, table_name, 'normal_table')
        
    def analyse(self, decimal_accuracy: int):
        self.column_types = []
        for column in self.table.columns:
            column_type = super()._identify_variable_type(column, decimal_accuracy)
            column_type.analyse()
            self.column_types.append(column_type)
            
    def generate(self, new_column_length: int) -> pd.DataFrame:
        new_table = pd.DataFrame()
        for column in self.column_types:
            column_data = column.generate(new_column_length)
            new_table[column_data.name] = column_data
            del [[column_data]]
            gc.collect()
            
        return new_table
    
    def dictionary_out(self) -> Dict:
        dictionary = {
            "Table_name": self.TABLE_NAME,
            "Table_type": self.TABLE_TYPE,
            "Number_of_rows": self.TABLE_ROWS,
            "Column_details" : []
            }
        
        for column in self.column_types:
            dictionary["Column_details"].append(column.dictionary_out())
            
        return dictionary
    
    def read_in_table(self,table_definition: Dict):
        self.TABLE_NAME = table_definition["Table_name"]
        self.TABLE_TYPE = table_definition["Table_type"]
        self.TABLE_ROWS = table_definition["Number_of_rows"]
        
        self.column_types = [] 
        for column in table_definition["Column_details"]:
            temp_column = pd.Series(dtype='object')
            if column['Type'] ==  'empty':
                temp_column = EmptyVariable(pd.Series([0], name=column["Name"]))
            elif column['Type'] ==  'numeric':
                temp_column = NumericalVariable(
                    pd.Series([0], name=column['Name']),
                    decimal_precision = column['decimal_precision'],
                    average_min_max = column['averaged_max_and_min'],
                    )
                temp_column.set(
                    mean = column['mean'],
                    standard_deviation = column['standard_deviation'],
                    maximum = column['maximum'],
                    minimum = column['minimum'],
                    is_integer = column['is_integer'],
                    no_vals_in_threshold = column['# of values in average_max_min'],
                    missing_freq = column["missing_value_freq"],
                    number_of_rows = self.TABLE_ROWS
                )
            elif column['Type'] ==  'categorical':
                temp_column = CategoricalVariable(pd.Series([0], name = column["Name"]))
                temp_column.set(
                    {value: column[value] for value in column.keys() if value not in ['Type','Name']}
                )
            elif column['Type'] ==  'date':
                if column['format']:
                    temp_column = DatetimeVariable(pd.Series([0], name = column["Name"]), average_min_max=column['averaged_max_and_min'], date_format=column['format'])
                else:
                    temp_column = DatetimeVariable(pd.Series([0], name = column["Name"]),average_min_max=column['averaged_max_and_min'])
                temp_column.set(
                    type = column['Type'],
                    earliest = column["earliest"],
                    latest = column["latest"],
                    missing_freq = column["missing_value_freq"],
                    number_of_rows = self.TABLE_ROWS,
                    no_vals_in_threshold = column['# of values in average_max_min']
                )
            elif column['Type'] ==  'datetime':
                if column['format']:
                    temp_column = DatetimeVariable(pd.Series([0], name = column["Name"]), average_min_max=column['averaged_max_and_min'], datetime_format=column['format'])
                else:
                    temp_column = DatetimeVariable(pd.Series([0], name = column["Name"]), average_min_max=column['averaged_max_and_min'])
                temp_column.set(
                    type = column['Type'],
                    earliest = column["earliest"],
                    latest = column["latest"],
                    missing_freq = column["missing_value_freq"],
                    number_of_rows = self.TABLE_ROWS,
                    no_vals_in_threshold = column['# of values in average_max_min']
                )                   
            elif column['Type'] ==  'time':
                if column['format']:
                    temp_column = DatetimeVariable(pd.Series([0], name = column["Name"]), average_min_max=column['averaged_max_and_min'], time_format=column['format'])
                else:
                    temp_column = DatetimeVariable(pd.Series([0], name = column["Name"]),average_min_max=column['averaged_max_and_min'])
                temp_column.set(
                    type = column['Type'],
                    earliest = column["earliest"],
                    latest = column["latest"],
                    missing_freq = column["missing_value_freq"],
                    number_of_rows = self.TABLE_ROWS,
                    no_vals_in_threshold = column['# of values in average_max_min']
                )
            elif column['Type'] ==  'text':
                temp_column = StringVariable(pd.Series([0], name = column["Name"]))
                if column['Pattern']==True:
                    temp_column.set_pattern(
                        pattern = column["Pattern"],
                        character_frequencies = {value: column[value] for value in column if "character_number_" in value},
                        max_length = column["Max_length"],
                        missing_freq = column["missing_value_freq"],
                        number_of_rows = self.TABLE_ROWS
                    )
                elif column['Pattern']==False:
                    temp_column.set_no_pattern(
                        pattern = column["Pattern"],
                        min_length = column["Min_length"],
                        max_length = column["Max_length"],
                        missing_freq = column["missing_value_freq"],
                        number_of_rows = self.TABLE_ROWS
                    )
                else:
                    raise ValueError(f"Pattern value in column {column['Name']} is neither true or false.")
            else:
                raise ValueError(f"Type of column {column['Name']} is {column['Type']}: this is not an allowed value.")
                
            self.column_types.append(temp_column)
    
    def analyse_with_column_list(self, columns_list: List[Dict]) :
        self.column_types = []
        for i, column in enumerate(self.table.columns):
            column_type = self._assign_variable_type(columns_list[i], self.table[column])
            column_type.analyse()
            self.column_types.append(column_type)
        
    def _assign_variable_type(self, column_data: Dict, column: pd.Series):
        
        def to_bool(variable):
            if variable == "True":
                return True
            elif variable == "False":
                return False
            else:
                return variable

        if column_data['Type'] == 'empty':
            return EmptyVariable(column)
        elif column_data['Type'] == 'numeric':
            return NumericalVariable(
                column,
                decimal_precision = column_data['decimal_precision'],
                average_min_max = to_bool(column_data['averaged_max_and_min'])
            )
        elif column_data['Type'] == 'categorical':
            return CategoricalVariable(column)
        elif column_data['Type'] == 'datetime':
            if column_data['format']:
                return DatetimeVariable(
                    column, 
                    datetime_format=column_data['format'],
                    average_min_max = to_bool(column_data['averaged_max_and_min'])
                    )
            else:
                return DatetimeVariable(column, average_min_max = to_bool(column_data['averaged_max_and_min']))
        elif column_data['Type'] ==  'date':
            if column_data['format']:
                return DatetimeVariable(
                    column, 
                    date_format=column_data['format'],
                    average_min_max = to_bool(column_data['averaged_max_and_min'])
                    )
            else:
                return DatetimeVariable(column, average_min_max = to_bool(column_data['averaged_max_and_min']))
        elif column_data['Type'] ==  'time':
            if column_data['format']:
                return DatetimeVariable(
                    column, 
                    time_format=column_data['format'],
                    average_min_max = to_bool(column_data['averaged_max_and_min'])
                    )
            else:
                return DatetimeVariable(column,average_min_max = to_bool(column_data['averaged_max_and_min']))            
        elif column_data['Type'] ==  'text':
            return StringVariable(column)
        else:
            raise ValueError(f"Type of column {column.name} is defined as {column_data['Type']}: this is not an allowed value.")
                