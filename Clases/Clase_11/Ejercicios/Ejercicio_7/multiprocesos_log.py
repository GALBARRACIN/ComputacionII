# multiprocesos_log.py

from multiprocessing import Process, Lock
from datetime import datetime
import os
import time

LOG_PATH = "log_concurrente.txt"

def escribir_log(lock: Lock, proceso_id: int):
    for _ in range(3):  # cada proceso escribe varias veces
        with lock:
            with open(LOG_PATH, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] PID {os.getpid()} (Proceso {proceso_id}) escribiendo en el log.\n")
        time.sleep(0.5)

def main():
    lock = Lock()
    procesos = []

    # Limpiar el archivo de log
    open(LOG_PATH, 'w').close()

    for i in range(4):
        p = Process(target=escribir_log, args=(lock, i + 1))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print("Todos los procesos han escrito en el log.")

if __name__ == "__main__":
    main()
