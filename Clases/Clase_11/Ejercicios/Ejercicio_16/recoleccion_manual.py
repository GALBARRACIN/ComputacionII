# recoleccion_manual.py

import os
import time
import random

def hijo(dormir):
    print(f"[HIJO PID {os.getpid()}] Durmiendo {dormir} segundos.")
    time.sleep(dormir)
    print(f"[HIJO PID {os.getpid()}] Terminando.")
    os._exit(0)

def main():
    pids = []
    duraciones = [random.uniform(1, 5) for _ in range(3)]

    for dur in duraciones:
        pid = os.fork()
        if pid == 0:
            hijo(dur)
        else:
            pids.append(pid)

    print(f"[PADRE PID {os.getpid()}] Hijos creados: {pids}")

    terminados = []
    while pids:
        pid, status = os.waitpid(-1, 0)  # Espera a cualquier hijo
        print(f"[PADRE] Proceso {pid} terminó con status {status}")
        terminados.append(pid)
        pids.remove(pid)

    print(f"[PADRE] Orden de terminación: {terminados}")

if __name__ == "__main__":
    main()
