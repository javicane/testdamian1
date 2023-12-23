import sys
import time

sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')

from django import forms
from binance_d.example_d.user.helpers_scripts.sql import exec_sql

def list_engines():
    try:
        sql = "select name, name from engines;"
        result_list_of_tuples = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error sql engines")
        if result_list_of_tuples:
            ee = str(time.time())
            result_list_of_tuples.append(('dunamically_assigned', 'dynamically_assigned'))
            result_list_of_tuples.append(('dummy_engine', 'dummy_engine'))
            result_list_of_tuples.append((ee, ee))
            return result_list_of_tuples
    except:
        print("except in sql")


class ChooseMaskingEngineForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_choices'] = forms.ChoiceField(label="choose a masking engine", required=False, choices=list_engines())
        self.fields['name_specific'] = forms.CharField(label="or enter a specific one", max_length=50, initial="NONE", widget=forms.HiddenInput(attrs={'size': '50'}))