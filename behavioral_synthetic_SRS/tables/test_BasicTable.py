import pandas as pd
import numpy as np
import re
import pytest


from .BasicTable import BasicTable
#rom columns.EmptyVariable import EmptyVariable

#dummy class so we can call abstracted functions
class dummy_class(BasicTable):
    
    def __init__(self, table: pd.DataFrame, table_name: str, table_type: str):
        super().__init__(table, table_name, table_type)
        
    def analyse(self, decimal_precision: int):
        return super().analyse(decimal_precision)
    
    def generate(self, new_column_length: int) -> pd.DataFrame:
        return super().generate(new_column_length)
    
    def dictionary_out(self) -> dict:
        return super().dictionary_out()
    
    def analyse_column(self, column_name:str) -> str:
        column = super()._identify_variable_type(column_name, decimal_precision=2)
        return column.COLUMN_TYPE #()
    
""" class MockCategorical():
    def  __init__(self, column: pd.Series):
        pass #self.column_type = 'categorical'
        
    def column_type(self):
        return 'categorical'
        
class MockDatetime():
    def __init__(self, column: pd.Series):
        self.column_type = 'datetime'
        
class MockEmpty():
    def __init__(self, column: pd.Series):
        self.column_type = 'empty'
    
    #def column_type(self):
       # return 'empty'
        
class MockString():
    def __init__(self, column: pd.Series):
        self.column_type = 'string'
        
class MockNumerical():
    def __init__(self, column: pd.Series, decimal_precision:int):
        self.column_type = 'numerical' """
        
        
        
class TestBasicTable():
    
    test_table =
    
    def test_identify_variable_type(self, monkeypatch):
        table = dummy_class(self.test_table, table_name='test_table', table_type='test_table_type')
    
        
        #monkeypatch.setattr("columns.EmptyVariable.EmptyVariable", MockEmpty)
        #monkeypatch.setattr("columns.CategoricalVariable.CategoricalVariable", MockCategorical)
        #monkeypatch.setattr("columns.NumericalVariable.NumericalVariable", MockNumerical)
        #monkeypatch.setattr("columns.StringVariable.StringVariable", MockString)
        #monkeypatch.setattr("columns.DatetimeVariable.DatetimeVariable", MockDatetime)
        
        column_type = {}
        for column_name in self.test_table.columns:
            column_type[column_name] = table.analyse_column(column_name)
        
        example_column_types = {
            "A": "empty",
            "B": "categorical",
            "C": "categorical",
            "D": "numeric",
            "E": "string",
            "F": "datetime"
            }
        
        assert column_type == example_column_types
        
    def test_delete_table(self):
        table = dummy_class(self.test_table, table_name='test_table', table_type='test_table_type')
        table.delete_table()
        with pytest.raises(AttributeError, match=re.escape("'dummy_class' object has no attribute 'table'")):
            table.table
            
    
    def test_analyse(self):
        table = dummy_class(self.test_table, table_name='test_table', table_type='test_table_type')
        with pytest.raises(NotImplementedError):
            table.analyse(decimal_precision=2)
            
    def test_generate(self):
        table = dummy_class(self.test_table, table_name='test_table', table_type='test_table_type')
        with pytest.raises(NotImplementedError):
            table.generate(15)
            
    def dictionary_out(self):
        table = dummy_class(self.test_table, table_name='test_table', table_type='test_table_type')
        with pytest.raises(NotImplementedError):
            table.dictionary_out()
