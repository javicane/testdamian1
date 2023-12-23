import pdb
#pdb.set_trace()
import threading
import websocket
import gzip
import ssl
import logging
from urllib import parse
import urllib.parse

from binance_d.base.printtime import PrintDate
from binance_d.impl.utils.timeservice import get_current_timestamp
from binance_d.impl.utils.urlparamsbuilder import UrlParamsBuilder
from binance_d.impl.utils.apisignature import create_signature
from binance_d.exception.binanceapiexception import BinanceApiException
from binance_d.impl.utils import *
from binance_d.base.printobject import *
from binance_d.model.constant import *

from binance_d.example_d.user.helpers_scripts.helpers_module import funcname

# Key: ws, Value: connection
websocket_connection_handler = dict()


def on_message(ws, message):
    websocket_connection = websocket_connection_handler[ws]
    websocket_connection.on_message(message)
    return


def on_error(ws, error):
    websocket_connection = websocket_connection_handler[ws]
    websocket_connection.on_failure(error)

#def on_close(ws):
def on_close(ws, close_status_code, close_msg):
#in binance_d.impl.websocketconnection.on_error parameter error: on_close() takes 1 positional argument but 3 were given, pec
#https://github.com/Tkd-Alex/Twitch-Channel-Points-Miner-v2/pull/189
#https://pypi.org/project/websocket-client/
    websocket_connection = websocket_connection_handler[ws]
    #websocket_connection.on_close() typo ?  'WebsocketConnection' object has no attribute 'on_close'
    websocket_connection.close()  #damian


def on_open(ws):
    websocket_connection = websocket_connection_handler[ws]
    websocket_connection.on_open(ws)


connection_id = 0


class ConnectionState:
    IDLE = 0
    CONNECTED = 1
    CLOSED_ON_ERROR = 2


def websocket_func(*args):
    connection_instance = args[0]
    connection_instance.ws = websocket.WebSocketApp(connection_instance.url,
                                                    on_message=on_message,
                                                    on_error=on_error,
                                                    on_close=on_close)
    global websocket_connection_handler
    websocket_connection_handler[connection_instance.ws] = connection_instance
    connection_instance.logger.info("[Sub][" + str(connection_instance.id) + "] Connecting...")
    connection_instance.delay_in_second = -1
    connection_instance.ws.on_open = on_open
    connection_instance.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    connection_instance.logger.info("[Sub][" + str(connection_instance.id) + "] Connection event loop down")
    if connection_instance.state == ConnectionState.CONNECTED:
        connection_instance.state = ConnectionState.IDLE


class WebsocketConnection:

    def __init__(self, api_key, secret_key, uri, watch_dog, request):
        self.__thread = None
        self.url = uri
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.request = request
        self.__watch_dog = watch_dog
        self.delay_in_second = -1
        self.ws = None
        self.last_receive_time = 0
        self.logger = logging.getLogger("binance-futures")
        self.state = ConnectionState.IDLE
        global connection_id
        connection_id += 1
        self.id = connection_id

    def in_delay_connection(self):
        try:
            print("impl.websocketconnection.WebsocketConnection.in_delay_connection delay_in_second:", self.delay_in_second)
        except:
            print("impl.websocketconnection.WebsocketConnection.in_delay_connection except :", sys.exc_info())
        return self.delay_in_second != -1

    def re_connect_in_delay(self, delay_in_second):
        '''
        # caller is websocketwatchdog.watch_dog_job
        # connection.re_connect_in_delay(watch_dog_instance.connection_delay_failure) 
        '''
        print("WATA2 impl.websocketconnection.WebsocketConnection.re_connect_in_delay")
        if self.ws is not None:
            print("WATA2 impl.websocketconnection.WebsocketConnection.re_connect_in_delay self.ws is not None, self.ws:", self.ws)
            print("WATA2 impl.websocketconnection.WebsocketConnection.re_connect_in_delay call ws.close")
            self.ws.close()
            self.ws = None
        else:
            print("WATA2 impl.websocketconnection.WebsocketConnection.re_connect_in_delay self.ws is None")
        self.delay_in_second = delay_in_second
        self.logger.warning("[Sub][" + str(self.id) + "] Reconnecting after "
                            + str(self.delay_in_second) + " seconds later")
        print("WATA2 impl.websocketconnection.WebsocketConnection.re_connect_in_delay , reconnecting after " + str(self.delay_in_second) + " seconds later")

    def re_connect(self):
        print("impl.websocketconnection.WebsocketConnection.re_connect")
        if self.delay_in_second != 0:
            self.delay_in_second -= 1
            self.logger.warning("In delay connection: " + str(self.delay_in_second))
            print("impl.websocketconnection.WebsocketConnection.re_connect, in delay connection !=0 self.delay_in_second:", self.delay_in_second)
        else:
            print("impl.websocketconnection.WebsocketConnection.re_connect, in delay connection =0, call self.connect")
            self.connect()

    def connect_damian(self, tseconds_parameter):
        if self.state == ConnectionState.CONNECTED:
            self.logger.info("[Sub][" + str(self.id) + "] Already connected")
            print("WATA3 impl.websocketconnection.WebsocketConnection.connect_damian, already connected self.id:", self.id, ", tseconds_parameter:", tseconds_parameter)
        else:
            print("WATA3 impl.websocketconnection.WebsocketConnection.connect_damian, not connected, call thread.start, tseconds_paramter:", tseconds_parameter )
            print("WATA3 exists a thread running?")
            for thread in threading.enumerate():
                print("WATA3 running thread: ", thread)
                print("WATA3 running thread.current_thread: ", threading.current_thread())
            self.__thread = threading.Thread(target=websocket_func, args=[self])
            self.__thread.start()
            print("WATA3 started, tseconds_paramter:", tseconds_parameter)

    def connect(self):
        if self.state == ConnectionState.CONNECTED:
            self.logger.info("[Sub][" + str(self.id) + "] Already connected")
            print("impl.websocketconnection.WebsocketConnection.connect, already connected self.id:", self.id)
        else:
            print("impl.websocketconnection.WebsocketConnection.connect, not connected, call thread.start" )
            self.__thread = threading.Thread(target=websocket_func, args=[self])
            self.__thread.start()

    def send(self, data):
        self.ws.send(data)

    def close(self):
        print("impl.websocketconnection.WebsocketConnection.close, Closing Normally")
        self.ws.close()
        del websocket_connection_handler[self.ws]
        self.__watch_dog.on_connection_closed(self)
        self.logger.error("[Sub][" + str(self.id) + "] Closing normally")
        # damian
