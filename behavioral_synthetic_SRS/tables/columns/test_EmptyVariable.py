import pandas as pd
import numpy as np
import pytest
import re

from .EmptyVariable import EmptyVariable

THRESHOLD = 10  # This needs to match the value given in the VariableType base abstract class


class TestEmptyVariable():
    
    empty_series = 
    
    def test_threshold(self):
        column = EmptyVariable(self.empty_series)
        assert column.THRESHOLD == THRESHOLD
    
    def test_empty_input(self):
       column = EmptyVariable(self.empty_series)
       column.analyse()
       test_dict = column.dictionary_out()
       
       example_dict = 
       
       assert test_dict == example_dict
       
       test_column = column.generate(self.empty_series.size)
       test_values = test_column.fillna('nan').to_list() #otherwise test fails.
       assert self.empty_series.dtypes == test_column.dtypes
       for value in test_values:
           assert value == 'nan'
       assert test_column.size == self.empty_series.size
       
    def test_set_empty_columns(self):
        input_dict = 
        
        column = EmptyVariable(pd.Series([0], name=input_dict["Name"]))
        output_dict = column.dictionary_out()
            
        assert input_dict == output_dict
