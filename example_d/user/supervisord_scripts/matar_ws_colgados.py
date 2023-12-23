import subprocess
import psutil

def kill_process(pid):
    try:
        # Ejecuta el comando 'kill -9' para terminar el proceso con el PID especificado
        subprocess.run(["kill", "-9", str(pid)])
        print(f"Proceso con PID {pid} ha sido terminado exitosamente.")
    except subprocess.CalledProcessError:
        print(f"No se pudo terminar el proceso con PID {pid}.")

def find_processes_with_parent_init(process_name):
    try:
        # Obtén los procesos que coinciden con el nombre especificado
        process_list_cmd = f"ps -ef | grep '{process_name}'|grep -v grep"
        process_list = subprocess.check_output(process_list_cmd, shell=True, universal_newlines=True).splitlines()
        #print("process_list:", process_list)
        for process_info in process_list:

            
            # Divide la línea de información del proceso en columnas
            
            columns = process_info.split()
            if len(columns) >= 2:
                pid = columns[1]
                # Encuentra el proceso padre del proceso actual
                parent_pid_cmd = f"ps -o ppid -p {pid} | grep -v PPID"
                parent_pid = subprocess.check_output(parent_pid_cmd, shell=True, universal_newlines=True).strip()
                if parent_pid == "17":
                    print(f"Proceso {pid} tiene padre '/init': {process_info}")
                    print("kill -9", pid)
                    #input("enter to kill")
                    kill_process(pid)
    except subprocess.CalledProcessError:
        pass

# Llama a la función para encontrar procesos con el nombre especificado y padre '/init'
find_processes_with_parent_init("python3 websocket_module.py")
