import pdb
#pdb.set_trace()
import threading
import logging
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from binance_d.impl.websocketconnection import ConnectionState
from binance_d.impl.utils.timeservice import get_current_timestamp
from binance_d.example_d.user.fake_order_scripts.fake_order_module import run_fake_order 

#damian
from binance_d.requestclient import RequestClient
from binance_d.constant.test import *
from datetime import datetime

#print("websocketwatchdog line 13,pec") 
request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
#print("websocketwatchdog line 15,pec") 
listen_key = request_client.start_user_data_stream()
print("#### in immpl.websocketwatchdog scope global  listenKey: ", listen_key)


def watch_dog_job(*args):
    '''
    connection.id the order depends on websocket_module.py:
       order 1 is user  : sub_client.subscribe_user_data_event(listen_key, callback, error)
       order 2 is market: sub_client.subscribe_mark_price_event("adausd_perp", callback, error)
    '''
   
    watch_dog_instance = args[0]
    #print("in watch_dog_job watch_dog_instance.connection_list: " + str(watch_dog_instance.connection_list))
    print("WATA5 before loop watch_dog_job, watch_dog_instance.connection_list:", watch_dog_instance.connection_list)
    # Verifica si hay duplicados comparando la longitud de la lista original con la longitud de la lista única
    original_list = watch_dog_instance.connection_list
    if len(original_list) != len(set(original_list)):
        print("WATA5 La lista contiene elementos duplicados.")

        # Luego, puedes eliminar duplicados
        unique_list = list(set(original_list))
        watch_dog_instance.connection_list = unique_list  
        print("WATA5 lista luego de remover elementos duplicados:", watch_dog_instance.connection_list)
    for connection in watch_dog_instance.connection_list:
        print("WATA6 watch_dog_job, loop, connection:", connection)
        #print("watch_dog_job, loop, connection.state:", connection.state)
        conn_id = connection.id
        receive_time_limit_ms = watch_dog_instance.receive_limit_ms
        if connection.state == ConnectionState.CONNECTED:
            #print("watch_dog_job, loop, if, connection.state is CONNECTED")
            if watch_dog_instance.is_auto_connect:
                ts = get_current_timestamp() - connection.last_receive_time
                tseconds = round(ts/1000) # tseconds se resetea cuando llega un event por websocket
                curr_timestamp = round(time.time())
                '''
                connection.id the order depends on websocket_module.py:
                order 1 is user  : sub_client.subscribe_user_data_event(listen_key, callback, error)
                order 2 is market: sub_client.subscribe_mark_price_event("adausd_perp", callback, error)
                '''
                if connection.id == 1:
                    print("wdogj user: " + str(curr_timestamp) + ", " + str(tseconds) + ", connecton.id:" + str(connection.id))
                #if curr_timestamp % 20 == 0 or tseconds > 25:
                #if (curr_timestamp % 20 == 0 and tseconds < 20) or (tseconds >= 20 and curr_timestamp % 10 == 0) or (tseconds >= 30 and curr_timestamp % 5 == 0):
                    if (curr_timestamp % 20 == 0 and tseconds < 20): 
                        print(".... .... curr_timestamp % 20 and tseconds < 20", curr_timestamp % 20)
                        print(".... in if, curr_timestamp: " + str(curr_timestamp) + ", tseconds: " + str(tseconds) + ", call keep")
                        result = request_client.keep_user_data_stream()
                        print(".... result keep_user_data_stream: ", result)
                        print(".... call run_fake_order")
                        run_fake_order(request_client, tseconds) # tseconds se resetea cuando llega el event fake por websocket 
                    elif (tseconds >= 20 and tseconds < 30 and curr_timestamp % 10 == 0): 
                        print(".... .... tseconds >=20 and curr_timestamp % 10", curr_timestamp % 10)
                        print(".... in if, curr_timestamp: " + str(curr_timestamp) + ", tseconds: " + str(tseconds) + ", call keep")
                        result = request_client.keep_user_data_stream()
                        print(".... result keep_user_data_stream: ", result)
                        print(".... call run_fake_order")
                        run_fake_order(request_client, tseconds) # tseconds se resetea cuando llega el event fake por websocket 
                    elif (tseconds >= 30 and tseconds < 55 and curr_timestamp % 5 == 0): 
                        print(".... .... tseconds >= 30 and curr_timestamp % 5", curr_timestamp % 5)
                        print(".... in if, curr_timestamp: " + str(curr_timestamp) + ", tseconds: " + str(tseconds) + ", call keep")
                        result = request_client.keep_user_data_stream()
                        print(".... result keep_user_data_stream: ", result)
                        print(".... call run_fake_order")
                        run_fake_order(request_client, tseconds) # tseconds se resetea cuando llega el event fake por websocket 
                    #elif tseconds >= 55:
                    elif ( tseconds >= 55 and curr_timestamp % 5 == 0):
                        #print(".... .... .... tseconds >= 55, curr_timestamp: " + str(curr_timestamp) + ", tseconds: " + str(tseconds) + ", perhaps will die")
                        print("in if .... .... .... ( tseconds >= 55 and curr_timestamp % 5 ), curr_timestamp: " + str(curr_timestamp) + ", tseconds: " + str(tseconds) + ", perhaps will die")
                        
                        #print(".... in if, curr_timestamp: " + str(curr_timestamp) + ", tseconds: " + str(tseconds) + ", call keep")
                        result = request_client.keep_user_data_stream()
                        print(".... result keep_user_data_stream: ", result)
                        run_fake_order(request_client, tseconds) # tseconds se resetea cuando llega el event fake por websocket 
                    '''
                    if tseconds > 25:
                        print(".... if tseconds > 25, curr_timestamp now:", curr_timestamp) 
                        result = request_client.keep_user_data_stream()
                        print(".... if tseconds > 25 keep_user_data_stream: ", result)
                        #run_fake_order(request_client, tseconds) # tseconds se resetea cuando llega el event fake por websocket 
                    else:
                        print(".... multiplo 20: ", curr_timestamp)
                        result = request_client.keep_user_data_stream()
                        print(".... keep_user_data_stream: ", result)
                        if tseconds >= 20:
                            print(".... multiplo 20, tseconds >= 20, call run_fake_order")
                            run_fake_order(request_client, tseconds) # tseconds se resetea cuando llega el event fake por websocket 
                        # no llamar a run_fake_order si tseconds es menor a 20, ya que significa que hubo otro evento y reseteo
                        # tseconds
                        else: 
                            print(".... multiplo 20, tseconds < 20, not call run_fake_order")
                    ''' 
                elif connection.id == 2:
                    print("wdogj market: " + str(curr_timestamp) + ", " + str(tseconds) + ", connecton.id:" + str(connection.id))
                #if ts > 55:
                #    print("OLOL damian 55 s reached for connection.id {" + str(connection.id) + "}")
                #    print("OLOL damian [Sub][" + str(connection.id) + "] No response from server")
                #    watch_dog_instance.logger.warning("[Sub][" + str(connection.id) + "] No response from server")
                #    connection.re_connect_in_delay(watch_dog_instance.connection_delay_failure)
                 
                if ts > watch_dog_instance.receive_limit_ms:
                    print("OLOL damian, conn_id: " + str(conn_id) + ", reached limit message1, Receive time limit:" + str(watch_dog_instance.receive_limit_ms) + " ms) reached for connection.id {" + str(connection.id) + "}")
                    print("OLOL damian, conn_id: " + str(conn_id) + ", reached limit message2, [Sub][" + str(connection.id) + "] No response from server")
                   
                    # comentado porque la watch_dog_instance.connection_delay_failure parece que solo cierra
                    # la conexion pero no hace el reconnect

                    #watch_dog_instance.logger.warning("[Sub][" + str(connection.id) + "] No response from server")
                    #connection.re_connect_in_delay(watch_dog_instance.connection_delay_failure)
        elif connection.in_delay_connection():
            print("OLOL damian , conn_id: " + str(conn_id) + ", connection.in_delay_connection is True, no hago nada")
            #print("OLOL damian , conn_id: " + str(conn_id) + ", connection.in_delay_connection is True, [Sub] call re_connect")
            #watch_dog_instance.logger.warning("[Sub] call re_connect, conn_id:" + str(conn_id))
            #connection.re_connect()
            pass
        elif connection.state == ConnectionState.CLOSED_ON_ERROR:
            print("watch_dog_job, loop, if, connection.state is CLOSED_ON_ERROR, conn_id: " + str(conn_id))
            print("OLOL damian connection.state == ConnectionState.CLOSED_ON_ERROR conn_id: " + str(conn_id))
            if watch_dog_instance.is_auto_connect:
