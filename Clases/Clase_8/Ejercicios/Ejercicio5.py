from multiprocessing import Process, Pipe
import random
import time

def productor(conn):
    """Genera 10 números aleatorios y los envía al padre."""
    for _ in range(10):
        num = random.randint(1, 100)
        conn.send(num)
        time.sleep(0.1)  # Simula generación de datos
    conn.send(None)  # Señal de fin
    conn.close()

def consumidor(conn):
    """Recibe números y calcula su cuadrado."""
    while True:
        num = conn.recv()
        if num is None:
            break
        print(f"Consumidor: {num}² = {num**2}")
    conn.close()

if __name__ == "__main__":
    p_in, c_in = Pipe()   # Pipe de productor → padre
    p_out, c_out = Pipe() # Pipe de padre → consumidor

    prod = Process(target=productor, args=(p_in,))
    cons = Process(target=consumidor, args=(c_out,))
    
    prod.start()
    cons.start()

    # Padre actúa como intermediario
    while True:
        num = c_in.recv()
        if num is None:
            p_out.send(None)  # Propagar señal de cierre
            break
        p_out.send(num)  # Reenvío de datos

    # Esperar la finalización de procesos
    prod.join()
    cons.join()
