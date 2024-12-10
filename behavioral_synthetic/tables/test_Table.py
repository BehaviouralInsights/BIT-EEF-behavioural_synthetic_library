import pandas as pd
import numpy as np
import re
import pytest

from .Table import Table

class TestTable():
    test_table = pd.DataFrame.from_dict({
        "A": [np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN],
        "B": ["Y", "N", "N", "Y", "Y", "Y", "N", "N","N", "Y", "N", "N", "N", "Y", "N"],
        "C": [1, 0, 0, 1, 1, 1, 0, 0,0, 1, 0, 0, 0, 1, 0],
        "D": [12, 45, 12, 78, 20, 33, 1, 1000, 20, 56, 89, 34,56.03, 45, 3445],
        "E": ["Gwyr", "a aeth", "Gatraeth oedd ffraith", "eu llu", "glasfedd", "eu", "hancwyn", "a'u gwenwyn", "fu", "trichant", "trwy peiriant", "yn catau", "ac", "gwedu elwch","tawelwch fu"],
        "F": ["2081-12-15 00:01:34", "2081-12-16 01:32:22", "2081-12-17 04:43:34", "2081-12-18 08:50:02", "2081-12-19 09:40:45", "2081-12-20 10:45:45","2081-12-21 11:12:13", "2081-12-22 14:34:32", "2081-12-23 15:11:59", "2081-12-24 16:34:56", "2081-12-25 18:32:23", "2081-12-26 19:23:33", "2081-12-27 19:43:33", "2081-12-28 21:56:43", "2081-12-29 23:10:22"],
        "G": ["2081-12-15", "2081-12-16", "2081-12-17", "2081-12-18", "2081-12-19", "2081-12-20","2081-12-21", "2081-12-22", "2081-12-23", "2081-12-24", "2081-12-25", "2081-12-26", "2081-12-27", "2081-12-28", "2081-12-29"],
        "H" : ["00:01:34", "01:32:22", "04:43:34", "08:50:02", "09:40:45", "10:45:45","11:12:13", "14:34:32", "15:11:59", "16:34:56", "18:32:23", "19:23:33", "19:43:33", "21:56:43", "23:10:22"],
        "I" : ["ab", "cd", "ef", "gh", "ij", "kl", "mn", "op", "qr", "st", "uv", "wx", "yz", "ba", "dc"]
    })
    
    
    test_dict = {'Table_name': 'testTable',   # have checked, should be normal
                 'Table_type': 'normal_table', 
                 'Number_of_rows': 15, 
                 'Column_details': [
                     {
                         'Name': 'A', 
                         'Type': 'empty', 
                         'all_values': "NaN"
                         }, 
                     {
                         'N': 0.6, 
                         'Y': 0.4, 
                         'Type': 'categorical', 
                         'Name': 'B'
                         }, 
                     {
                         0: 0.6, 
                         1: 0.4, 
                         'Type': 'categorical', 
                         'Name': 'C'
                         }, 
                     {
                        'Name': 'D', 
                        'Type': 'numeric', 
                        'decimal_precision': 3, 
                        'mean': 329.7353333, 
                        'standard_deviation': 897.0112481, 
                        'minimum': 27.8, 'maximum': 488.103, 
                        'is_integer': False, 
                        'missing_value_freq': 0.0, 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                        'Name': 'E', 
                        'Type': 'text', 
                        'Pattern': False, 
                        'Max_length': 21, 
                        'Min_length': 2, 
                        'missing_value_freq': 0.0
                        }, 
                     {
                        'Name': 'F', 
                        'Type': 'datetime', 
                        'earliest': '2081-12-19 21:18:46', 
                        'latest': '2081-12-25 05:06:35', 
                        'missing_value_freq': 0.0, 
                        'format': '%Y-%m-%d %X', 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                        'Name': 'G', 
                        'Type': 'date',   
                        'earliest': '2081-12-19', 
                        'latest': '2081-12-24', 
                        'missing_value_freq': 0.0, 
                        'format': '%Y-%m-%d', 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                        'Name': 'H', 
                        'Type': 'time', 
                        'earliest': '09:18:46', 
                        'latest': '17:06:35', 
                        'missing_value_freq': 0.0, 
                        'format': '%X', 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                         'Name': 'I', 
                         'Type': 'text', 
                         'Pattern': True, 
                         'Max_length': 2, 
                         'character_number_0': {'a': 0.0666667, 'b': 0.0666667, 'c': 0.0666667, 'd': 0.0666667, 'e': 0.0666667, 'f': 0.0, 'g': 0.0666667, 'h': 0.0, 'i': 0.0666667, 'j': 0.0, 'k': 0.0666667, 'l': 0.0, 'm': 0.0666667, 'n': 0.0, 'o': 0.0666667, 'p': 0.0, 'q': 0.0666667, 'r': 0.0, 's': 0.0666667, 't': 0.0, 'u': 0.0666667, 'v': 0.0, 'w': 0.0666667, 'x': 0.0, 'y': 0.0666667, 'z': 0.0}, 
                         'character_number_1': {'a': 0.0666667, 'b': 0.0666667, 'c': 0.0666667, 'd': 0.0666667, 'e': 0.0, 'f': 0.0666667, 'g': 0.0, 'h': 0.0666667, 'i': 0.0, 'j': 0.0666667, 'k': 0.0, 'l': 0.0666667, 'm': 0.0, 'n': 0.0666667, 'o': 0.0, 'p': 0.0666667, 'q': 0.0, 'r': 0.0666667, 's': 0.0, 't': 0.0666667, 'u': 0.0, 'v': 0.0666667, 'w': 0.0, 'x': 0.0666667, 'y': 0.0, 'z': 0.0666667}, 
                         'missing_value_freq': 0.0}]}
    
    test_dict_type_error = {'Table_name': 'testTable',   # have checked, should be normal
                 'Table_type': 'normal_table', 
                 'Number_of_rows': 15, 
                 'Column_details': [
                     {
                         'Name': 'A', 
                         'Type': 'ey', # error
                         'all_values': "NaN"
                         }, 
                     {
                         'N': 0.6, 
                         'Y': 0.4, 
                         'Type': 'categorical', 
                         'Name': 'B'
                         }, 
                     {
                         0: 0.6, 
                         1: 0.4, 
                         'Type': 'categorical', 
                         'Name': 'C'
                         }, 
                     {
                        'Name': 'D', 
                        'Type': 'numeric', 
                        'decimal_precision': 3, 
                        'mean': 329.7353333, 
                        'standard_deviation': 897.0112481, 
                        'minimum': 27.8, 'maximum': 488.103, 
                        'is_integer': False, 
                        'missing_value_freq': 0.0, 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                        'Name': 'E', 
                        'Type': 'text', 
                        'Pattern': False, 
                        'Max_length': 21, 
                        'Min_length': 2, 
                        'missing_value_freq': 0.0
                        }, 
                     {
                        'Name': 'F', 
                        'Type': 'datetime', 
                        'earliest': '2081-12-19 21:18:46', 
                        'latest': '2081-12-25 05:06:35', 
                        'missing_value_freq': 0.0, 
                        'format': '%Y-%m-%d %X', 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                        'Name': 'G', 
                        'Type': 'date',   
                        'earliest': '2081-12-19', 
                        'latest': '2081-12-24', 
                        'missing_value_freq': 0.0, 
                        'format': '%Y-%m-%d', 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                        'Name': 'H', 
                        'Type': 'time', 
                        'earliest': '09:18:46', 
                        'latest': '17:06:35', 
                        'missing_value_freq': 0.0, 
                        'format': '%X', 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                         'Name': 'I', 
                         'Type': 'text', 
                         'Pattern': True, 
                         'Max_length': 2, 
                         'character_number_0': {'a': 0.0666667, 'b': 0.0666667, 'c': 0.0666667, 'd': 0.0666667, 'e': 0.0666667, 'f': 0.0, 'g': 0.0666667, 'h': 0.0, 'i': 0.0666667, 'j': 0.0, 'k': 0.0666667, 'l': 0.0, 'm': 0.0666667, 'n': 0.0, 'o': 0.0666667, 'p': 0.0, 'q': 0.0666667, 'r': 0.0, 's': 0.0666667, 't': 0.0, 'u': 0.0666667, 'v': 0.0, 'w': 0.0666667, 'x': 0.0, 'y': 0.0666667, 'z': 0.0}, 
                         'character_number_1': {'a': 0.0666667, 'b': 0.0666667, 'c': 0.0666667, 'd': 0.0666667, 'e': 0.0, 'f': 0.0666667, 'g': 0.0, 'h': 0.0666667, 'i': 0.0, 'j': 0.0666667, 'k': 0.0, 'l': 0.0666667, 'm': 0.0, 'n': 0.0666667, 'o': 0.0, 'p': 0.0666667, 'q': 0.0, 'r': 0.0666667, 's': 0.0, 't': 0.0666667, 'u': 0.0, 'v': 0.0666667, 'w': 0.0, 'x': 0.0666667, 'y': 0.0, 'z': 0.0666667}, 
                         'missing_value_freq': 0.0}]}
    
    test_dict_text_error = {'Table_name': 'testTable',   # have checked, should be normal
                 'Table_type': 'normal_table', 
                 'Number_of_rows': 15, 
                 'Column_details': [
                     {
                         'Name': 'A', 
                         'Type': 'empty', 
                         'all_values': "NaN"
                         }, 
                     {
                         'N': 0.6, 
                         'Y': 0.4, 
                         'Type': 'categorical', 
                         'Name': 'B'
                         }, 
                     {
                         0: 0.6, 
                         1: 0.4, 
                         'Type': 'categorical', 
                         'Name': 'C'
                         }, 
                     {
                        'Name': 'D', 
                        'Type': 'numeric', 
                        'decimal_precision': 3, 
                        'mean': 329.7353333, 
                        'standard_deviation': 897.0112481, 
                        'minimum': 27.8, 'maximum': 488.103, 
                        'is_integer': False, 
                        'missing_value_freq': 0.0, 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                        'Name': 'E', 
                        'Type': 'text', 
                        'Pattern': False, 
                        'Max_length': 21, 
                        'Min_length': 2, 
                        'missing_value_freq': 0.0
                        }, 
                     {
                        'Name': 'F', 
                        'Type': 'datetime', 
                        'earliest': '2081-12-19 21:18:46', 
                        'latest': '2081-12-25 05:06:35', 
                        'missing_value_freq': 0.0, 
                        'format': '%Y-%m-%d %X', 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                        'Name': 'G', 
                        'Type': 'date',   
                        'earliest': '2081-12-19', 
                        'latest': '2081-12-24', 
                        'missing_value_freq': 0.0, 
                        'format': '%Y-%m-%d', 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                        'Name': 'H', 
                        'Type': 'time', 
                        'earliest': '09:18:46', 
                        'latest': '17:06:35', 
                        'missing_value_freq': 0.0, 
                        'format': '%X', 
                        'averaged_max_and_min': True, 
                        '# of values in average_max_min': 10
                        }, 
                     {
                         'Name': 'I', 
                         'Type': 'text', 
                         'Pattern': None, #error
                         'Max_length': 2, 
                         'character_number_0': {'a': 0.0666667, 'b': 0.0666667, 'c': 0.0666667, 'd': 0.0666667, 'e': 0.0666667, 'f': 0.0, 'g': 0.0666667, 'h': 0.0, 'i': 0.0666667, 'j': 0.0, 'k': 0.0666667, 'l': 0.0, 'm': 0.0666667, 'n': 0.0, 'o': 0.0666667, 'p': 0.0, 'q': 0.0666667, 'r': 0.0, 's': 0.0666667, 't': 0.0, 'u': 0.0666667, 'v': 0.0, 'w': 0.0666667, 'x': 0.0, 'y': 0.0666667, 'z': 0.0}, 
                         'character_number_1': {'a': 0.0666667, 'b': 0.0666667, 'c': 0.0666667, 'd': 0.0666667, 'e': 0.0, 'f': 0.0666667, 'g': 0.0, 'h': 0.0666667, 'i': 0.0, 'j': 0.0666667, 'k': 0.0, 'l': 0.0666667, 'm': 0.0, 'n': 0.0666667, 'o': 0.0, 'p': 0.0666667, 'q': 0.0, 'r': 0.0666667, 's': 0.0, 't': 0.0666667, 'u': 0.0, 'v': 0.0666667, 'w': 0.0, 'x': 0.0666667, 'y': 0.0, 'z': 0.0666667}, 
                         'missing_value_freq': 0.0}]}
    
    def test_from_table(self):
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse(decimal_accuracy=3)
        
        out_dict = table.dictionary_out()
        assert out_dict == self.test_dict 
        
        pass
    
    def test_with_col_input(self):
        columns = [ 
            {
                "Type": "empty"
                },
            {
                "Type": "categorical"
                },
            {
                "Type": "categorical"
                },
            {
                "Type": "numeric",
                "decimal_precision": 3,
                "averaged_max_and_min": True
                },
            {
                "Type": "text"
                },
            {
                "Type": "datetime",
                "format": '%Y-%m-%d %X', 
                'averaged_max_and_min': True, 
                },
            {
                "Type": "date",
                "format": '%Y-%m-%d', 
                'averaged_max_and_min': True, 
                 },
            {
                "Type": "time",
                "format": '%X', 
                'averaged_max_and_min': True, 
                },
            {
                "Type": "text"
                }
            ]
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse_with_column_list(columns_list=columns)
        
        new_dict = table.dictionary_out()
        
        assert new_dict == self.test_dict
    
    def test_from_dict(self):
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=self.test_dict)
        
        new_dict = table.dictionary_out()
        assert new_dict == self.test_dict
        
    def test_table_dict_type_error(self):
        table = Table(table=pd.DataFrame(), table_name="")
        message = f"Type of column A is ey: this is not an allowed value."
        with pytest.raises(ValueError, match=re.escape(message)):
            table.read_in_table(table_definition=self.test_dict_type_error)
    
    def test_table_dict_text_pat_error(self):
        table = Table(table=pd.DataFrame(), table_name="")
        message = f"Pattern value in column I is neither true or false."
        with pytest.raises(ValueError, match=re.escape(message)):
            table.read_in_table(table_definition=self.test_dict_text_error)
    
    def test_column_def_type_error(self):
        columns_bad = [ 
            {
                "Type": "empty"
                },
            {
                "Type": "categorical"
                },
            {
                "Type": "categorical"
                },
            {
                "Type": "numeric",
                "decimal_precision": 3,
                "averaged_max_and_min": True
                },
            {
                "Type": "text"
                },
            {
                "Type": "datetime",
                "format": '%Y-%m-%d %X', 
                'averaged_max_and_min': True, 
                },
            {
                "Type": "date",
                "format": '%Y-%m-%d', 
                'averaged_max_and_min': True, 
                 },
            {
                "Type": "t",
                "format": '%X', 
                'averaged_max_and_min': True, 
                },
            {
                "Type": "text"
                }
            ]
        table = Table(table=self.test_table, table_name="testTable")
        message = f"Type of column H is defined as t: this is not an allowed value."
        with pytest.raises(ValueError, match=re.escape(message)):
            table.analyse_with_column_list(columns_list=columns_bad)
        
    def test_false_conversion_numeric(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column ={
            'Name': 'D', 
            'Type': 'numeric', 
            'decimal_precision': 3, 
            'mean': 329.7353333, 
            'standard_deviation': 897.0112481, 
            'minimum': 27.8, 'maximum': 488.103, 
            'is_integer': "False", 
            'missing_value_freq': 0.0, 
            'averaged_max_and_min': "False", 
            '# of values in average_max_min': 10
         }
        
        #test false
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)
        
        new_dict = table.dictionary_out()
        assert new_dict["Column_details"][0]['is_integer'] != 'False'
        assert new_dict["Column_details"][0]['averaged_max_and_min'] != 'False'
        assert not new_dict["Column_details"][0]['is_integer']
        assert not new_dict["Column_details"][0]['averaged_max_and_min'] 
        
    def test_true_conversion_numeric(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column ={
            'Name': 'D', 
            'Type': 'numeric', 
            'decimal_precision': 3, 
            'mean': 329.7353333, 
            'standard_deviation': 897.0112481, 
            'minimum': 27.8, 'maximum': 488.103, 
            'is_integer': "True", 
            'missing_value_freq': 0.0, 
            'averaged_max_and_min': "True", 
            '# of values in average_max_min': 10
         }
        
        #test false
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)
        
        new_dict = table.dictionary_out()
        assert new_dict["Column_details"][0]['is_integer'] != 'True'
        assert new_dict["Column_details"][0]['averaged_max_and_min'] != 'True'
        assert new_dict["Column_details"][0]['is_integer']
        assert new_dict["Column_details"][0]['averaged_max_and_min'] 
        
    def test_false_conversion_date(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column = {
            'Name': 'G', 
            'Type': 'date',   
            'earliest': '2081-12-19', 
            'latest': '2081-12-24', 
            'missing_value_freq': 0.0, 
            'format': '%Y-%m-%d', 
            'averaged_max_and_min': "False", 
            '# of values in average_max_min': 10
            }
        
            
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)

        new_dict = table.dictionary_out()
        
        assert new_dict["Column_details"][0]['averaged_max_and_min'] != 'False'
        assert not new_dict["Column_details"][0]['averaged_max_and_min'] 
        
    def test_true_conversion_date(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column = {
            'Name': 'G', 
            'Type': 'date',   
            'earliest': '2081-12-19', 
            'latest': '2081-12-24', 
            'missing_value_freq': 0.0, 
            'format': '%Y-%m-%d', 
            'averaged_max_and_min': "True", 
            '# of values in average_max_min': 10
            }
        
            
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)

        new_dict = table.dictionary_out()
        
        assert new_dict["Column_details"][0]['averaged_max_and_min'] != 'True'
        assert new_dict["Column_details"][0]['averaged_max_and_min']      