#                print(".... OLOL damian, conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance.is_auto_connect, is enabled, attempting reconnection.")
                print(".... OLOL damian, conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance.is_auto_connect, current time:", round(time.time()))
                print(".... OLOL damian, conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance.is_auto_connect, last receive time:", connection.last_receive_time)

                # Calculate the time since the last receive
                ts = get_current_timestamp() - connection.last_receive_time
                tseconds = round(ts / 1000)
                print(".... OLOL damian, conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance.is_auto_connect, time since last receive (seconds):", tseconds)
                print(".... .... OLOL damian, conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance.is_auto_connect,  watch_dog_instance.receive_limit_ms:", watch_dog_instance.receive_limit_ms, "ms.")
                ## debug if tseconds >= watch_dog_instance.receive_limit_ms:
                if tseconds >= 5:
                    print(".... .... OLOL damian, tseconds:", tseconds, ", conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance.is_auto_connect, tseconds >= watch_dog_instance.receive_limit_ms, receive time limit exceeded:", watch_dog_instance.receive_limit_ms, "ms.")
                    print(".... .... OLOL damian, tseconds:", tseconds, ", conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance.is_auto_connect, tseconds >= watch_dog_instance.receive_limit_ms, attempting reconnection.")
            
                    # Attempt the reconnection
                    #connection.re_connect_in_delay(watch_dog_instance.connection_delay_failure)
                    if (tseconds % 5 == 0): 
                        print("<<<< OLOL call connect_damian, tseconds:", tseconds)
                        connection.connect_damian(tseconds)
            
                    print(".... .... OLOL damian, tseconds:", tseconds, ", conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance.is_auto_connect, tseconds >= watch_dog_instance.receive_limit_ms, reconnection attempt completed.")
                else:
                    #print(".... .... OLOL damian, tseconds:", tseconds, ", conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance.is_auto_connect, receive time limit not exceeded, receive_limit_ms: ", receive_time_limit_ms, " not attempting reconnection.")
                    pass
            else:
                print("OLOL damian, conn_id: " + str(conn_id) + ", connection.state == ConnectionState.CLOSED_ON_ERROR, watch_dog_instance is_auto_connect is disabled, not attempting reconnection.")
                
        '''
        elif connection.state == ConnectionState.CLOSED_ON_ERROR:
            print("watch_dog_job, loop, if, connection.state is CLOSED_ON_ERROR")
            print("OLOL damian connection.state == ConnectionState.CLOSED_ON_ERROR")
            if watch_dog_instance.is_auto_connect:
                print("OLOL damian , watch_dog_instance.is_auto_connect, call connection.re_connect_in_delay")
                connection.re_connect_in_delay(watch_dog_instance.connection_delay_failure)
                pass
            else:
                print("OLOL damian , watch_dog_instance is not is_auto_connect")
                pass
        '''

