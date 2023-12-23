import sys
import os
import logging

#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.insert(0, ROOT_DIR + '/../..')
#sys.path.append('/home/damian/.local/lib/python3.8/site-packages/binance_d/')
sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')

#from binance_d import RequestClient
#from binance_d import SubscriptionClient
from binance_d.constant.test import *
from binance_d.model import *
from binance_d.exception.binanceapiexception import BinanceApiException

from binance_d.base.printobject import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, check_existence_radar_list_in_disc, list_pivots_in_radar_list_in_disk, funcname
from binance_d.example_d.user.process_event_scripts.process_module import process_event

from binance_d.example_d.user.common_scripts.create_orders_module import silent_limit_no_oco_sell_long
from binance_d.impl.utils.timeservice import get_current_timestamp
from binance_d.example_d.user.helpers_scripts.sql import exec_sql


def query_pivot_frequency_frontend(query_range):
    
        if query_range == 0: # for all data
            filter_range_with_gmt3_timezone_correction = "where cast(substr(timestamp, 1, 10) as integer)  < ( strftime('%s') + (3600*3)    ) "
        else:
            filter_range_with_gmt3_timezone_correction = "where cast(substr(timestamp, 1, 10) as integer)  >=  ( strftime('%s') - (" + str(query_range) + "*24*3600) )  and  cast(substr(timestamp, 1, 10) as integer)  < ( strftime('%s') + (3600*3)    ) "

        filter_order_by_limit = " order by 2 desc limit 20 "

        base = "select tpos, count(*) cc from ( "
        base += "select  "
        base += "case  "
        base += "when clientorderid like 'goto_in_position%' then replace(clientorderid,'goto_in_position','')  "
        base += "when clientorderid like 'new_pivot%' then replace(clientorderid,'new_pivot','') "
        base += "else clientorderid end timestamp, "
        base += "trigger_price_to_put_in_position tpos "
        base += " from pnl_hist where order_status='PNL' )  "
        base += filter_range_with_gmt3_timezone_correction 
        base += "group by tpos "
    
        sql = "select tpos, cc, sum_total, printf('%.5f',100*cast(cc as real)/cast(sum_total as real)) weight_percentage from (" 
        sql += "select "
        sql += "tpos, "
        sql += "cc, "
        sql += "( select sum(cc) suma from ( "
        sql += base 
        sql += ") "
        sql += " ) sum_total "
        sql += "from  "
        sql += "( "
        sql += base 
        sql += filter_order_by_limit  
        sql += ") "
        sql += ") "

        res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_pivot_frequency")
        #print("res_sql: ", res_sql)
        res_dict = [{'pivot':a[0], 'count':a[1] , 'sum_total':a[2], 'weight_percentage':a[3]} for a in res_sql] #convert list of tuples in list of dicts
        return res_dict