#        print("impl.websocketconnection.WebsocketConnection.closed normally, call self.connect()" )
 #       self.connect()
    

    def on_open(self, ws):
        self.logger.info("[Sub][" + str(self.id) + "] Connected to server")
        self.ws = ws
        self.last_receive_time = get_current_timestamp()
        self.state = ConnectionState.CONNECTED
        self.__watch_dog.on_connection_created(self)
        if self.request.subscription_handler is not None:
            self.request.subscription_handler(self)
        return

    def on_error(self, error_message):
        print("in impl.websocketconnection." + funcname() + ", error_message is: " + str(error_message))
        if self.request.error_handler is not None:
            print('error')
            exception = BinanceApiException(BinanceApiException.SUBSCRIPTION_ERROR, error_message)
            self.request.error_handler(exception)
        self.logger.error("[Sub][" + str(self.id) + "] " + str(error_message))
        print("[Sub][" + str(self.id) + "] " + str(error_message))

    def on_failure(self, error):
        print("in impl.websocketconnection." + funcname() + ", error is: " + str(error))
        self.on_error("Unexpected error: " + str(error))
        self.close_on_error()

    def on_message(self, message):
        print("in impl.websocketconnection." + funcname() + " BEGIN")
        self.last_receive_time = get_current_timestamp()
        #print('in ' + funcname() + ', Type of message is', type(message))
        if not isinstance(message, str):
            print('Decompressing...')
            message = gzip.decompress(message).decode('utf-8')
        print("in " + funcname() + ", message (raw message received by websocket client): |||| " + message + " ||||end of message")



        # message here is the raw message received by the client websocket, and json_wrapper is a new object that will contain only
        # the fields of the raw message that are modeled in impl.model.* directory, for example for event ORDER_TRADE_UPDATE, the model file 
        # is impl.model.orderupdate.py
        # after that, json_wrapper is passed to self.__on_receive_payload and 
        # self.__on_receive_payload passed the object to  weboscket_module.callback function executing this self.request.update_callback(SubscribeMessageType.PAYLOAD, res) 
        # and we can see in the screen the data received with the print statement in websocket_module.callback
        #print("in " + funcname() + "executing: json_wrapper = parse_json_from_string(message) | json_wrapper will contain only the fields modeled in impl.model.*")  
        json_wrapper = parse_json_from_string(message)
     
        #print("in impl.websocketconnection." + funcname() + ", json_wrapper: " + str(json_wrapper))
        #print("in impl.websocketconnection." + funcname() + ", ahora empiezo a scanear el objeto json el cual es el message recibido por el websocket")
        if json_wrapper.contain_key("method") and json_wrapper.get_string("method") == "PING":
            print("scan 1")
            self.__process_ping_on_new_spec(json_wrapper.get_int("E"))
        elif json_wrapper.contain_key("status") and json_wrapper.get_string("status") != "ok":
            print("scan 2")
            error_code = json_wrapper.get_string_or_default("err-code", "Unknown error")
            error_msg = json_wrapper.get_string_or_default("err-msg", "Unknown error")
            self.on_error(error_code + ": " + error_msg)
        elif json_wrapper.contain_key("err-code") and json_wrapper.get_int("err-code") != 0:
            print("scan 3")
            error_code = json_wrapper.get_string_or_default("err-code", "Unknown error")
            error_msg = json_wrapper.get_string_or_default("err-msg", "Unknown error")
            self.on_error(error_code + ": " + error_msg)
        elif json_wrapper.contain_key("result") and json_wrapper.contain_key("id"):
            print("scan 4 , esto aparece cuando se inicia la conexion de websocket")
            self.__on_receive_response(json_wrapper)
        else:
            print("scan 5")
            print("in " + funcname() + ", else, call self.__on_receive_payload(json_wrapper)")
            self.__on_receive_payload(json_wrapper)
        print("in impl.websocketconnection." + funcname() + " END")

    def __on_receive_response(self, json_wrapper):
        res = None
        try:
            res = json_wrapper.get_int("id")
        except Exception as e:
            self.on_error("Failed to parse server's response: " + str(e))

        try:
            if self.request.update_callback is not None:
                self.request.update_callback(SubscribeMessageType.RESPONSE, res)
        except Exception as e:
            self.on_error("Process error: " + str(e)
                     + " You should capture the exception in your error handler")

    def __on_receive_payload(self, json_wrapper):
        print('in impl.websocketconnection.' + funcname() + " BEGIN")
        #print('in impl.websocketconnection.' + funcname() + ", parameter json_wrapper is: " + str(json_wrapper))
        #print('in impl.websocketconnection.' + funcname() + ", parameter json_wrapper is type: " + str(type(json_wrapper)))
        res = None
        try:
            if self.request.json_parser is not None:
                res = self.request.json_parser(json_wrapper)
        except Exception as e:
            print("in impl.websocketconnection." + funcname() + ",exception in first try except, error is: " + str(e) + ", call function on_error")
            self.on_error("Failed to parse server's response: " + str(e))

        #print('in impl.websocketconnection.' + funcname() + ", res: " + str(res) )
        #print("in impl.websocketconnection." + funcname() + ",self.request.update_callback: " + str(self.request.update_callback) )
        #print("in impl.websocketconnection." + funcname() + ", self.request.update_callback is type: " + str(type(self.request.update_callback) ))
        
        try:
            if self.request.update_callback is not None:
                print('in impl.websocketconnection.' + funcname() + ", call self.request.update_callback(SubscribeMessageType.PAYLOAD, res)")
                #input("es posible parar aca ?")
                self.request.update_callback(SubscribeMessageType.PAYLOAD, res)
        except Exception as e:
            print("in impl.websocketconnection." + funcname() + ",exception in second try except, error is: " + str(e) + ", call function on_error")
            self.on_error("Process error: " + str(e)
                     + " You should capture the exception in your error handler")

        if self.request.auto_close:
            self.close()

        print('in impl.websocketconnection.' + funcname() + " END")

    def __process_ping_on_new_spec(self, ping_ts):
        """Respond on explicit ping frame
        """
        print("Responding to explicit PING...")
        respond_pong_msg = "{\"method\":\"PONG\",\"E\":" + str(ping_ts) + "}"
        self.send(respond_pong_msg)
        print(respond_pong_msg)
        return

    def __process_ping_on_trading_line(self, ping_ts):
        self.send("{\"op\":\"pong\",\"ts\":" + str(ping_ts) + "}")
        return

    def __process_ping_on_market_line(self, ping_ts):
        self.send("{\"pong\":" + str(ping_ts) + "}")
        return

    
    def close_on_error(self):
        if self.ws is not None:
            self.ws.close()
            self.state = ConnectionState.CLOSED_ON_ERROR
            self.logger.error("[Sub][" + str(self.id) + "] Connection is closing due to error")
            print("damian in impl.websocketconnction.WebsocketConnection.close_on_error, [Sub][" + str(self.id) + "] Connection is closing due to error")
            print("damian in impl.websocketconnection.WebsocketConnection.close_on_error, we have to launch websocket_module.py again")
            
            # damian
            for thread in threading.enumerate():
                print("WATA in close_on_error thread: ", thread)
                print("WATA in close_on_error thread.current_thread: ", threading.current_thread())
                #if thread != threading.current_thread():
                #    thread._stop()

            #queda ejecutando con el sys.exit y sin thread._stop()
            print("WATA sys.exit(1)")
            sys.exit(1)

            #sin el sys.exit y sin thread._stop() se hace un close normally y finaliza su ejecucion( el log
            # no se mueve mas ):
               #impl.websocketconnection.WebsocketConnection.close, Closing Normally
               #OLOL websocketwatchdog on_connection_closed
            

            #print("damian in impl.websocketconnection.WebsocketConnection.close_on_error, try self.connect()")
            #self.connect()