class WebSocketWatchDog(threading.Thread):
    print("in impl.websocketwatchdog.WebSocketWatchDog en scope global")
    mutex = threading.Lock()
    connection_list = list()

    def __init__(self, is_auto_connect=True, receive_limit_ms=60000, connection_delay_failure=15):
        print("in impl.websocketwatchdog.WebSocketWatchDog en __init__, receive_limit_ms:", receive_limit_ms)
        threading.Thread.__init__(self)
        self.is_auto_connect = is_auto_connect
        print("in impl.websocketwatchdog.WebSocketWatchDog __init__, is_auto_connect:", is_auto_connect)
        # aca controlo el close del websocket si supera el threshold receive_limit_ms 
        #self.receive_limit_ms = 86400000 # 24 hours
        self.receive_limit_ms = receive_limit_ms

        self.connection_delay_failure = connection_delay_failure
        self.logger = logging.getLogger("binance-client")
        self.scheduler = BlockingScheduler()
        self.scheduler.add_job(watch_dog_job, "interval", max_instances=10, seconds=1, args=[self])
        #print("in binance_d.impl.websocketwatchdog.WebSocketWatchDog.__init__ self.scheduler.print_jobs():", self.scheduler.print_jobs())
        self.scheduler.print_jobs() # only prints in the console
        self.start()

    def run(self):
        self.scheduler.start()

    def on_connection_created(self, connection):
        print("OLOL websocketwatchdog on_connection_created, solo aparece cuando se inicia el websocket")
        self.mutex.acquire()
        self.connection_list.append(connection)
        self.mutex.release()

    def on_connection_closed(self, connection):
        print("OLOL websocketwatchdog on_connection_closed")
        self.mutex.acquire()
        self.connection_list.remove(connection)
        self.mutex.release()
