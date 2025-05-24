from multiprocessing import Process, Queue
import time

def test_queue(queue):
    """Envía un millón de enteros a través de Queue() y mide el tiempo."""
    inicio = time.time()
    for i in range(1_000_000):
        queue.put(i)
    for _ in range(1_000_000):
        queue.get()
    fin = time.time()
    return fin - inicio

if __name__ == "__main__":
    queue = Queue()
    p = Process(target=test_queue, args=(queue,))
    p.start()
    p.join()
    print(f"Tiempo Queue: {test_queue(queue):.2f} segundos")
