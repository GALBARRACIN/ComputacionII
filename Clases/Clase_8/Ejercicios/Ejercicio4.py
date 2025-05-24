import time
import threading
import multiprocessing

def fibonacci(n):
    """Calcula el n-ésimo número de Fibonacci recursivamente."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def ejecutar_fibonacci(n, num_hilos):
    """Ejecuta la función en múltiples hilos para medir el impacto del GIL."""
    threads = []
    for _ in range(num_hilos):
        t = threading.Thread(target=fibonacci, args=(n,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

def ejecutar_fibonacci_procesos(n, num_procesos):
    """Ejecuta la función en múltiples procesos evitando el GIL."""
    procesos = []
    for _ in range(num_procesos):
        p = multiprocessing.Process(target=fibonacci, args=(n,))
        procesos.append(p)
        p.start()
    
    for p in procesos:
        p.join()

if __name__ == "__main__":
    n = 35
    num_workers = 4

    print("Ejecutando con hilos...")
    inicio = time.perf_counter()
    ejecutar_fibonacci(n, num_workers)
    fin = time.perf_counter()
    print(f"Tiempo con hilos: {fin - inicio:.2f} segundos\n")

    print("Ejecutando con procesos...")
    inicio = time.perf_counter()
    ejecutar_fibonacci_procesos(n, num_workers)
    fin = time.perf_counter()
    print(f"Tiempo con procesos: {fin - inicio:.2f} segundos")
