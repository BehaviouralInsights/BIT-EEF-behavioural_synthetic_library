import pandas as pd
import numpy as np
import pytest
import re

from .DatetimeVariable import DatetimeVariable

THRESHOLD = 10 # This needs to match the value given in the VariableType base abstract class

class TestDatetimeVariable():
    # used https://onlinetools.com/time/calculate-average-calendar-date to get the average datetime value for testing
    
    short_series = pd.Series(["2023-01-01", "2023-11-01", "2023-01-01"], name='test')
    short_series_with_gaps = pd.Series(["2023-01-01", np.NaN, "2023-11-01", np.NAN, "2023-01-01", "", np.NaN, np.NaN, np.NAN, "", np.NaN],name='test')
    short_series_with_blanks = pd.Series(["2023-01-01", "", "2023-11-01", "", "2023-01-01", "", "", "", "", "", ""],name='test')
    short_series_with_gaps_blanks = pd.Series(["2023-01-01", np.NaN, "2023-11-01", "", "2023-01-01", pd.NaT, np.NaN, "", np.NAN, pd.NaT, ""],name='test')
    
    dates_series = pd.Series(["2021-01-12", "2021-02-01", "2023-01-24", "1980-05-23", "1978-03-12", "2021-10-06", "2019-05-23", "2002-07-17", "1998-05-12", "1990-03-01","2081-12-14", "1931-08-23", "1933-04-19", "2030-12-27", "1907-06-09"],name='test')
    dates_series_with_gaps = pd.Series(["2021-01-12", pd.NaT, "2021-02-01", "2023-01-24", "1980-05-23", "1978-03-12", "2021-10-06", "2019-05-23", pd.NaT, "2002-07-17", "1998-05-12", np.NaN, np.NaN, "1990-03-01","2081-12-14", "1931-08-23", "1933-04-19", "2030-12-27", "1907-06-09"],name='test')
    dates_series_with_blanks = pd.Series(["2021-01-12", "", "2021-02-01", "2023-01-24", "1980-05-23", "1978-03-12", "2021-10-06", "2019-05-23", "", "2002-07-17", "1998-05-12", "", "", "1990-03-01","2081-12-14", "1931-08-23", "1933-04-19", "2030-12-27", "1907-06-09"],name='test')
    dates_series_with_gaps_blanks = pd.Series(["2021-01-12", np.NaN, "2021-02-01", "2023-01-24", "1980-05-23", "1978-03-12", "2021-10-06", "2019-05-23", "", "2002-07-17", "1998-05-12", np.NAN, "", "1990-03-01","2081-12-14", "1931-08-23", "1933-04-19", "2030-12-27", "1907-06-09"],name='test')
    
    dates_series_same_avg = pd.Series(["2021-01-12", "2021-02-01", "2023-01-24", "1980-05-23", "1978-03-12", "2021-10-06", "2019-05-23", "2002-07-17", "1998-05-12", "1990-03-01"],name='test')
    
    time_series = pd.Series(["00:01:34", "01:32:22", "04:43:34", "08:50:02", "09:40:45", "10:45:45","11:12:13", "14:34:32", "15:11:59", "16:34:56", "18:32:23", "19:23:33", "19:43:33", "21:56:43", "23:10:22"],name='test')
    
    datetime_series = pd.Series(["2081-12-15 00:01:34", "2081-12-16 01:32:22", "2081-12-17 04:43:34", "2081-12-18 08:50:02", "2081-12-19 09:40:45", "2081-12-20 10:45:45","2081-12-21 11:12:13", "2081-12-22 14:34:32", "2081-12-23 15:11:59", "2081-12-24 16:34:56", "2081-12-25 18:32:23", "2081-12-26 19:23:33", "2081-12-27 19:43:33", "2081-12-28 21:56:43", "2081-12-29 23:10:22"],name='test')
    
    def test_threshold(self):
        column = DatetimeVariable(self.short_series)
        assert column.get_THRESHOLD() == THRESHOLD
        
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
        
        example_dictionary =  {"Name" : "test", "Type": "date", "earliest": "1907-06-09", "latest": "2081-12-14", "missing_value_freq": 0.0, "format": "%Y-%m-%d", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': False}
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    def test_dates_average(self): 
        column = DatetimeVariable(self.dates_series)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  {"Name": "test", "Type": "date", "earliest": "1976-03-30", "latest": "2021-01-12", "missing_value_freq": 0.0, "format": "%Y-%m-%d", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
        
    def test_dates_same_average(self):
        column = DatetimeVariable(self.dates_series_same_avg)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  {"Name": "test", "Type": "date", "earliest": "2005-08-06", "latest": "2005-08-06", "missing_value_freq": 0.0, "format": "%Y-%m-%d", '# of values in average_max_min':THRESHOLD, 'averaged_max_and_min': True}
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_same_avg.size)
        assert test_column.dtypes == self.dates_series_same_avg.dtypes
        assert any(test_column != self.dates_series_same_avg)
        assert all([str(test_column.iloc[i]) == "2005-08-06" for i in range(self.dates_series_same_avg.size)] )
    
    
    def test_dates_avg_with_gaps(self):
        column = DatetimeVariable(self.dates_series_with_gaps)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  {"Name": "test", "Type": "date", "earliest": "1976-03-30", "latest": "2021-01-12", "missing_value_freq": round(4.0/self.dates_series_with_gaps.size,7), "format": "%Y-%m-%d", '# of values in average_max_min':THRESHOLD, 'averaged_max_and_min': True}
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_gaps.size)
        assert test_column.dtypes == self.dates_series_with_gaps.dtypes
        assert any(test_column != self.dates_series_with_gaps)
    
    def test_dates_no_avg_with_gaps(self):
        column = DatetimeVariable(self.dates_series_with_gaps, average_min_max=False)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  {"Name": "test", "Type": "date", "earliest": "1907-06-09", "latest": "2081-12-14", "missing_value_freq": round(4.0/self.dates_series_with_gaps.size,7), "format": "%Y-%m-%d",'# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': False}
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_gaps.size)
        assert test_column.dtypes == self.dates_series_with_gaps.dtypes
        assert any(test_column != self.dates_series_with_gaps)
    
    def test_dates_avg_with_blanks(self):
        column = DatetimeVariable(self.dates_series_with_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  {"Name": "test", "Type": "date", "earliest": "1976-03-30", "latest": "2021-01-12", "missing_value_freq": round(4.0/self.dates_series_with_blanks.size,7), "format": "%Y-%m-%d", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_blanks.size)
        assert test_column.dtypes == self.dates_series_with_blanks.dtypes
        assert any(test_column != self.dates_series_with_blanks)
    
    def test_dates_no_avg_with_blanks(self):
        column = DatetimeVariable(self.dates_series_with_blanks, average_min_max=False)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  {"Name": "test", "Type": "date", "earliest": "1907-06-09", "latest": "2081-12-14", "missing_value_freq": round(4.0/self.dates_series_with_blanks.size,7), "format": "%Y-%m-%d",'# of values in average_max_min':THRESHOLD, 'averaged_max_and_min': False}
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_blanks.size)
        assert test_column.dtypes == self.dates_series_with_blanks.dtypes
        assert any(test_column != self.dates_series_with_blanks)
        
    
    def test_dates_avg_with_gaps_blanks(self):
        column = DatetimeVariable(self.dates_series_with_gaps_blanks)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  {"Name": "test", "Type": "date", "earliest": "1976-03-30", "latest": "2021-01-12", "missing_value_freq": round(4.0/self.dates_series_with_gaps_blanks.size,7), "format": "%Y-%m-%d", '# of values in average_max_min':THRESHOLD, 'averaged_max_and_min': True}
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_gaps_blanks.size)
        assert test_column.dtypes == self.dates_series_with_gaps_blanks.dtypes
        assert any(test_column != self.dates_series_with_gaps_blanks)
    
    def test_dates_no_avg_with_gaps_blanks(self):
        column = DatetimeVariable(self.dates_series_with_gaps_blanks, average_min_max=False)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  {"Name": "test", "Type": "date", "earliest": "1907-06-09", "latest": "2081-12-14", "missing_value_freq": round(4.0/self.dates_series_with_blanks.size,7), "format": "%Y-%m-%d", '# of values in average_max_min':THRESHOLD, 'averaged_max_and_min': False}
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series_with_gaps_blanks.size)
        assert test_column.dtypes == self.dates_series_with_gaps_blanks.dtypes
        assert any(test_column != self.dates_series_with_gaps_blanks)
        
    def test_dates_avg_new_format(self):
        column = DatetimeVariable(self.dates_series, date_format="%d/%m/%Y")
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary =  {"Name": "test", "Type": "date", "earliest": "30/03/1976", "latest": "12/01/2021", "missing_value_freq": 0.0, "format": "%d/%m/%Y", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
        
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
        
        example_dictionary = {"Name": "test", "Type": "time", "earliest": "00:01:34", "latest": "23:10:22", "missing_value_freq": 0.0, "format": "%X",'# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': False}
        
        assert test_dictionary == example_dictionary
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    def test_times_average(self):
        column = DatetimeVariable(self.time_series)
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = {"Name": "test", "Type": "time", "earliest": "09:18:46", "latest": "17:06:35", "missing_value_freq": 0.0,"format": "%X", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
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
        
        example_dictionary = {"Name": "test", "Type": "time", "earliest": "09:18:46 AM", "latest": "05:06:35 PM", "missing_value_freq": 0.0, "format": "%I:%M:%S %p", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
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
        
        example_dictionary = {"Name": "test", "Type": "datetime", "earliest": "2081-12-19 21:18:46", "latest": "2081-12-25 05:06:35", "missing_value_freq": 0.0, "format" : "%Y-%m-%d %X", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
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
        
        example_dictionary = {"Name": "test", "Type": "datetime", "earliest": "2081-12-15 00:01:34", "latest": "2081-12-29 23:10:22", "missing_value_freq": 0.0, "format" : "%Y-%m-%d %X", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': False}
        
        assert test_dictionary == example_dictionary
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
    
    def test_datetimes_average_new_format(self):
        column = DatetimeVariable(self.datetime_series, datetime_format="%d/%m/%Y %X")
        column.analyse()
        test_dictionary = column.dictionary_out()
        
        example_dictionary = {"Name": "test", "Type": "datetime", "earliest": "19/12/2081 21:18:46", "latest": "25/12/2081 05:06:35", "missing_value_freq": 0.0, "format" : "%d/%m/%Y %X", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
        #possible rounding error in comparison with external value (17:06:36)? probably not significant
        
        assert test_dictionary == example_dictionary
        
        assert test_dictionary == example_dictionary
        test_column = column.generate(self.dates_series.size)
        assert test_column.dtypes == self.dates_series.dtypes
        assert any(test_column != self.dates_series)
        
    def test_datetimes_set_values_new_format(self):
        input_dict = {"Name": "test", "Type": "datetime", "earliest": "19/12/2081 21:18:46", "latest": "25/12/2081 05:06:35", "missing_value_freq": 0.0, "format" : "%d/%m/%Y %X",'# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
        temp_column=DatetimeVariable(
            pd.Series([0], name = input_dict["Name"]), 
            average_min_max=input_dict['averaged_max_and_min'],
            datetime_format=input_dict['format']
        )
        temp_column.set(
            type = input_dict["Type"],
            earliest = input_dict["earliest"],
            latest = input_dict["latest"],
            missing_freq = input_dict["missing_value_freq"],
            number_of_rows = self.datetime_series.size,
            no_vals_in_threshold = input_dict['# of values in average_max_min']
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert output_dict == input_dict
        
    def test_times_set_values_new_format(self):
        input_dict = {"Name": "test", "Type": "time", "earliest": "09:18:46 AM", "latest": "05:06:35 PM", "missing_value_freq": 0.0, "format": "%I:%M:%S %p", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
        temp_column=DatetimeVariable(
            pd.Series([0], name = input_dict["Name"]), 
            average_min_max=input_dict['averaged_max_and_min'],
            time_format=input_dict['format']
        )
        temp_column.set(
            type = input_dict["Type"],
            earliest = input_dict["earliest"],
            latest = input_dict["latest"],
            missing_freq = input_dict["missing_value_freq"],
            number_of_rows = self.time_series.size,
            no_vals_in_threshold = input_dict['# of values in average_max_min']
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert output_dict == input_dict
        
    def test_dates_set_values_new_format(self):
        input_dict = {"Name": "test", "Type": "date", "earliest": "30/03/1976", "latest": "12/01/2021", "missing_value_freq": 0.0, "format": "%d/%m/%Y", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
        temp_column=DatetimeVariable(
            pd.Series([0], name = input_dict["Name"]), 
            average_min_max=input_dict['averaged_max_and_min'],
            date_format=input_dict['format']
        )
        temp_column.set(
            type = input_dict["Type"],
            earliest = input_dict["earliest"],
            latest = input_dict["latest"],
            missing_freq = input_dict["missing_value_freq"],
            number_of_rows = self.dates_series.size,
            no_vals_in_threshold = input_dict['# of values in average_max_min']
        )
        
        output_dict = temp_column.dictionary_out()
        
        assert output_dict == input_dict
        
    def test_trigger_invalid_type(self):
        input_dict = {"Name": "test", "Type": "cheese", "earliest": "30/03/1976", "latest": "12/01/2021", "missing_value_freq": 0.0, "format": "%d/%m/%Y", '# of values in average_max_min': THRESHOLD, 'averaged_max_and_min': True}
        temp_column=DatetimeVariable(
            pd.Series([0], name = input_dict["Name"]), 
            average_min_max=input_dict['averaged_max_and_min'],
            date_format=input_dict['format']
        )
        message = f"Invalid value of datetime parameter Type in column {input_dict['Name']}."
        with pytest.raises(ValueError, match=re.escape(message)):
            temp_column.set(
                type = input_dict["Type"],
                earliest = input_dict["earliest"],
                latest = input_dict["latest"],
                missing_freq = input_dict["missing_value_freq"],
                number_of_rows = self.dates_series.size,
                no_vals_in_threshold = input_dict['# of values in average_max_min']
            )
            
    def test_trigger_insufficent_threshold(self):
        input_dict = {"Name": "test", "Type": "date", "earliest": "30/03/1976", "latest": "12/01/2021", "missing_value_freq": 0.0, "format": "%d/%m/%Y", '# of values in average_max_min': 2, 'averaged_max_and_min': True}
        temp_column=DatetimeVariable(
            pd.Series([0], name = input_dict["Name"]), 
            average_min_max=input_dict['averaged_max_and_min'],
            date_format=input_dict['format']
        )
        message = f"Warning: external setting of threshold for averaging is {input_dict['# of values in average_max_min']} but the internal value is {THRESHOLD}. The input is unsafe with respect to disclosure."
        with pytest.raises(ValueError, match=re.escape(message)):
            temp_column.set(
                type = input_dict["Type"],
                earliest = input_dict["earliest"],
                latest = input_dict["latest"],
                missing_freq = input_dict["missing_value_freq"],
                number_of_rows = self.dates_series.size,
                no_vals_in_threshold = input_dict['# of values in average_max_min']
            )