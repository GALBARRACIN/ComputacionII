# escritura_sin_lock.py

from multiprocessing import Process
import os
import time

LOG_FILE = "log_concurrente_sin_lock.txt"

def escribir(id_proceso):
    for i in range(5):
        with open(LOG_FILE, "a") as f:
            f.write(f"[Proceso {id_proceso} PID {os.getpid()}] Línea {i+1}\n")
        time.sleep(0.1)

def main():
    procesos = []
    # Limpiar archivo
    open(LOG_FILE, "w").close()

    for i in range(4):
        p = Process(target=escribir, args=(i+1,))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print("Finalizó escritura sin Lock.")

if __name__ == "__main__":
    main()
