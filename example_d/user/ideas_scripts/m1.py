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

