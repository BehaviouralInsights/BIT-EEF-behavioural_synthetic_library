import pandas as pd
import numpy as np
import pytest
import re

from .VariableType import VariableType

THRESHOLD = 10  # This needs to match the value given in the VariableType base abstract class

class inheriting_class(VariableType):
    # this is a stub class that lets us test the general features of the base class
    # can't access base class directly since the constructor is abstract
    # similarly some methods can't be accessed directly as they're abstract
    
    def __init__(self, column: pd.Series):
        super().__init__(column, "dummy")
        
    def dictionary_out(self) -> dict:
        return super().dictionary_out()
    
    def analyse(self):
        return super().analyse()
    
    def generate(self, new_column_length: int) -> pd.Series:
        return super().generate(new_column_length)

class TestVariableType():
    
    series = 
    series_missing =
    short_series = 
    missing_series =
    
    def test_threshold(self):
        test_column = inheriting_class(self.series)
        assert test_column.THRESHOLD == THRESHOLD
    
    def test_analyse_missingness(self):
        # this is just a simple check to show it works
        # more sophisticated tests for different types are included in the other class definitions
        test_column = inheriting_class(self.series_missing)
        test_length, test_missing, test_values = test_column.analyse_missingness()
        assert test_length == self.series_missing.size
        assert test_values == self.series_missing.size - 3
        assert test_missing == 3
    
    def test_too_short_series(self):
        test_column = inheriting_class(self.short_series)
        with pytest.raises(ValueError, match=re.escape('Insuffucient number of values in series to produce disclosure safe values (less than 10)')):
            test_length, test_missing, test_values = test_column.analyse_missingness()
    
    def test_too_missing_series(self):
        test_column = inheriting_class(self.missing_series)
        with pytest.raises(ValueError, match=re.escape('Insuffucient number of values in series to produce disclosure safe values (less than 10)')):
            test_length, test_missing, test_values = test_column.analyse_missingness()
    
    def test_analyse(self):
        test_column = inheriting_class(self.series)
        with pytest.raises(NotImplementedError):
            test_column.generate(self.series.size)
    
    def test_generate(self):
        test_column = inheriting_class(self.series)
        with pytest.raises(NotImplementedError):
            test_column.generate(self.series.size)
    
    def test_dictionary_out(self):
        test_column = inheriting_class(self.series)
        with pytest.raises(NotImplementedError):
            test_column.dictionary_out()
