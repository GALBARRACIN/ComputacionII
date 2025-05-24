from multiprocessing import Process, Lock
import math
import time

def es_primo(n):
    """Verifica si n es primo."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def buscar_primos(inicio, fin, lock):
    """Busca números primos en el rango [inicio, fin] y los escribe en primos.txt"""
    primos = [n for n in range(inicio, fin) if es_primo(n)]
    
    with lock:
        with open("primos.txt", "a") as f:
            for primo in primos:
                f.write(f"{primo}\n")

if __name__ == "__main__":
    MAX = 50000  # Máximo número a buscar
    N = 8  # Número de procesos
    lock = Lock()

    # Dividir el rango en fragmentos
    fragmentos = [(i * (MAX // N), (i + 1) * (MAX // N)) for i in range(N)]

    # Medir el tiempo de ejecución
    inicio_tiempo = time.time()

    # Crear procesos
    procesos = [Process(target=buscar_primos, args=(inicio, fin, lock)) for inicio, fin in fragmentos]

    # Iniciar procesos
    for p in procesos:
        p.start()

    # Esperar finalización
    for p in procesos:
        p.join()

    duracion = time.time() - inicio_tiempo
    print(f"Tiempo de ejecución: {duracion:.2f} segundos")