# Need tests for no format cases for date/time/datetime

    def test_false_conversion_datetime(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column =  {
            'Name': 'F', 
            'Type': 'datetime', 
            'earliest': '2081-12-19 21:18:46', 
            'latest': '2081-12-25 05:06:35', 
            'missing_value_freq': 0.0, 
            'format': '%Y-%m-%d %X', 
            'averaged_max_and_min': 'False', 
            '# of values in average_max_min': 10
            }
        
            
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)

        new_dict = table.dictionary_out()
        
        assert new_dict["Column_details"][0]['averaged_max_and_min'] != 'False'
        assert not new_dict["Column_details"][0]['averaged_max_and_min']  
        
    def test_true_conversion_datetime(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column =  {
            'Name': 'F', 
            'Type': 'datetime', 
            'earliest': '2081-12-19 21:18:46', 
            'latest': '2081-12-25 05:06:35', 
            'missing_value_freq': 0.0, 
            'format': '%Y-%m-%d %X', 
            'averaged_max_and_min': 'True', 
            '# of values in average_max_min': 10
            }
        
            
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)

        new_dict = table.dictionary_out()
        
        assert new_dict["Column_details"][0]['averaged_max_and_min'] != 'True'
        assert new_dict["Column_details"][0]['averaged_max_and_min']  
        
    def test_false_conversion_time(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column =  {
            'Name': 'H', 
            'Type': 'time', 
            'earliest': '09:18:46', 
            'latest': '17:06:35', 
            'missing_value_freq': 0.0, 
            'format': '%X', 
            'averaged_max_and_min': "False", 
            '# of values in average_max_min': 10
        }
        
            
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)

        new_dict = table.dictionary_out()
        
        assert new_dict["Column_details"][0]['averaged_max_and_min'] != 'False'
        assert not new_dict["Column_details"][0]['averaged_max_and_min']  
        
    def test_true_conversion_time(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column =  {
            'Name': 'H', 
            'Type': 'time', 
            'earliest': '09:18:46', 
            'latest': '17:06:35', 
            'missing_value_freq': 0.0, 
            'format': '%X', 
            'averaged_max_and_min': "True", 
            '# of values in average_max_min': 10
        }
        
            
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)

        new_dict = table.dictionary_out()
        
        assert new_dict["Column_details"][0]['averaged_max_and_min'] != 'True'
        assert new_dict["Column_details"][0]['averaged_max_and_min']
         
    def test_unpatterned_conversion(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column =  {
            'Name': 'E', 
            'Type': 'text', 
            'Pattern': "False", 
            'Max_length': 21, 
            'Min_length': 2, 
            'missing_value_freq': 0.0
        }
        
            
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)

        new_dict = table.dictionary_out()
        
        assert new_dict["Column_details"][0]['Pattern'] != 'False'
        assert not new_dict["Column_details"][0]['Pattern'] 
        
    def test_patterned_conversion(self):
        table_base = {
            'Table_name': 'testTable',   # have checked, should be normal
            'Table_type': 'normal_table', 
            'Number_of_rows': 15, 
            'Column_details': []
            }
        
        column ={
            'Name': 'I', 
            'Type': 'text', 
            'Pattern': "True",
            'Max_length': 2, 
            'character_number_0': {'a': 0.0666667, 'b': 0.0666667, 'c': 0.0666667, 'd': 0.0666667, 'e': 0.0666667, 'f': 0.0, 'g': 0.0666667, 'h': 0.0, 'i': 0.0666667, 'j': 0.0, 'k': 0.0666667, 'l': 0.0, 'm': 0.0666667, 'n': 0.0, 'o': 0.0666667, 'p': 0.0, 'q': 0.0666667, 'r': 0.0, 's': 0.0666667, 't': 0.0, 'u': 0.0666667, 'v': 0.0, 'w': 0.0666667, 'x': 0.0, 'y': 0.0666667, 'z': 0.0}, 
            'character_number_1': {'a': 0.0666667, 'b': 0.0666667, 'c': 0.0666667, 'd': 0.0666667, 'e': 0.0, 'f': 0.0666667, 'g': 0.0, 'h': 0.0666667, 'i': 0.0, 'j': 0.0666667, 'k': 0.0, 'l': 0.0666667, 'm': 0.0, 'n': 0.0666667, 'o': 0.0, 'p': 0.0666667, 'q': 0.0, 'r': 0.0666667, 's': 0.0, 't': 0.0666667, 'u': 0.0, 'v': 0.0666667, 'w': 0.0, 'x': 0.0666667, 'y': 0.0, 'z': 0.0666667}, 
            'missing_value_freq': 0.0
        }
        
            
        table_base['Column_details'].append(column)
        table = Table(table=pd.DataFrame(), table_name="")
        table.read_in_table(table_definition=table_base)

        new_dict = table.dictionary_out()
        
        assert new_dict["Column_details"][0]['Pattern'] != 'True'
        assert new_dict["Column_details"][0]['Pattern'] 