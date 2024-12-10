import pandas as pd
import numpy as np
import pytest
import re

from .CategoricalVariable import CategoricalVariable

THRESHOLD = 10  # This needs to match the value given in the VariableType base abstract class


class TestCategoricalVariable():
    
    numerical_series = 
    numerical_series_with_gaps = 
    
    string_series = 
    string_series_with_errors = 
    string_series_with_blanks = 
    string_series_with_blanks_errors =

    short_series = 
    short_series_error = 
    short_series_blanks = 
    short_series_both = 
    
    
    string_series_for_disclosure =
    
    def test_threshold(self):
        column = CategoricalVariable(self.short_series, disclosure=False)
        assert column.THRESHOLD == THRESHOLD
    
    def test_short_series_error(self):
        test_column = CategoricalVariable(self.short_series, disclosure=False)
        message = f"Insuffucient number of values in series to produce disclosure safe results (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            test_column.analyse()
            
    def test_short_series_error_with_errors(self):
        test_column = CategoricalVariable(self.short_series_error, disclosure=False)
        message = f"Insuffucient number of values in series to produce disclosure safe results (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            test_column.analyse()
            
    def test_short_series_error_with_blanks(self):
        test_column = CategoricalVariable(self.short_series_blanks,disclosure=False)
        message = f"Insuffucient number of values in series to produce disclosure safe results (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            test_column.analyse()
            
    def test_short_series_error_with_both(self):
        test_column = CategoricalVariable(self.short_series_both, disclosure=False)
        message = f"Insuffucient number of values in series to produce disclosure safe results (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            test_column.analyse()
    
    def test_numerical_categories(self):
        column = CategoricalVariable(self.numerical_series, disclosure=False)    
        column.analyse()
        test_column = column.generate(self.numerical_series.size)
        
        test_dict = column.dictionary_out()
    
        expected_dict = 
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        assert test_column.dtypes == self.numerical_series.dtypes
        assert any(test_column != self.numerical_series)
        
        
    
    def test_numerical_categories_with_error(self):
        
        column = CategoricalVariable(self.numerical_series_with_gaps, disclosure=False)    
        column.analyse()
        test_column = column.generate(self.numerical_series_with_gaps.size)
        
        test_dict = column.dictionary_out()
        
        expected_dict = 
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        assert test_column.dtypes == self.numerical_series_with_gaps.dtypes
        assert any(test_column != self.numerical_series_with_gaps)
    
    
    def test_string_categories(self):
        column = CategoricalVariable(self.string_series, disclosure=False)
        column.analyse()
        
        test_dict = column.dictionary_out()
        expected_dict =
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        test_column = column.generate(self.string_series.size)
        assert test_column.dtypes == self.string_series.dtypes
        assert any(test_column != self.string_series)
    
    def test_string_categories_with_error(self):
        column = CategoricalVariable(self.string_series_with_errors, disclosure=False)
        column.analyse()
        
        test_dict = column.dictionary_out()
        expected_dict = 
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        test_column = column.generate(self.string_series_with_errors.size)
        assert test_column.dtypes == self.string_series_with_errors.dtypes
        assert any(test_column != self.string_series_with_errors)
    
    def test_string_categories_with_blanks(self):
        column = CategoricalVariable(self.string_series_with_blanks, disclosure=False)
        column.analyse()
        
        test_dict = column.dictionary_out()
        expected_dict = 
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        test_column = column.generate(self.string_series_with_blanks.size)
        assert test_column.dtypes == self.string_series_with_blanks.dtypes
        assert any(test_column != self.string_series_with_blanks)
    
    def test_string_categories_with_blanks_errors(self):
        column = CategoricalVariable(self.string_series_with_blanks_errors, disclosure=False)
        column.analyse()
        
        test_dict = column.dictionary_out()
        expected_dict = 
           
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        test_column = column.generate(self.string_series_with_blanks_errors.size)
        assert test_column.dtypes == self.string_series_with_blanks_errors.dtypes
        assert any(test_column != self.string_series_with_blanks_errors)
        
    def test_set_string_categories(self):
        input_dict =  
        
        column = CategoricalVariable(pd.Series([0], name = input_dict["Name"]), disclosure=False)
        column.set(
                    frequencies = {value: input_dict[value] for value in input_dict.keys() if value not in ['Type','Name']}
                )
        output_dict = column.dictionary_out()
        
        assert input_dict == output_dict
            
    def test_set_integer_categores(self):
        input_dict = 
        
        column = CategoricalVariable(pd.Series([0], name = input_dict["Name"]), disclosure=False)
        column.set(
                    frequencies = {value: input_dict[value] for value in input_dict.keys() if value not in ['Type','Name']}
                )
        output_dict = column.dictionary_out()
        
        assert input_dict == output_dict
     
    def test_string_disclosure(self):
        column = CategoricalVariable(self.string_series_for_disclosure) #, disclosure=True)
        column.analyse()
        
        test_dict = column.dictionary_out()
        
       # assert test_dict['A'] + test_dict['nan'] == 1.0
        
        #base_PA = (15.0+3.0)/20.0
        note = f"All values with a frequency of less than {THRESHOLD/self.string_series_for_disclosure.size} have had that frequency repressed (here, set to zero), and the frequencies have been recalculated to prevent secondary disclosure."#" 'nan' values are not considered disclosive."
        expected_dict = {
          
        }
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
         
         
