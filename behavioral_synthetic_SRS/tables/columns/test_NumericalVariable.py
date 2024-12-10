import pandas as pd
import numpy as np
import pytest
import re

from .NumericalVariable import NumericalVariable

THRESHOLD = 10  # This needs to match the value given in the VariableType base abstract class

class TestNumericalVariable:
    
    decimal_precision=3
    small_series = 
    mostly_nan_series = 
    
    integer_series = 
    integer_series_mean = 
    integer_series_max = 
    integer_series_min = 
    integer_series_sd = 
    integer_series_av_max = 
    integer_series_av_min = 
    
    integer_series_with_errors = 
    
    float_series =
    float_series_mean = 
    float_series_max = 
    float_series_min = 
    float_series_sd = 
    float_series_av_max = 
    float_series_av_min = 
    
    float_series_with_errors = 
    
    pos_neg_list = 
    all_positive = 
    all_negative = 
    
    def test_threshold(self):
        column = NumericalVariable(self.small_series, self.decimal_precision)
        assert column.THRESHOLD == THRESHOLD
    
    def test_too_small_series(self):
        column = NumericalVariable(self.small_series,self.decimal_precision, False)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
            
    def test_mostly_nan_series(self):
        column = NumericalVariable(self.mostly_nan_series,self.decimal_precision, False)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
        
    
    def test_integer_series(self):
        column =  NumericalVariable(self.integer_series, self.decimal_precision, False)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.integer_series.size)
        #assert str(test_column.dtypes) == str(self.integer_series.dtype)
        assert str(test_column.dtypes) == 'Int64'
        assert any(test_column != self.integer_series)
    
    def test_integer_with_avgs(self):
        column =  NumericalVariable(self.integer_series, self.decimal_precision)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict = 
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.integer_series.size)
        #assert str(test_column.dtypes) == str(self.integer_series.dtype)
        assert str(test_column.dtypes) == 'Int64'
        assert any(test_column != self.integer_series)
    
    def test_integer_with_errors(self):
        column =  NumericalVariable(self.integer_series_with_errors, self.decimal_precision, False)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.integer_series_with_errors.size)
        #assert str(test_column.dtypes) == str(self.integer_series.dtype)
        assert str(test_column.dtypes) == 'Int64'
    
        assert any(test_column.fillna(0) != self.integer_series_with_errors.fillna(0)) # replace as otherwise can't do comparison as pd.NA is ambiguous wrt Boolean tests
    
    def test_integer_with_errors_and_avgs(self):
        column =  NumericalVariable(self.integer_series_with_errors, self.decimal_precision)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict = 
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.integer_series_with_errors.size)
        #assert str(test_column.dtypes) == str(self.integer_series_with_errors.dtype)
        assert str(test_column.dtypes) == 'Int64'
        assert any(test_column.fillna(0) != self.integer_series_with_errors.fillna(0)) # replace as otherwise can't do comparison as pd.NA is ambiguous wrt Boolean tests
    
    def test_real_series(self):
        column =  NumericalVariable(self.float_series, self.decimal_precision, False)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.float_series.size)
        assert str(test_column.dtypes) == str(self.float_series.dtype)
        assert str(test_column.dtypes) == 'float64'
        assert any(test_column != self.float_series)
    
    def test_real_with_avgs(self):
        column =  NumericalVariable(self.float_series, self.decimal_precision)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict = 
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.float_series.size)
        assert str(test_column.dtypes) == str(self.float_series.dtype)
        assert str(test_column.dtypes) == 'float64'
        assert any(test_column != self.float_series)
    
    def test_real_with_errors(self):
        column =  NumericalVariable(self.float_series_with_errors, self.decimal_precision, False)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.float_series_with_errors.size)
        #assert str(test_column.dtypes) == str(self.float_series_with_errors.dtype)
        assert str(test_column.dtypes) == 'float64'
        assert any(test_column != self.float_series_with_errors)
    
    def test_real_with_errors_and_avgs(self):
        column =  NumericalVariable(self.float_series_with_errors, self.decimal_precision)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict = 
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.float_series_with_errors.size)
       # assert str(test_column.dtypes) == str(self.float_series_with_errors.dtype)
        assert str(test_column.dtypes) == 'float64'
        assert any(test_column != self.float_series_with_errors)
        
    def test_all_positive(self):
        column = NumericalVariable(self.all_positive, self.decimal_precision)
        column.analyse()
        test_column=column.generate(self.all_positive.size)
        
        assert all(test_column.dropna() > 0)
        
    def test_all_negative(self):
        column = NumericalVariable(self.all_negative, self.decimal_precision)
        column.analyse()
        test_column=column.generate(self.all_negative.size)
        print(self.all_negative)
        
        assert all(test_column.dropna() < 0)
    
    def test_set_int(self):
        input_dict =  
        
        temp_column = NumericalVariable(
     
            )
        temp_column.set(
       
        )
        output_dict = temp_column.dictionary_out()
        
        assert input_dict == output_dict
        
    def test_set_float(self):
        input_dict =  
        
        temp_column = NumericalVariable(
                       )
        temp_column.set(
            
        )
        output_dict = temp_column.dictionary_out()
        
        assert input_dict == output_dict
        
    def test_set_threshold_too_small(self):
        input_dict = 
        
        temp_column = NumericalVariable(
          
            )
        message = f"Warning: external setting of threshold for averaging is {input_dict['# of values in average_max_min']} but the internal value is {THRESHOLD}. The input is unsafe with respect to disclosure."
        
        with pytest.raises(ValueError, match=re.escape(message)):
            temp_column.set(
               
            )
            
    def test_disclosure_option(self):
        column =  NumericalVariable(self.float_series_with_errors, self.decimal_precision, disclosure = True)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  {
          }
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.float_series_with_errors.size)
       # assert str(test_column.dtypes) == str(self.float_series_with_errors.dtype)
        assert str(test_column.dtypes) == 'float64'
        assert any(test_column != self.float_series_with_errors)
