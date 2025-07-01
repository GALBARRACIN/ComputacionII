import multiprocessing
import time
import math
import os

def cpu_bound_task(n):
    """Simula una tarea intensiva en CPU: calcular el n-ésimo número primo."""
    print(f"🔧 Proceso {os.getpid()} calculando el primo #{n}")
    count = 0
    candidate = 2
    while True:
        for i in range(2, int(math.sqrt(candidate)) + 1):
            if candidate % i == 0:
                break
        else:
            count += 1
            if count == n:
                print(f"✅ Proceso {os.getpid()} completó: primo #{n} = {candidate}")
                return candidate
        candidate += 1

if __name__ == "__main__":
    start = time.time()

    # Lista de tareas: calcular los primos en esas posiciones
    tasks = [5000, 6000, 7000, 8000]

    # Crear pool de procesos
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(cpu_bound_task, tasks)

    print("\n📊 Resultados:")
    for pos, prime in zip(tasks, results):
        print(f"- Primo #{pos}: {prime}")

    print(f"\n⏱️ Tiempo total: {time.time() - start:.2f} segundos")
