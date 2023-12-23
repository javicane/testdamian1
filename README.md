

##### 
viejo repo https://github.com/Binance-docs/Binance_Futures_python ( contiene el codigo con watchdog )
Notice of Change
This repository is no longer recommended for use in production. Instead, please use this one: https://github.com/binance/binance-futures-connector-python. This code will be removed in the future.
This repository will be set to offline on 2023-06-08.

# este es el nuevo repo para binance futures SDK python (no tiene codigo de watchdog , asi que sigo usando el viejo codigo )


# test-repo

https://www.sachinsf.com/how-to-push-the-code-from-vs-code-to-github/#:~:text=To%20push%20the%20code%20to,push%20your%20folder%20to%20Github.

tuve que hacer esto , no estoy seguro si antes de empezar con el seteo del "source control" ( el icono de 3 circulos de vscode abajo de la lupa):

git config --global user.email "damianbogan@gmail.com"
git config --global user.name "damian"

y leugo de tener todo el codigo pusheado a github hice esto (git config --list muestra los seteos):
git config core.filemode true


{

profiler

https://coderzcolumn.com/tutorials/python/line-profiler-line-by-line-profiling-of-python-code:w


root@DESKTOP-2UIJB1T:/tmp# pip install line_profiler
Collecting line_profiler
  Downloading line_profiler-3.5.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (71 kB)
     |████████████████████████████████| 71 kB 3.1 MB/s
Installing collected packages: line-profiler
Successfully installed line-profiler-3.5.1
root@DESKTOP-2UIJB1T:/tmp#

en el python hacer:
from line_profiler import LineProfiler
lprofiler = LineProfiler()


y luego abajo :
lprofiler.add_function(get_position_size)
lprofiler.add_function(get_open_orders_dict) <------aca vamos agregando las funciones que queremos profilear
lp_wrapper = lprofiler(funcion_principal)  <----aca ejecutamos la funcion principal( no debe tener parametros)
lp_wrapper()
lprofiler.print_stats()

genera una tabla con cada funcion profileada:


Total time: 1.20591 s
File: ./dangling_module_tunned.py
Function: get_open_orders_dict at line 47

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    47                                           def get_open_orders_dict():
    48                                               '''
    49                                               returns:
    50                                                   my_list: list, list of dicts
    51                                               '''
	.
	.
	.
Total time: 2.43312 s
File: ./dangling_module_tunned.py
Function: check_dangling_before_starting_websocket at line 64

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    64                                           def check_dangling_before_starting_websocket():
    65                                               #input("in " + funcname() + ", pec")
    66                                           
    67         1    1205927.0 1205927.0     49.6      open_orders_list = get_open_orders_dict()
    68                                            	
}
++++


memcached

dos cosas, uno instalar en wsl el server, y luego instalar el cliente python.
wsl:
sudo apt update
sudo apt upgrade
sudo apt install memcached

python:
damian@DESKTOP-2UIJB1T:~/.local/lib/python3.8/site-packages/binance_d/example_d/user$ pip install python-memcached
Collecting python-memcached
  Using cached python_memcached-1.59-py2.py3-none-any.whl (16 kB)
Requirement already satisfied: six>=1.4.0 in /usr/lib/python3/dist-packages (from python-memcached) (1.14.0)
Installing collected packages: python-memcached
Successfully installed python-memcached-1.59

ahora para usarlo hay que inicializarlo, como es un wsl los "service" no funcan como en un ubuntu real, por lo tanto
este comando que me permite ver si anda en un linux real, en wsl no anda:
Verifica el estado del servidor Memcached:
Puedes verificar si el servicio Memcached está en ejecución ejecutando:


sudo service memcached status

entonces lo que hago para inicializarlo es en una terminal de wsl hago esto:
damian@DESKTOP-2UIJB1T:/mnt/c/WINDOWS/system32$ memcached

esto no devuelve el prompt nunca, asi que habria que inicializarlo con el supervisord 



+++
codigo ejemplo m1.py
damian@DESKTOP-2UIJB1T:~/.local/lib/python3.8/site-packages/binance_d/example_d/user$ cat m1.py
import time
import memcache

# Crear una conexión al servidor Memcached (asegúrate de que Memcached esté en ejecución)
memcached_conn = memcache.Client(['localhost:11211'], debug=0)

def set_markprice(value):
    memcached_conn.set('markprice', str(value))

def get_markprice():
    markprice = memcached_conn.get('markprice')
    return float(markprice) if markprice is not None else None

