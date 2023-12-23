import pdb
#pdb.set_trace()
import sys
#sys.path.append("C:/binance/futures/futures")
#print("in dangling_module line 3")
from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from binance_d.example_d.user.helpers_scripts.helpers_module import create_dict_from_output, funcname, get_radar_list
from binance_d.example_d.user.helpers_scripts.sql import exec_sql
from difflib import SequenceMatcher
from binance_d.example_d.user.common_scripts.get_order_status_module import get_order_status

from binance_d.general_settings import adaperp_decimals



def check2new():
# Consulta SQL para obtener los datos
    query = "SELECT timestamp, rp FROM tracker_pnl ORDER BY timestamp DESC limit 200"
    rows = exec_sql(sql = query, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error  ")

# Ejecutar la consulta y obtener los resultados
    print(rows)
# Calcular la sumatoria acumulada de rp desde el registro más reciente hacia atrás
    cumulative_sum = 0
    for i in range(len(rows)):
        #print("i", i)
        cumulative_sum += rows[i][1]
        #print("cumu", cumulative_sum)
        # Comprobar si la sumatoria acumulada ha comenzado a disminuir
        if i > 0 and cumulative_sum < rows[i-1][1]:
            # Si la sumatoria ha comenzado a disminuir, devolver el timestamp anterior
            print("El primer timestamp donde hay un máximo de sumatoria de rp es:", rows[i-1][0])
            break

    max_sum = 0  # Variable para almacenar el máximo de sumatoria
    max_sum_rows = 0  # Variable para almacenar la cantidad de filas de la sumatoria máxima
    current_sum = 0  # Variable para almacenar la sumatoria acumulada actual
    current_rows = 0  # Variable para almacenar la cantidad de filas de la sumatoria actual

# Iterar sobre los registros desde el más reciente hacia atrás
    for row in rows:
        current_sum += row[1]
        current_rows += 1
        if current_sum > max_sum:
            max_sum = current_sum
            max_sum_rows = current_rows
        if current_sum < 0:
            break

# Imprimir los resultados
    print("El máximo de sumatoria es:", max_sum)
    print("La cantidad de filas acumuladas en el máximo de sumatoria es:", max_sum_rows)

    min_sum = 0  # Variable para almacenar el mínimo de sumatoria
    min_sum_rows = 0  # Variable para almacenar la cantidad de filas de la sumatoria mínima
    current_sum = 0  # Variable para almacenar la sumatoria acumulada actual
    current_rows = 0  # Variable para almacenar la cantidad de filas de la sumatoria actual
    
    # Iterar sobre los registros desde el más reciente hacia atrás
    for row in rows:
        current_sum += row[1]
        current_rows += 1
        if current_sum < min_sum:
            min_sum = current_sum
            min_sum_rows = current_rows
        if current_sum > 0:
            break
    
    # Imprimir los resultados
    print("El mínimo de sumatoria es:", min_sum)
    print("La cantidad de filas acumuladas en el mínimo de sumatoria es:", min_sum_rows)
    
def min():
# Consulta SQL para obtener los datos
    query = "SELECT timestamp, rp FROM tracker_pnl ORDER BY timestamp DESC limit 2000"
    rows = exec_sql(sql = query, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error  ")
    min_sum = 0  # Variable para almacenar el mínimo de sumatoria
    min_sum_rows = 0  # Variable para almacenar la cantidad de filas de la sumatoria mínima
    current_sum = 0  # Variable para almacenar la sumatoria acumulada actual
    current_rows = 0  # Variable para almacenar la cantidad de filas de la sumatoria actual
    
    min_sums = []  # Lista para almacenar los mínimos encontrados
    min_sums_rows = []  # Lista para almacenar las cantidades de filas acumuladas en cada mínimo
    
    # Iterar sobre los registros desde el más reciente hacia atrás
    for row in rows:
        current_sum += row[1]
        current_rows += 1
        if current_sum < min_sum:
            min_sum = current_sum
            min_sum_rows = current_rows
        if current_sum > 0:
            min_sums.append(min_sum)
            min_sums_rows.append(min_sum_rows)
            min_sum = current_sum
            min_sum_rows = current_rows
            current_sum = 0
            current_rows = 0
    
    # Imprimir los resultados
    for i, min_sum in enumerate(min_sums):
        print("El mínimo de sumatoria", i+1, "es:", min_sum)
        print("La cantidad de filas acumuladas en el mínimo", i+1, "es:", min_sums_rows[i])

def min_neg():
# Consulta SQL para obtener los datos
    query = "SELECT timestamp, rp FROM tracker_pnl ORDER BY timestamp DESC limit 2000"
    rows = exec_sql(sql = query, sql_command = "select", return_type = "return_raw", fetch_type = "fetchall", error_message = "error  ")
    
    # Inicializar variables
    current_sum = 0.0
    current_min = float('inf')
    accumulated_rows = 0
    min_rows_accumulated = []
    
    # Recorrer las filas en orden descendente
    for i, row in enumerate(rows):
        timestamp, rp = row
    
        # Actualizar la suma acumulada
        current_sum += rp
    
        # Si la suma actual es menor que el mínimo actual y es negativa, actualizar el mínimo
        if current_sum < current_min and current_sum < 0:
            # Imprimir los datos del mínimo anterior si existen
            if current_min != float('inf'):
                print(f"Mínimo: {current_min:.2f}, filas acumuladas: {accumulated_rows}")
                min_rows_accumulated.append(accumulated_rows)
            
            # Actualizar el mínimo actual y reiniciar la cuenta de filas acumuladas
            current_min = current_sum
            accumulated_rows = 1
        else:
            # Incrementar la cuenta de filas acumuladas
            accumulated_rows += 1
    
    # Imprimir el último mínimo si es negativo
    if current_min < 0:
        print(f"Mínimo: {current_min:.2f}, filas acumuladas: {accumulated_rows}")
        min_rows_accumulated.append(accumulated_rows)
    
    # Imprimir el total de mínimos encontrados
    print(f"Total de mínimos negativos encontrados: {len(min_rows_accumulated)}")
    
    #check2new()
#    min()
min_neg()