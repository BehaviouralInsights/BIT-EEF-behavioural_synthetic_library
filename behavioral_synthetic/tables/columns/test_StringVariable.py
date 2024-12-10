import pandas as pd
import numpy as np
import pytest
import re

from .StringVariable import StringVariable

THRESHOLD = 10  # This needs to match the value given in the VariableType base abstract class

class TestStringVariable():
    
    short_series = pd.Series(['ab zx', 'bc xy', 'cd yw'], name='test')
    short_series_gaps = pd.Series([np.NaN, np.NaN,'ab zx', np.NaN, np.NaN, 'bc xy', np.NaN, 'cd yw', np.NaN, np.NaN, np.NaN], name='test')
    short_series_blanks = pd.Series(["", "",'ab zx', "", "", 'bc xy', "", 'cd yw', "", "", ""], name='test')
    short_series_blanks_gaps = pd.Series([np.NaN, "",'ab zx', "", "", 'bc xy', "", 'cd yw', "", np.NaN, ""], name='test')
    
    patterned_string = pd.Series(['ab', 'cd', 'ef', 'gh', 'ij', 'kl', 'mn', 'op', 'qr', 'st', 'uv', 'wx', 'yz'], name='test')
    patterned_string_with_gaps = pd.Series(['ab', 'cd', 'ef', 'gh', np.NaN, 'ij', 'kl', 'mn', np.NaN,'op', np.NaN, 'qr', 'st', 'uv', 'wx', 'yz'], name='test')
    patterned_string_with_blanks = pd.Series(['ab', 'cd', 'ef', 'gh', "", 'ij', 'kl', 'mn', "",'op', "", 'qr', 'st', 'uv', 'wx', 'yz'], name='test')
    patterned_string_with_gaps_blanks = pd.Series(['ab', 'cd', 'ef', 'gh', np.NaN , 'ij', 'kl', 'mn', "",'op', "", 'qr', 'st', 'uv', 'wx', 'yz'], name='test')
    
    unpatterned_string = pd.Series(["Gwyr a aeth", "Gatraeth oedd", "ffraeth", "eu llu", "glasfedd eu", "hancwyn a'i wenwyn fu", "trichant trwy", "beiriant yn catáu", "ac gwedy elwch", "tawelwch", "fu"], name='test')
    unpatterned_string_gaps = pd.Series(["Gwyr a aeth", "Gatraeth oedd", np.NaN, "ffraeth", "eu llu", "glasfedd eu", "hancwyn a'i wenwyn fu", "trichant trwy", np.NaN, "beiriant yn catáu", "ac gwedy elwch", np.NaN, "tawelwch", "fu"], name='test')
    unpatterned_string_blanks = pd.Series(["Gwyr a aeth", "Gatraeth oedd", "", "ffraeth", "eu llu", "glasfedd eu", "hancwyn a'i wenwyn fu", "trichant trwy", "", "beiriant yn catáu", "ac gwedy elwch", "", "tawelwch", "fu"], name='test')
    unpatterned_string_gaps_blanks = pd.Series(["Gwyr a aeth", "Gatraeth oedd", np.NaN, "ffraeth", "eu llu", "glasfedd eu", "hancwyn a'i wenwyn fu", "trichant trwy", "", "beiriant yn catáu", "ac gwedy elwch", "", "tawelwch", "fu"], name='test')
    
    def test_threshold(self):
        column = StringVariable(self.short_series)
        assert column.get_THRESHOLD() == THRESHOLD
    
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
        example_dictionary = {'Name': 'test', 'Type': 'text', 'Pattern': True, 'Max_length': 2, 'character_number_0': {'a': chance, 'b': 0.0, 'c': chance, 'd': 0.0, 'e': chance, 'f': 0.0, 'g': chance, 'h': 0.0, 'i': chance, 'j': 0.0, 'k': chance, 'l': 0.0, 'm': chance, 'n': 0.0, 'o': chance, 'p': 0.0, 'q': chance, 'r': 0.0, 's': chance, 't': 0.0, 'u': chance, 'v': 0.0, 'w': chance, 'x': 0.0, 'y': chance, 'z': 0.0}, 'character_number_1': {'a': 0.0, 'b': chance, 'c': 0.0, 'd': chance, 'e': 0.0, 'f': chance, 'g': 0.0, 'h': chance, 'i': 0.0, 'j': chance, 'k': 0.0, 'l': chance, 'm': 0.0, 'n': chance, 'o': 0.0, 'p': chance, 'q': 0.0, 'r': chance, 's': 0.0, 't': chance, 'u': 0.0, 'v': chance, 'w': 0.0, 'x': chance, 'y': 0.0, 'z': chance}, 'missing_value_freq': 0.0}
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.patterned_string.size)
        assert test_column.dtypes == self.patterned_string.dtypes
        assert any(test_column != self.patterned_string)
    
    def test_patterned_string_with_gaps(self):
        column = StringVariable(self.patterned_string_with_gaps)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        chance = round(1.0/13.0, 7)
        example_dictionary = {'Name': 'test', 'Type': 'text', 'Pattern': True, 'Max_length': 2, 'character_number_0': {'a': chance, 'b': 0.0, 'c': chance, 'd': 0.0, 'e': chance, 'f': 0.0, 'g': chance, 'h': 0.0, 'i': chance, 'j': 0.0, 'k': chance, 'l': 0.0, 'm': chance, 'n': 0.0, 'o': chance, 'p': 0.0, 'q': chance, 'r': 0.0, 's': chance, 't': 0.0, 'u': chance, 'v': 0.0, 'w': chance, 'x': 0.0, 'y': chance, 'z': 0.0}, 'character_number_1': {'a': 0.0, 'b': chance, 'c': 0.0, 'd': chance, 'e': 0.0, 'f': chance, 'g': 0.0, 'h': chance, 'i': 0.0, 'j': chance, 'k': 0.0, 'l': chance, 'm': 0.0, 'n': chance, 'o': 0.0, 'p': chance, 'q': 0.0, 'r': chance, 's': 0.0, 't': chance, 'u': 0.0, 'v': chance, 'w': 0.0, 'x': chance, 'y': 0.0, 'z': chance}, 'missing_value_freq': round(3.0/self.patterned_string_with_gaps.size,7)}
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.patterned_string_with_gaps.size)
        assert test_column.dtypes == self.patterned_string_with_gaps.dtypes
        assert any(test_column != self.patterned_string_with_gaps)
    
    def test_patterned_string_with_blanks(self):
        column = StringVariable(self.patterned_string_with_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        chance = round(1.0/13.0, 7)
        example_dictionary = {'Name': 'test', 'Type': 'text', 'Pattern': True, 'Max_length': 2, 'character_number_0': {'a': chance, 'b': 0.0, 'c': chance, 'd': 0.0, 'e': chance, 'f': 0.0, 'g': chance, 'h': 0.0, 'i': chance, 'j': 0.0, 'k': chance, 'l': 0.0, 'm': chance, 'n': 0.0, 'o': chance, 'p': 0.0, 'q': chance, 'r': 0.0, 's': chance, 't': 0.0, 'u': chance, 'v': 0.0, 'w': chance, 'x': 0.0, 'y': chance, 'z': 0.0}, 'character_number_1': {'a': 0.0, 'b': chance, 'c': 0.0, 'd': chance, 'e': 0.0, 'f': chance, 'g': 0.0, 'h': chance, 'i': 0.0, 'j': chance, 'k': 0.0, 'l': chance, 'm': 0.0, 'n': chance, 'o': 0.0, 'p': chance, 'q': 0.0, 'r': chance, 's': 0.0, 't': chance, 'u': 0.0, 'v': chance, 'w': 0.0, 'x': chance, 'y': 0.0, 'z': chance}, 'missing_value_freq': round(3.0/self.patterned_string_with_blanks.size,7)}
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.patterned_string_with_blanks.size)
        assert test_column.dtypes == self.patterned_string_with_blanks.dtypes
        assert any(test_column != self.patterned_string_with_blanks)
    
    def test_patterned_string_with_gaps_blanks(self):
        column = StringVariable(self.patterned_string_with_gaps_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        chance = round(1.0/13.0, 7)
        example_dictionary = {'Name': 'test', 'Type': 'text', 'Pattern': True, 'Max_length': 2, 'character_number_0': {'a': chance, 'b': 0.0, 'c': chance, 'd': 0.0, 'e': chance, 'f': 0.0, 'g': chance, 'h': 0.0, 'i': chance, 'j': 0.0, 'k': chance, 'l': 0.0, 'm': chance, 'n': 0.0, 'o': chance, 'p': 0.0, 'q': chance, 'r': 0.0, 's': chance, 't': 0.0, 'u': chance, 'v': 0.0, 'w': chance, 'x': 0.0, 'y': chance, 'z': 0.0}, 'character_number_1': {'a': 0.0, 'b': chance, 'c': 0.0, 'd': chance, 'e': 0.0, 'f': chance, 'g': 0.0, 'h': chance, 'i': 0.0, 'j': chance, 'k': 0.0, 'l': chance, 'm': 0.0, 'n': chance, 'o': 0.0, 'p': chance, 'q': 0.0, 'r': chance, 's': 0.0, 't': chance, 'u': 0.0, 'v': chance, 'w': 0.0, 'x': chance, 'y': 0.0, 'z': chance}, 'missing_value_freq': round(3.0/self.patterned_string_with_blanks.size,7)}
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.patterned_string_with_gaps_blanks.size)
        assert test_column.dtypes == self.patterned_string_with_gaps_blanks.dtypes
        assert any(test_column != self.patterned_string_with_gaps_blanks)
    
    def test_unpatterned_string(self):
        column = StringVariable(self.unpatterned_string)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = {"Name": "test", "Type": "text", "Pattern": False, "Max_length": 21, "Min_length": 2, "missing_value_freq": 0.0}
        
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.unpatterned_string.size)
        assert test_column.dtypes == self.unpatterned_string.dtypes
        assert any(test_column != self.unpatterned_string)
    
    def test_unpatterned_string_with_gaps(self):
        column = StringVariable(self.unpatterned_string_gaps)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = {"Name": "test", "Type": "text", "Pattern": False, "Max_length": 21, "Min_length": 2, "missing_value_freq": round(3.0/self.unpatterned_string_gaps.size, 7)}
        
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.unpatterned_string_gaps.size)
        assert test_column.dtypes == self.unpatterned_string_gaps.dtypes
        assert any(test_column != self.unpatterned_string_gaps)
    
    def test_unpatterned_string_with_blanks(self):
        column = StringVariable(self.unpatterned_string_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = {"Name": "test", "Type": "text", "Pattern": False, "Max_length": 21, "Min_length": 2, "missing_value_freq": round(3.0/self.unpatterned_string_blanks.size, 7)}
        
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.unpatterned_string_blanks.size)
        assert test_column.dtypes == self.unpatterned_string_blanks.dtypes
        assert any(test_column != self.unpatterned_string_blanks)
    
    def test_unpatterned_string_with_gaps_blanks(self):
        column = StringVariable(self.unpatterned_string_gaps_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = {"Name": "test", "Type": "text", "Pattern": False, "Max_length": 21, "Min_length": 2, "missing_value_freq": round(3.0/self.unpatterned_string_gaps_blanks.size, 7)}
        
        assert test_dictionary == example_dictionary
        
        test_column = column.generate(self.unpatterned_string_gaps_blanks.size)
        assert test_column.dtypes == self.unpatterned_string_gaps_blanks.dtypes
        assert any(test_column != self.unpatterned_string_gaps_blanks)
        
        
    def test_set_unpatterned_string(self):
        input_dict = {"Name": "test", "Type": "text", "Pattern": False, "Max_length": 21, "Min_length": 2, "missing_value_freq": round(3.0/self.unpatterned_string_gaps_blanks.size, 7)}
        temp_column = StringVariable(pd.Series([0], name = input_dict["Name"]))
        temp_column.set_no_pattern(
            pattern = input_dict["Pattern"],
            min_length = input_dict["Min_length"],
            max_length = input_dict["Max_length"],
            missing_freq = input_dict["missing_value_freq"],
            number_of_rows = self.unpatterned_string_gaps_blanks.size
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert input_dict == output_dict
        
    def test_set_patterned_string(self):
        chance = round(1.0/13.0, 7)
        input_dict = {'Name': 'test', 'Type': 'text', 'Pattern': True, 'Max_length': 2, 'character_number_0': {'a': chance, 'b': 0.0, 'c': chance, 'd': 0.0, 'e': chance, 'f': 0.0, 'g': chance, 'h': 0.0, 'i': chance, 'j': 0.0, 'k': chance, 'l': 0.0, 'm': chance, 'n': 0.0, 'o': chance, 'p': 0.0, 'q': chance, 'r': 0.0, 's': chance, 't': 0.0, 'u': chance, 'v': 0.0, 'w': chance, 'x': 0.0, 'y': chance, 'z': 0.0}, 'character_number_1': {'a': 0.0, 'b': chance, 'c': 0.0, 'd': chance, 'e': 0.0, 'f': chance, 'g': 0.0, 'h': chance, 'i': 0.0, 'j': chance, 'k': 0.0, 'l': chance, 'm': 0.0, 'n': chance, 'o': 0.0, 'p': chance, 'q': 0.0, 'r': chance, 's': 0.0, 't': chance, 'u': 0.0, 'v': chance, 'w': 0.0, 'x': chance, 'y': 0.0, 'z': chance}, 'missing_value_freq': round(3.0/self.patterned_string_with_blanks.size,7)}
        temp_column = StringVariable(pd.Series([0], name = input_dict["Name"]))
        temp_column.set_pattern(
            pattern = input_dict["Pattern"],
            character_frequencies = {value: input_dict[value] for value in input_dict if "character_number_" in value},
            max_length = input_dict["Max_length"],
            missing_freq = input_dict["missing_value_freq"],
            number_of_rows = self.patterned_string_with_blanks.size
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert input_dict == output_dict