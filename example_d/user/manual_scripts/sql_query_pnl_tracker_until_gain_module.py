import sys
import os
import logging
import datetime
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

from binance_d.general_settings import adaperp_decimals


def find_sum_pnl_threshold():

    # Obtener registros ordenados por timestamp en orden descendente
    sql = "SELECT timestamp, rp FROM tracker_pnl ORDER BY timestamp DESC"
    res_sql = exec_sql(sql = sql, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "query_pnl_frequency")
   # cursor.execute(query)
   # rows = cursor.fetchall()
    rows = res_sql
    print(rows)
    running_sum = 0
    oldest_timestamp = None
    row_count = 0

    # Calcular la suma acumulada y encontrar el punto de corte
    for row in rows:
        running_sum += row[1]
        if running_sum >= 0:
            oldest_timestamp = row[0]
            break
        row_count += 1

    human_date= unix_timestamp_to_human_date(oldest_timestamp/1000)
    return running_sum, human_date, row_count

def unix_timestamp_to_human_date(unix_timestamp):
    # Convert Unix timestamp to a datetime object
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp)

    # Format the datetime object as a human-readable date string
    formatted_date = timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Adjust the format as needed

    return formatted_date

# Llamar a la función y obtener los resultados
sum_pnl, oldest_timestamp, row_count = find_sum_pnl_threshold()

# Mostrar los resultados
print("Suma PNL:", sum_pnl)
print("Timestamp más antiguo:", oldest_timestamp)
print("Cantidad de filas:", row_count)
