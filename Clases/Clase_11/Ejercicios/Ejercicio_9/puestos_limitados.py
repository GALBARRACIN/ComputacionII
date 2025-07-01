# puestos_limitados.py

from multiprocessing import Process, Semaphore
import os
import time
import random

def usar_puesto(sem: Semaphore, proceso_id: int):
    print(f"[P{proceso_id}] PID {os.getpid()} esperando un puesto...")
    with sem:
        print(f"[P{proceso_id}] ✅ Entró a la zona crítica.")
        time.sleep(random.uniform(1, 3))  # Simula uso del recurso
        print(f"[P{proceso_id}] ❌ Saliendo de la zona crítica.")

def main():
    sem = Semaphore(3)  # Solo 3 procesos simultáneamente
    procesos = []

    for i in range(10):
        p = Process(target=usar_puesto, args=(sem, i + 1))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print("Todos los procesos terminaron.")

if __name__ == "__main__":
    main()
