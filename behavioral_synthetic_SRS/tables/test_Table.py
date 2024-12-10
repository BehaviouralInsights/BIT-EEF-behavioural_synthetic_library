import pandas as pd
import numpy as np
import re
import pytest

from .Table import Table

class TestTable():
    test_table = 
    
    
    test_dict = 
    
    test_dict_type_error =
    
    test_dict_text_error =
    
    def test_from_table(self):
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse(decimal_accuracy=3)
        
        out_dict = table.dictionary_out()
        assert out_dict == self.test_dict 
        
        pass
    
    def test_with_col_input(self):
        columns = [ 
        
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
      
            ]
        table = Table(table=self.test_table, table_name="testTable")
        message = f"Type of column H is defined as t: this is not an allowed value."
        with pytest.raises(ValueError, match=re.escape(message)):
            table.analyse_with_column_list(columns_list=columns_bad)
            
    def test_col_num_true(self):
        
        coldef =  [ 
            {
         
            ]
            
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse_with_column_list(columns_list=coldef)
        
        new_dict = table.dictionary_out()
        assert new_dict['Column_details'][3]['averaged_max_and_min'] !="True"
        assert new_dict['Column_details'][3]['averaged_max_and_min']
            
    def test_col_num_false(self):
        coldef =  [ 
      
            ]
            
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse_with_column_list(columns_list=coldef)
        
        new_dict = table.dictionary_out()
        assert new_dict['Column_details'][3]['averaged_max_and_min'] !="False"
        assert not new_dict['Column_details'][3]['averaged_max_and_min']
        
    def test_col_date_true(self):
        
        coldef =  [ 
          
            ]
        
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse_with_column_list(columns_list=coldef)
        
        new_dict = table.dictionary_out()
        assert new_dict['Column_details'][6]['averaged_max_and_min'] !="True"
        assert new_dict['Column_details'][6]['averaged_max_and_min']
        
        
    def test_col_date_false(self):
        
        coldef =  [ 
           
            ]
        
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse_with_column_list(columns_list=coldef)
        
        new_dict = table.dictionary_out()
        assert new_dict['Column_details'][6]['averaged_max_and_min'] !="False"
        assert not new_dict['Column_details'][6]['averaged_max_and_min']
        
        
    def test_col_datetime_true(self):
        
        coldef =  [ 
            {
        
        
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse_with_column_list(columns_list=coldef)
        
        new_dict = table.dictionary_out()
        assert new_dict['Column_details'][5]['averaged_max_and_min'] !="True"
        assert new_dict['Column_details'][5]['averaged_max_and_min']
        
        
    def test_col_datetime_false(self):
        
        coldef =  [ 
            
        
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse_with_column_list(columns_list=coldef)
        
        new_dict = table.dictionary_out()
        assert new_dict['Column_details'][5]['averaged_max_and_min'] !="False"
        assert not new_dict['Column_details'][5]['averaged_max_and_min']     
        
    def test_col_time_true(self):
        
        coldef =  [ 
          
        
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse_with_column_list(columns_list=coldef)
        
        new_dict = table.dictionary_out()
        assert new_dict['Column_details'][7]['averaged_max_and_min']!="True"
        assert new_dict['Column_details'][7]['averaged_max_and_min']
        
        
    def test_col_time_false(self):
        
        coldef =  [ 
     
        
        table = Table(table=self.test_table, table_name="testTable")
        table.analyse_with_column_list(columns_list=coldef)
        
        new_dict = table.dictionary_out()
        assert new_dict['Column_details'][7]['averaged_max_and_min'] !="False"
        assert not new_dict['Column_details'][7]['averaged_max_and_min']          
        
    