if __name__ == "__main__":
    # Ejemplo de uso
    set_markprice(100.0)
    print("Mark Price:", get_markprice())
    time.sleep(5)
    set_markprice(150.0)
    print("Mark Price:", get_markprice())
####

supervisord

root@DESKTOP-2UIJB1T:/etc/supervisor/conf.d# cat supervisord.conf
[unix_http_server]
file=/tmp/supervisor.sock   ; the path to the socket file
;chmod=0700                 ; socket file mode (default 0700)
;chown=nobody:nogroup       ; socket file uid:gid owner
;username=user              ; default is no username (open server)
;password=123               ; default is no password (open server)


[inet_http_server]         ; inet (TCP) server disabled by default
;port=127.0.0.1:9001        ; ip_address:port specifier, *:port for all iface

port=127.0.0.1:9999        ; ip_address:port specifier, *:port for all iface
;port=127.0.0.1:9001        ; damian , lo cambie porque jupyter notebook usa este puerto
; este el proceso de jupyter  damian@DESKTOP-2UIJB1T:~/.local/lib/python3.8/site-packages/binance_d/example_d/user$ ps -ef|grep -i 9001
;damian    6373 30005  0 20:36 pts/1    00:00:01 /bin/python3 -m ipykernel_launcher --ip=127.0.0.1 --stdin=9003 --control=9001 --hb=9000 --Session.signature_scheme="hmac-sha256" --Session.key=b"4be02312-e1ec-4eba-923a-2db7cb6f854a" --shell=9002 --transport="tcp" --iopub=9004 --f=/home/damian/.local/share/jupyter/runtime/kernel-30005UxJxxZtl48Mi.json

;username=user              ; default is no username (open server)
;password=123               ; default is no password (open server)

[supervisord]
logfile=/tmp/supervisord.log ; main log file; default $CWD/supervisord.log
logfile_maxbytes=50MB        ; max main logfile bytes b4 rotation; default 50MB
logfile_backups=10           ; # of main logfile backups; 0 means none, default 10
loglevel=info                ; log level; default info; others: debug,warn,trace
pidfile=/tmp/supervisord.pid ; supervisord pidfile; default supervisord.pid
nodaemon=false               ; start in foreground if true; default false
minfds=1024                  ; min. avail startup file descriptors; default 1024
minprocs=200                 ; min. avail process descriptors;default 200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface


[supervisorctl]
serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket


[program:check_dangling]
;command=bash -c /home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/check_dangling.sh
command = python3 /home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/check_dangling_wrapper.py
user = damian
autostart = false
startsecs = 0
autorestart = false
stderr_logfile= /tmp/supervisord_check_dangling.err.log
stdout_logfile= /tmp/supervisord_check_dangling.out.log
environment=PYTHONUNBUFFERED=1

[program:websocket_user]
command = python3 /home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/websocket_module.py
user = damian
autostart = false
startsecs = 0
autorestart = false
stderr_logfile= /tmp/supervisord_websocket_user.err.log
stdout_logfile= /tmp/supervisord_websocket_user.out.log
environment=PYTHONUNBUFFERED=1

[program:check_ws]
command = python3 -u /home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/check_websocket_log_wrapper.py
user = damian
autostart = false
startsecs = 0
autorestart = false
stderr_logfile= /tmp/supervisord_check_ws.err.log
stdout_logfile= /tmp/supervisord_check_ws.out.log
environment=PYTHONUNBUFFERED=1

[program:query_tracker_pnl]
command=bash -c /home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/query_tracker_pnl.sh
user = damian
autostart = false
startsecs = 0
autorestart = false
stderr_logfile= /tmp/supervisord_query_tracker_pnl.err.log
stdout_logfile= /tmp/supervisord_query_tracker_pnl.out.log

[program:memcached_start]
command=bash -c memcached
user = damian
autostart = false
startsecs = 0
autorestart = false
stderr_logfile= /tmp/supervisord_memcached.err.log
stdout_logfile= /tmp/supervisord_memcached.out.log

[program:react_django]
;command = python3 /home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/wrapper_django.py
command = bash -c "sudo -u damian python3 /home/damian/.local/lib/python3.8/site-packages/binance_d/example_d/user/wrapper_django.py"
user = damian
autostart = false
startsecs = 0
autorestart = false
stderr_logfile= /tmp/supervisord_react_django.err.log
stdout_logfile= /tmp/supervisord_react_django.out.log
environment=PYTHONUNBUFFERED=1