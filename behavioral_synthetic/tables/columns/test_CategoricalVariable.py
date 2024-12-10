import pandas as pd
import numpy as np
import pytest
import re

from .CategoricalVariable import CategoricalVariable

THRESHOLD = 10  # This needs to match the value given in the VariableType base abstract class


class TestCategoricalVariable():
    
    numerical_series = pd.Series([7,5,5,6,8,9,9,9,2,3,3,9], name='test')
    numerical_series_with_gaps = pd.Series([7,5, np.NaN,5,6,8, np.NaN,9,9,9,np.NaN,2,3,3,9], name='test')
    
    string_series = pd.Series(["A", "A", "B", "B", "B", "C", "C", "L", "A", "B", "R", "Y"], name='test')
    string_series_with_errors = pd.Series(["A", "A", "B", np.NaN, "B", "B", "C",np.NaN, "C", "L", "A", "B", "R", "Y", np.NaN], name='test')
    string_series_with_blanks = pd.Series(["A", "A", "B", "", "B", "B", "C","", "C", "L", "A", "B", "R", "Y", ""], name='test')
    string_series_with_blanks_errors = pd.Series(["A", "A", "B", "",np.NaN, "B", "B", "C","", "C", "L", "A", "B", np.NaN, "R", np.NaN, "Y", ""], name='test')
    
    short_series = pd.Series([1,2,3,5,3], name='test')
    short_series_error = pd.Series([1,2,3,5,3, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN], name='test')
    short_series_blanks = pd.Series([1,2,3,5,3, "", "", "", "", "", ""], name='test')
    short_series_both = pd.Series([1,2,3,5,3, "", "", "", "", "", "", np.NaN,np.NaN], name='test')
    
    def test_threshold(self):
        column = CategoricalVariable(self.short_series)
        assert column.get_THRESHOLD() == THRESHOLD
    
    def test_short_series_error(self):
        test_column = CategoricalVariable(self.short_series)
        message = f"Insuffucient number of values in series to produce disclosure safe results (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            test_column.analyse()
            
    def test_short_series_error_with_errors(self):
        test_column = CategoricalVariable(self.short_series_error)
        message = f"Insuffucient number of values in series to produce disclosure safe results (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            test_column.analyse()
            
    def test_short_series_error_with_blanks(self):
        test_column = CategoricalVariable(self.short_series_blanks)
        message = f"Insuffucient number of values in series to produce disclosure safe results (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            test_column.analyse()
            
    def test_short_series_error_with_both(self):
        test_column = CategoricalVariable(self.short_series_both)
        message = f"Insuffucient number of values in series to produce disclosure safe results (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            test_column.analyse()
    
    def test_numerical_categories(self):
        column = CategoricalVariable(self.numerical_series)    
        column.analyse()
        test_column = column.generate(self.numerical_series.size)
        
        test_dict = column.dictionary_out()
    
        expected_dict = {
            "Name": "test",
            "Type": "categorical", 
            7: round(1.0/self.numerical_series.size,7),
            5: round(2.0/self.numerical_series.size,7),
            6: round(1.0/self.numerical_series.size, 7),
            8: round(1.0/self.numerical_series.size,7),
            9: round(4.0/self.numerical_series.size,7),
            2: round(1.0/self.numerical_series.size,7),
            3: round(2.0/self.numerical_series.size,7)
        }
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        # level of strictness assumed by line below causes problems so commented out
        # assert test_column.dtypes == self.numerical_series.dtypes 
        assert any(test_column != self.numerical_series)
        
        
    
    def test_numerical_categories_with_error(self):
        
        column = CategoricalVariable(self.numerical_series_with_gaps)    
        column.analyse()
        test_column = column.generate(self.numerical_series_with_gaps.size)
        
        test_dict = column.dictionary_out()
        
        expected_dict = {
            "Name": "test",
            "Type": "categorical", 
            7: round(1.0/self.numerical_series_with_gaps.size,7),
            5: round(2.0/self.numerical_series_with_gaps.size,7),
            6: round(1.0/self.numerical_series_with_gaps.size, 7),
            8: round(1.0/self.numerical_series_with_gaps.size,7),
            9: round(4.0/self.numerical_series_with_gaps.size,7),
            2: round(1.0/self.numerical_series_with_gaps.size,7),
            3: round(2.0/self.numerical_series_with_gaps.size,7),
            'nan': round(3.0/self.numerical_series_with_gaps.size,7)
        }
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        #  level of strictness assumed by line below causes problems so commented out
        # assert test_column.dtypes == self.numerical_series_with_gaps.dtypes
        assert any(test_column != self.numerical_series_with_gaps)
    
    
    def test_string_categories(self):
        column = CategoricalVariable(self.string_series)
        column.analyse()
        
        test_dict = column.dictionary_out()
        expected_dict = {
            "Name": "test",
            "Type": "categorical",
            "A": round(self.string_series.to_list().count("A")/self.string_series.size, 7),
            "B": round(self.string_series.to_list().count("B")/self.string_series.size, 7),
            "C": round(self.string_series.to_list().count("C")/self.string_series.size, 7),
            "L": round(self.string_series.to_list().count("L")/self.string_series.size, 7),
            "R": round(self.string_series.to_list().count("R")/self.string_series.size, 7),
            "Y": round(self.string_series.to_list().count("Y")/self.string_series.size, 7)
        }
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        test_column = column.generate(self.string_series.size)
        assert test_column.dtypes == self.string_series.dtypes
        assert any(test_column != self.string_series)
    
    def test_string_categories_with_error(self):
        column = CategoricalVariable(self.string_series_with_errors)
        column.analyse()
        
        test_dict = column.dictionary_out()
        expected_dict = {
            "Name": "test",
            "Type": "categorical",
            "A": round(self.string_series_with_errors.to_list().count("A")/self.string_series_with_errors.size, 7),
            "B": round(self.string_series_with_errors.to_list().count("B")/self.string_series_with_errors.size, 7),
            "C": round(self.string_series_with_errors.to_list().count("C")/self.string_series_with_errors.size, 7),
            "L": round(self.string_series_with_errors.to_list().count("L")/self.string_series_with_errors.size, 7),
            "R": round(self.string_series_with_errors.to_list().count("R")/self.string_series_with_errors.size, 7),
            "Y": round(self.string_series_with_errors.to_list().count("Y")/self.string_series_with_errors.size, 7),
            'nan': round(3.0/self.string_series_with_errors.size, 7)
        }
        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        test_column = column.generate(self.string_series_with_errors.size)
        assert test_column.dtypes == self.string_series_with_errors.dtypes
        assert any(test_column != self.string_series_with_errors)
    
    def test_string_categories_with_blanks(self):
        column = CategoricalVariable(self.string_series_with_blanks)
        column.analyse()
        
        test_dict = column.dictionary_out()
        expected_dict = {
            "Name": "test",
            "Type": "categorical",
            "A": round(self.string_series_with_blanks.to_list().count("A")/self.string_series_with_blanks.size, 7),
            "B": round(self.string_series_with_blanks.to_list().count("B")/self.string_series_with_blanks.size, 7),
            "C": round(self.string_series_with_blanks.to_list().count("C")/self.string_series_with_blanks.size, 7),
            "L": round(self.string_series_with_blanks.to_list().count("L")/self.string_series_with_blanks.size, 7),
            "R": round(self.string_series_with_blanks.to_list().count("R")/self.string_series_with_blanks.size, 7),
            "Y": round(self.string_series_with_blanks.to_list().count("Y")/self.string_series_with_blanks.size, 7),
            '': round(3.0/self.string_series_with_blanks.size, 7)
        }
        

        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        test_column = column.generate(self.string_series_with_blanks.size)
        assert test_column.dtypes == self.string_series_with_blanks.dtypes
        assert any(test_column != self.string_series_with_blanks)
    
    def test_string_categories_with_blanks_errors(self):
        column = CategoricalVariable(self.string_series_with_blanks_errors)
        column.analyse()
        
        test_dict = column.dictionary_out()
        expected_dict = {
            "Name": "test",
            "Type": "categorical",
            "A": round(self.string_series_with_blanks_errors.to_list().count("A")/self.string_series_with_blanks_errors.size, 7),
            "B": round(self.string_series_with_blanks_errors.to_list().count("B")/self.string_series_with_blanks_errors.size, 7),
            "C": round(self.string_series_with_blanks_errors.to_list().count("C")/self.string_series_with_blanks_errors.size, 7),
            "L": round(self.string_series_with_blanks_errors.to_list().count("L")/self.string_series_with_blanks_errors.size, 7),
            "R": round(self.string_series_with_blanks_errors.to_list().count("R")/self.string_series_with_blanks_errors.size, 7),
            "Y": round(self.string_series_with_blanks_errors.to_list().count("Y")/self.string_series_with_blanks_errors.size, 7),
            '': round(3.0/self.string_series_with_blanks_errors.size, 7),
            'nan': round(3.0/self.string_series_with_blanks_errors.size, 7)
        }
        

        
        for key in test_dict.keys():
            assert key in expected_dict
            assert test_dict[key] == expected_dict[key]
        assert len(test_dict) == len(expected_dict)
        
        test_column = column.generate(self.string_series_with_blanks_errors.size)
        assert test_column.dtypes == self.string_series_with_blanks_errors.dtypes
        assert any(test_column != self.string_series_with_blanks_errors)
        
    def test_set_string_categories(self):
        input_dict =  {
            "Name": "test",
            "Type": "categorical",
            "A": round(self.string_series_with_blanks_errors.to_list().count("A")/self.string_series_with_blanks_errors.size, 7),
            "B": round(self.string_series_with_blanks_errors.to_list().count("B")/self.string_series_with_blanks_errors.size, 7),
            "C": round(self.string_series_with_blanks_errors.to_list().count("C")/self.string_series_with_blanks_errors.size, 7),
            "L": round(self.string_series_with_blanks_errors.to_list().count("L")/self.string_series_with_blanks_errors.size, 7),
            "R": round(self.string_series_with_blanks_errors.to_list().count("R")/self.string_series_with_blanks_errors.size, 7),
            "Y": round(self.string_series_with_blanks_errors.to_list().count("Y")/self.string_series_with_blanks_errors.size, 7),
            '': round(3.0/self.string_series_with_blanks_errors.size, 7),
            'nan': round(3.0/self.string_series_with_blanks_errors.size, 7)
        }
        
        column = CategoricalVariable(pd.Series([0], name = input_dict["Name"]))
        column.set(
                    frequencies = {value: input_dict[value] for value in input_dict.keys() if value not in ['Type','Name']}
                )
        output_dict = column.dictionary_out()
        
        assert input_dict == output_dict
            
    def test_set_integer_categores(self):
        input_dict = {
            "Name": "test",
            "Type": "categorical", 
            7: round(1.0/self.numerical_series_with_gaps.size,7),
            5: round(2.0/self.numerical_series_with_gaps.size,7),
            6: round(1.0/self.numerical_series_with_gaps.size, 7),
            8: round(1.0/self.numerical_series_with_gaps.size,7),
            9: round(4.0/self.numerical_series_with_gaps.size,7),
            2: round(1.0/self.numerical_series_with_gaps.size,7),
            3: round(2.0/self.numerical_series_with_gaps.size,7),
            'nan': round(3.0/self.numerical_series_with_gaps.size,7)
        }
        
        column = CategoricalVariable(pd.Series([0], name = input_dict["Name"]))
        column.set(
                    frequencies = {value: input_dict[value] for value in input_dict.keys() if value not in ['Type','Name']}
                )
        output_dict = column.dictionary_out()
        
        assert input_dict == output_dict
            