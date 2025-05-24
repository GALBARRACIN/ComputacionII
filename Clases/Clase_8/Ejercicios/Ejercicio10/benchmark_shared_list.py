from multiprocessing import Process, Manager
import time

def test_shared_list(shared_list):
    """Envía un millón de enteros a través de Manager().list() y mide el tiempo."""
    inicio = time.time()
    shared_list[:] = list(range(1_000_000))  # Operación en memoria compartida
    fin = time.time()
    return fin - inicio

if __name__ == "__main__":
    with Manager() as manager:
        shared_list = manager.list()
        p = Process(target=test_shared_list, args=(shared_list,))
        p.start()
        p.join()
        print(f"Tiempo Manager().list: {test_shared_list(shared_list):.2f} segundos")
