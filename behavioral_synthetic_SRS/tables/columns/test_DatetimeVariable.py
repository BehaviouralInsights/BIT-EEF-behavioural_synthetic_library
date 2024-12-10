import pandas as pd
import numpy as np
import pytest
import re

from .DatetimeVariable import DatetimeVariable

THRESHOLD = 10 # This needs to match the value given in the VariableType base abstract class


    # used https://onlinetools.com/time/calculate-average-calendar-date to get the average datetime value for testing
    
    short_series = 
    short_series_with_gaps = 
    short_series_with_blanks = 
    short_series_with_gaps_blanks = 
    
    dates_series = 
    dates_series_with_gaps = 
    dates_series_with_blanks = 
    dates_series_with_gaps_blanks = 
    
    dates_series=
    
    time_series = 
    
    datetime_series = 
    
    def test_threshold(self):
        column = DatetimeVariable(self.short_series)
        assert column.THRESHOLD == THRESHOLD
        
    def test_short_series_error(self):
        column = DatetimeVariable(self.short_series)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
    
    def test_short_series_with_gaps(self):
        column = DatetimeVariable(self.short_series_with_gaps)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
    
    def test_short_series_with_blanks(self):
        column = DatetimeVariable(self.short_series_with_blanks)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
    
    def test_short_series_with_gaps_blanks(self):
        column = DatetimeVariable(self.short_series_with_gaps_blanks)
        message = f"Insuffucient number of values in series to produce disclosure safe values (less than {THRESHOLD})"
        with pytest.raises(ValueError, match=re.escape(message)):
            column.analyse()
    
    def test_dates_no_average(self):
        column = DatetimeVariable(self.dates_series, average_min_max=False)
       
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    def test_dates_average(self): 
        column = DatetimeVariable(self.dates_series)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
        
    def test_dates_same_average(self):
        column = DatetimeVariable(self.dates_series_same_avg)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_same_avg.size)
        assert test_column.dtypes == self.dates_series_same_avg.dtypes
        assert any(test_column != self.dates_series_same_avg)
        assert all([str(test_column.iloc[i]) == "2005-08-06" for i in range(self.dates_series_same_avg.size)] )
    
    
    def test_dates_avg_with_gaps(self):
        column = DatetimeVariable(self.dates_series_with_gaps)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_gaps.size)
        assert test_column.dtypes == self.dates_series_with_gaps.dtypes
        assert any(test_column != self.dates_series_with_gaps)
    
    def test_dates_no_avg_with_gaps(self):
        column = DatetimeVariable(self.dates_series_with_gaps, average_min_max=False)
        print(column.column)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_gaps.size)
        # Turning off the next assertion as there seems to be some kind of data conversion going on that breaks it
        # It doesn't check anything important anyway as output defaults to correct format -- IOT 2024-03-12
        assert test_column.dtypes == self.dates_series_with_gaps.dtypes
        assert any(test_column != self.dates_series_with_gaps)
    
    def test_dates_avg_with_blanks(self):
        column = DatetimeVariable(self.dates_series_with_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_blanks.size)
        assert test_column.dtypes == self.dates_series_with_blanks.dtypes
        assert any(test_column != self.dates_series_with_blanks)
    
    def test_dates_no_avg_with_blanks(self):
        column = DatetimeVariable(self.dates_series_with_blanks, average_min_max=False)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_blanks.size)
        assert test_column.dtypes == self.dates_series_with_blanks.dtypes
        assert any(test_column != self.dates_series_with_blanks)
        
    
    def test_dates_avg_with_gaps_blanks(self):
        column = DatetimeVariable(self.dates_series_with_gaps_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_gaps_blanks.size)
        assert test_column.dtypes == self.dates_series_with_gaps_blanks.dtypes
        assert any(test_column != self.dates_series_with_gaps_blanks)
    
    def test_dates_no_avg_with_gaps_blanks(self):
        column = DatetimeVariable(self.dates_series_with_gaps_blanks, average_min_max=False)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_gaps_blanks.size)
        assert test_column.dtypes == self.dates_series_with_gaps_blanks.dtypes
        assert any(test_column != self.dates_series_with_gaps_blanks)
        
    def test_dates_avg_new_format(self):
        column = DatetimeVariable(self.dates_series, date_format="%d/%m/%Y")
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    ## probably don't need to test gaps for datetime and time as these seem to be handled fine
    ## probably do want to handle average/not_average and format passing for each case though
    
    def test_times_no_average(self):
        column = DatetimeVariable(self.time_series, average_min_max=False)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        
        assert test_dictionary == example_dictionary
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    def test_times_average(self):
        column = DatetimeVariable(self.time_series)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        #possible rounding error in comparison with external value (17:06:36)? probably not significant
        
        assert test_dictionary == example_dictionary
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    def test_times_average_new_format(self):
        column = DatetimeVariable(self.time_series, time_format="%I:%M:%S %p")
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        #possible rounding error in comparison with external value (17:06:36)? probably not significant
        
        assert test_dictionary == example_dictionary
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    def test_datetimes_average(self):
        column = DatetimeVariable(self.datetime_series)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        #possible rounding error in comparison with external value (17:06:36)? probably not significant
        
        assert test_dictionary == example_dictionary
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    
    def test_datetimes_no_average(self):
        column = DatetimeVariable(self.datetime_series, average_min_max=False)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        
        assert test_dictionary == example_dictionary
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    def test_datetimes_average_new_format(self):
        column = DatetimeVariable(self.datetime_series, datetime_format="%d/%m/%Y %X")
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = 
        #possible rounding error in comparison with external value (17:06:36)? probably not significant
        
        assert test_dictionary == example_dictionary
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
        
    def test_datetimes_set_values_new_format(self):
        input_dict = 
        temp_column=DatetimeVariable(
                )
        temp_column.set(
            type = input_dict["Type"],
         
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert output_dict == input_dict
        
    def test_times_set_values_new_format(self):
        input_dict = 
        temp_column=DatetimeVariable(
           
                   )
        temp_column.set(
       
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert output_dict == input_dict
        
    def test_dates_set_values_new_format(self):
        input_dict =
        te
        )
        temp_column.set(
           
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert output_dict == input_dict
        
    def test_trigger_invalid_type(self):
        input_dict = 
        temp_column=DatetimeVariable(
           
        )
        message = f"Invalid value of datetime parameter Type in column {input_dict['Name']}."
        with pytest.raises(ValueError, match=re.escape(message)):
            temp_column.set(
               
            
    def test_trigger_insufficent_threshold(self):
        input_dict = 
        temp_column=DatetimeVariable(
           
        )
        message = f"Warning: external setting of threshold for averaging is {input_dict['# of values in average_max_min']} but the internal value is {THRESHOLD}. The input is unsafe with respect to disclosure."
        with pytest.raises(ValueError, match=re.escape(message)):
            temp_column.set(
               
