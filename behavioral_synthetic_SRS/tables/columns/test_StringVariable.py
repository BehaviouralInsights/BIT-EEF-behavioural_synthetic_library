import pandas as pd
import numpy as np
import pytest
import re

from .StringVariable import StringVariable

THRESHOLD = 10  # This needs to match the value given in the VariableType base abstract class

class TestStringVariable():
    
    short_series = 
    short_series_gaps = 
    short_series_blanks = 
    short_series_blanks_gaps = 
    
    patterned_string = 
    patterned_string_with_gaps = 
    patterned_string_with_blanks = 
    patterned_string_with_gaps_blanks 
    patterned_string_with_variable_lengths =
    
    
    unpatterned_string =
    unpatterned_string_gaps = 
    unpatterned_string_blanks = 
    unpatterned_string_gaps_blanks = 
    
    def test_threshold(self):
        column = StringVariable(self.short_series)
        assert column.THRESHOLD == THRESHOLD
    
    def test_short_series_error(self):
        column = StringVariable(self.short_series)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
    
    def test_short_series_with_gaps(self):
        column = StringVariable(self.short_series_gaps)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
    
    def test_short_series_with_blanks(self):
        column = StringVariable(self.short_series_blanks)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
    
    
    def test_short_series_with_gaps_blanks(self):
        column = StringVariable(self.short_series_blanks_gaps)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
    
    def test_patterned_string(self):
        column = StringVariable(self.patterned_string)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        chance = round(1.0/13.0, 7)
        example_dictionary = 
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.patterned_string.size)
        assert test_column.dtypes == self.patterned_string.dtypes
        assert any(test_column != self.patterned_string)
    
    def test_patterned_string_with_gaps(self):
        column = StringVariable(self.patterned_string_with_gaps)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        chance = round(1.0/13.0, 7)
        example_dictionary = 
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.patterned_string_with_gaps.size)
        assert test_column.dtypes == self.patterned_string_with_gaps.dtypes
        assert any(test_column != self.patterned_string_with_gaps)
    
    def test_patterned_string_with_blanks(self):
        column = StringVariable(self.patterned_string_with_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        chance = round(1.0/13.0, 7)
        example_dictionary = 
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.patterned_string_with_blanks.size)
        assert test_column.dtypes == self.patterned_string_with_blanks.dtypes
        assert any(test_column != self.patterned_string_with_blanks)
    
    def test_patterned_string_with_gaps_blanks(self):
        column = StringVariable(self.patterned_string_with_gaps_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        chance = round(1.0/13.0, 7)
        example_dictionary = 
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.patterned_string_with_gaps_blanks.size)
        assert test_column.dtypes == self.patterned_string_with_gaps_blanks.dtypes
        assert any(test_column != self.patterned_string_with_gaps_blanks)
    
    def test_patterned_string_with_variable_length(self):
        column = StringVariable(self.patterned_string_with_variable_lengths)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        chance = round(1.0/13.0, 7)
        pad_chance = round(11.0/13.0, 7)
        example_dictionary = {}
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.patterned_string_with_gaps_blanks.size)
        assert test_column.dtypes == self.patterned_string_with_gaps_blanks.dtypes
        assert any(test_column != self.patterned_string_with_gaps_blanks)
    
    
    def test_unpatterned_string(self):
        column = StringVariable(self.unpatterned_string)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.unpatterned_string.size)
        assert test_column.dtypes == self.unpatterned_string.dtypes
        assert any(test_column != self.unpatterned_string)
    
    def test_unpatterned_string_with_gaps(self):
        column = StringVariable(self.unpatterned_string_gaps)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =
        
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.unpatterned_string_gaps.size)
        assert test_column.dtypes == self.unpatterned_string_gaps.dtypes
        assert any(test_column != self.unpatterned_string_gaps)
    
    def test_unpatterned_string_with_blanks(self):
        column = StringVariable(self.unpatterned_string_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.unpatterned_string_blanks.size)
        assert test_column.dtypes == self.unpatterned_string_blanks.dtypes
        assert any(test_column != self.unpatterned_string_blanks)
    
    def test_unpatterned_string_with_gaps_blanks(self):
        column = StringVariable(self.unpatterned_string_gaps_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.unpatterned_string_gaps_blanks.size)
        assert test_column.dtypes == self.unpatterned_string_gaps_blanks.dtypes
        assert any(test_column != self.unpatterned_string_gaps_blanks)
        
        
    def test_set_unpatterned_string(self):
        input_dict = 
        temp_column = 
        temp_column.set_no_pattern(
           
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert input_dict == output_dict
        
    def test_set_patterned_string(self):
        chance = round(1.0/13.0, 7)
        input_dict = 
        temp_column = 
        temp_column.set_pattern(
            
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert input_dict == output_dict
