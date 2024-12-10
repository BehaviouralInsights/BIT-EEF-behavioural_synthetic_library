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
        column = super().identify_variable_type(column_name, decimal_precision=2)
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
    
    test_table = pd.DataFrame.from_dict({
        "A": [np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN],
        "B": ["Y", "N", "N", "Y", "Y", "Y", "N", "N","N", "Y", "N", "N", "N", "Y", "N"],
        "C": [1, 0, 0, 1, 1, 1, 0, 0,0, 1, 0, 0, 0, 1, 0],
        "D": [12, 45, 12, 78, 20, 33, 1, 1000, 20, 56, 89, 34,56.03, 45, 3445],
        "E": ["Gwyr", "a aeth", "Gatraeth oedd ffraith", "eu llu", "glasfedd", "eu", "hancwyn", "a'u gwenwyn", "fu", "trichant", "trwy peiriant", "yn catau", "ac", "gwedu elwch","tawelwch fu"],
        "F": ["2081-12-15 00:01:34", "2081-12-16 01:32:22", "2081-12-17 04:43:34", "2081-12-18 08:50:02", "2081-12-19 09:40:45", "2081-12-20 10:45:45","2081-12-21 11:12:13", "2081-12-22 14:34:32", "2081-12-23 15:11:59", "2081-12-24 16:34:56", "2081-12-25 18:32:23", "2081-12-26 19:23:33", "2081-12-27 19:43:33", "2081-12-28 21:56:43", "2081-12-29 23:10:22"]
    })
    
    def test_identify_variable_type(self):
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