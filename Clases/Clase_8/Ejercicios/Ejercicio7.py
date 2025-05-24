from multiprocessing import Process, Queue
import requests
import time
import random

def worker(queue, result_queue):
    """Descarga una URL, mide el tiempo y almacena el resultado."""
    while not queue.empty():
        url = queue.get()
        inicio = time.time()
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            resultado = (url, -1, f"Error: {str(e)}")  # -1 indica fallo
        else:
            duracion = time.time() - inicio
            resultado = (url, duracion, f"PID: {Process().pid}")

        result_queue.put(resultado)

if __name__ == "__main__":
    urls = [
        "https://www.example.com",
        "https://www.python.org",
        "https://www.wikipedia.org",
        "https://www.github.com",
        "https://www.stackoverflow.com"
    ]  # Lista de URLs a descargar

    num_workers = 3  # Número de procesos

    url_queue = Queue()
    result_queue = Queue()

    # Agregar URLs a la cola
    for url in urls:
        url_queue.put(url)

    # Crear procesos workers
    workers = [Process(target=worker, args=(url_queue, result_queue)) for _ in range(num_workers)]

    # Iniciar procesos
    for w in workers:
        w.start()

    # Esperar que terminen
    for w in workers:
        w.join()

    # Recoger y ordenar resultados
    resultados = []
    while not result_queue.empty():
        resultados.append(result_queue.get())

    resultados.sort(key=lambda x: x[1])  # Ordenar por tiempo de descarga

    print("\nReporte de Descargas:")
    for url, duracion, info in resultados:
        estado = "✔️ Completado" if duracion >= 0 else "❌ Falló"
        print(f"{url}: {estado} | Tiempo: {duracion:.2f} seg | {info}")
