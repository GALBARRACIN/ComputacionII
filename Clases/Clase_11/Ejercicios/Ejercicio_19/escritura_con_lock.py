# escritura_con_lock.py

from multiprocessing import Process, Lock
import os
import time

LOG_FILE = "log_concurrente_con_lock.txt"

def escribir(lock, id_proceso):
    for i in range(5):
        with lock:
            with open(LOG_FILE, "a") as f:
                f.write(f"[Proceso {id_proceso} PID {os.getpid()}] Línea {i+1}\n")
        time.sleep(0.1)

def main():
    lock = Lock()
    procesos = []
    # Limpiar archivo
    open(LOG_FILE, "w").close()

    for i in range(4):
        p = Process(target=escribir, args=(lock, i+1))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print("Finalizó escritura con Lock.")

if __name__ == "__main__":
    main()
