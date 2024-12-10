import pandas as pd
import numpy as np
import pytest
import re

from .NumericalVariable import NumericalVariable

THRESHOLD = 10  # This needs to match the value given in the VariableType base abstract class

class TestNumericalVariable:
    
    decimal_precision=3
    small_series = pd.Series([4.5, 45.1, 11, 10, 1], name='test')
    mostly_nan_series = pd.Series([np.NaN, np.NaN,4.5, np.NaN, 45.1, 11, np.NaN, 10, 1, np.NaN, np.NaN, np.NaN], name='test')
    
    integer_series = pd.Series([10,20,30,10,40,60,30,30,39,11,50,99,23,43], name='test')
    integer_series_mean = round(integer_series.mean(),7)
    integer_series_max = round(integer_series.max(),7)
    integer_series_min = round(integer_series.min(),7)
    integer_series_sd = round(integer_series.std(),7)
    integer_series_av_max = round(integer_series.nlargest(THRESHOLD, keep='first').mean(),7)
    integer_series_av_min = round(integer_series.nsmallest(THRESHOLD, keep='first').mean(),7)
    
    integer_series_with_errors = pd.Series([10,20,30,np.NaN,10,40,60,np.NaN,30,30,39,11,50,99,np.NaN,23,43], name='test')
    
    float_series = pd.Series([45.3, 43.1, 56.34, 10.1, 1.1,99.2,34.9,12.1,55.1, 30.1, 12, 45.7, 40], name='test')
    float_series_mean = round(float_series.mean(),7)
    float_series_max = round(float_series.max(),7)
    float_series_min = round(float_series.min(),7)
    float_series_sd = round(float_series.std(),7)
    float_series_av_max = round(float_series.nlargest(THRESHOLD, keep='first').mean(),7)
    float_series_av_min = round(float_series.nsmallest(THRESHOLD, keep='first').mean(),7)
    
    float_series_with_errors = pd.Series([45.3,np.NaN, 43.1, 56.34, np.NaN, 10.1, 1.1,99.2,34.9,12.1,55.1, 30.1, np.NaN, 12, 45.7, 40], name='test')
    
    pos_neg_list = np.array([3, 8, 9, 34, np.NaN, 23, 3, 1, 34, 23, 9, 23, 45, 100, 34.34, np.NaN])
    all_positive = pd.Series(pos_neg_list, name='test')
    all_negative = pd.Series(-pos_neg_list, name='test')
    
    def test_threshold(self):
        column = NumericalVariable(self.small_series, self.decimal_precision)
        assert column.get_THRESHOLD() == THRESHOLD
    
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
        
        expected_dict =  {"Name":"test","Type": "numeric", "decimal_precision": 0, "mean": self.integer_series_mean, "standard_deviation": self.integer_series_sd, "minimum": self.integer_series_min, "maximum": self.integer_series_max, "is_integer": True, "missing_value_freq": 0 , "averaged_max_and_min": False, "# of values in average_max_min": THRESHOLD}
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.integer_series.size)
        #assert str(test_column.dtypes) == str(self.integer_series.dtype)
        assert str(test_column.dtypes) == 'Int64'
        assert any(test_column != self.integer_series)
    
    def test_integer_with_avgs(self):
        column =  NumericalVariable(self.integer_series, self.decimal_precision)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  {"Name":"test","Type": "numeric", "decimal_precision": 0, "mean": self.integer_series_mean, "standard_deviation": self.integer_series_sd, "minimum": self.integer_series_av_min, "maximum": self.integer_series_av_max, "is_integer": True, "missing_value_freq": 0 , "averaged_max_and_min": True, "# of values in average_max_min": THRESHOLD}
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.integer_series.size)
        #assert str(test_column.dtypes) == str(self.integer_series.dtype)
        assert str(test_column.dtypes) == 'Int64'
        assert any(test_column != self.integer_series)
    
    def test_integer_with_errors(self):
        column =  NumericalVariable(self.integer_series_with_errors, self.decimal_precision, False)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  {"Name":"test","Type": "numeric", "decimal_precision": 0, "mean": self.integer_series_mean, "standard_deviation": self.integer_series_sd, "minimum": self.integer_series_min, "maximum": self.integer_series_max, "is_integer": True, "missing_value_freq": round(3.0/self.integer_series_with_errors.size, 7) , "averaged_max_and_min": False, "# of values in average_max_min": THRESHOLD}
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.integer_series_with_errors.size)
        #assert str(test_column.dtypes) == str(self.integer_series.dtype)
        assert str(test_column.dtypes) == 'Int64'
    
        assert any(test_column.fillna(0) != self.integer_series_with_errors.fillna(0)) # replace as otherwise can't do comparison as pd.NA is ambiguous wrt Boolean tests
    
    def test_integer_with_errors_and_avgs(self):
        column =  NumericalVariable(self.integer_series_with_errors, self.decimal_precision)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  {"Name":"test","Type": "numeric", "decimal_precision": 0, "mean": self.integer_series_mean, "standard_deviation": self.integer_series_sd, "minimum": self.integer_series_av_min, "maximum": self.integer_series_av_max, "is_integer": True, "missing_value_freq": round(3.0/self.integer_series_with_errors.size,7) , "averaged_max_and_min": True, "# of values in average_max_min": THRESHOLD}
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.integer_series_with_errors.size)
        #assert str(test_column.dtypes) == str(self.integer_series_with_errors.dtype)
        assert str(test_column.dtypes) == 'Int64'
        assert any(test_column.fillna(0) != self.integer_series_with_errors.fillna(0)) # replace as otherwise can't do comparison as pd.NA is ambiguous wrt Boolean tests
    
    def test_real_series(self):
        column =  NumericalVariable(self.float_series, self.decimal_precision, False)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  {"Name":"test","Type": "numeric", "decimal_precision": self.decimal_precision, "mean": self.float_series_mean, "standard_deviation": self.float_series_sd, "minimum": self.float_series_min, "maximum": self.float_series_max, "is_integer": False, "missing_value_freq": 0 , "averaged_max_and_min": False, "# of values in average_max_min": THRESHOLD}
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.float_series.size)
        assert str(test_column.dtypes) == str(self.float_series.dtype)
        assert str(test_column.dtypes) == 'float64'
        assert any(test_column != self.float_series)
    
    def test_real_with_avgs(self):
        column =  NumericalVariable(self.float_series, self.decimal_precision)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  {"Name":"test","Type": "numeric", "decimal_precision": self.decimal_precision, "mean": self.float_series_mean, "standard_deviation": self.float_series_sd, "minimum": self.float_series_av_min, "maximum": self.float_series_av_max, "is_integer": False, "missing_value_freq": 0 , "averaged_max_and_min": True, "# of values in average_max_min": THRESHOLD}
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.float_series.size)
        assert str(test_column.dtypes) == str(self.float_series.dtype)
        assert str(test_column.dtypes) == 'float64'
        assert any(test_column != self.float_series)
    
    def test_real_with_errors(self):
        column =  NumericalVariable(self.float_series_with_errors, self.decimal_precision, False)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  {"Name":"test","Type": "numeric", "decimal_precision": self.decimal_precision, "mean": self.float_series_mean, "standard_deviation": self.float_series_sd, "minimum": self.float_series_min, "maximum": self.float_series_max, "is_integer": False, "missing_value_freq": 3.0/self.float_series_with_errors.size, "averaged_max_and_min": False, "# of values in average_max_min": THRESHOLD}
        
        assert test_dict == expected_dict
        
        test_column = column.generate(self.float_series_with_errors.size)
        #assert str(test_column.dtypes) == str(self.float_series_with_errors.dtype)
        assert str(test_column.dtypes) == 'float64'
        assert any(test_column != self.float_series_with_errors)
    
    def test_real_with_errors_and_avgs(self):
        column =  NumericalVariable(self.float_series_with_errors, self.decimal_precision)
        column.analyse()
        test_dict = column.dictionary_out()
        
        expected_dict =  {"Name":"test","Type": "numeric", "decimal_precision": self.decimal_precision, "mean": self.float_series_mean, "standard_deviation": self.float_series_sd, "minimum": self.float_series_av_min, "maximum": self.float_series_av_max, "is_integer": False, "missing_value_freq": 3.0/self.float_series_with_errors.size, "averaged_max_and_min": True, "# of values in average_max_min": THRESHOLD}
        
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
        input_dict =  {"Name":"test","Type": "numeric", "decimal_precision": 0, "mean": self.integer_series_mean, "standard_deviation": self.integer_series_sd, "minimum": self.integer_series_av_min, "maximum": self.integer_series_av_max, "is_integer": True, "missing_value_freq": round(3.0/self.integer_series_with_errors.size,7) , "averaged_max_and_min": True, "# of values in average_max_min": THRESHOLD}
        
        temp_column = NumericalVariable(
            pd.Series([0], name=input_dict['Name']),
            decimal_precision = input_dict['decimal_precision'],
            average_min_max = input_dict['averaged_max_and_min'],
            )
        temp_column.set(
            mean = input_dict['mean'],
            standard_deviation = input_dict['standard_deviation'],
            maximum = input_dict['maximum'],
            minimum = input_dict['minimum'],
            is_integer = input_dict['is_integer'],
            no_vals_in_threshold = input_dict['# of values in average_max_min'],
            missing_freq = input_dict["missing_value_freq"],
            number_of_rows = self.integer_series_with_errors.size
        )
        output_dict = temp_column.dictionary_out()
        
        assert input_dict == output_dict
        
    def test_set_float(self):
        input_dict =  {"Name":"test","Type": "numeric", "decimal_precision": self.decimal_precision, "mean": self.float_series_mean, "standard_deviation": self.float_series_sd, "minimum": self.float_series_av_min, "maximum": self.float_series_av_max, "is_integer": False, "missing_value_freq": 3.0/self.float_series_with_errors.size, "averaged_max_and_min": True, "# of values in average_max_min": THRESHOLD}
        
        temp_column = NumericalVariable(
            pd.Series([0], name=input_dict['Name']),
            decimal_precision = input_dict['decimal_precision'],
            average_min_max = input_dict['averaged_max_and_min'],
            )
        temp_column.set(
            mean = input_dict['mean'],
            standard_deviation = input_dict['standard_deviation'],
            maximum = input_dict['maximum'],
            minimum = input_dict['minimum'],
            is_integer = input_dict['is_integer'],
            no_vals_in_threshold = input_dict['# of values in average_max_min'],
            missing_freq = input_dict["missing_value_freq"],
            number_of_rows = self.float_series_with_errors.size
        )
        output_dict = temp_column.dictionary_out()
        
        assert input_dict == output_dict
        
    def test_set_threshold_too_small(self):
        input_dict =  {"Name":"test","Type": "numeric", "decimal_precision": self.decimal_precision, "mean": self.float_series_mean, "standard_deviation": self.float_series_sd, "minimum": self.float_series_av_min, "maximum": self.float_series_av_max, "is_integer": False, "missing_value_freq": 3.0/self.float_series_with_errors.size, "averaged_max_and_min": True, "# of values in average_max_min": 4}
        
        temp_column = NumericalVariable(
            pd.Series([0], name=input_dict['Name']),
            decimal_precision = input_dict['decimal_precision'],
            average_min_max = input_dict['averaged_max_and_min'],
            )
        message = f"Warning: external setting of threshold for averaging is {input_dict['# of values in average_max_min']} but the internal value is {THRESHOLD}. The input is unsafe with respect to disclosure."
        
        with pytest.raises(ValueError, match=re.escape(message)):
            temp_column.set(
                mean = input_dict['mean'],
                standard_deviation = input_dict['standard_deviation'],
                maximum = input_dict['maximum'],
                minimum = input_dict['minimum'],
                is_integer = input_dict['is_integer'],
                no_vals_in_threshold = input_dict['# of values in average_max_min'],
                missing_freq = input_dict["missing_value_freq"],
                number_of_rows = self.float_series_with_errors.size
            )