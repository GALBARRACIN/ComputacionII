from multiprocessing import Process, Queue

def worker(k, q):
    """Cada proceso calcula la suma de los primeros k enteros y lo envía a la cola."""
    q.put(sum(range(k)))

if __name__ == '__main__':
    k = 1_000_000  # Cantidad de números a sumar
    q = Queue()  # Cola de comunicación

    # Crear 4 procesos
    procesos = [Process(target=worker, args=(k, q)) for _ in range(4)]

    # Iniciar los procesos
    for p in procesos:
        p.start()

    # Recoger resultados
    resultados = [q.get() for _ in procesos]

    # Esperar a que terminen
    for p in procesos:
        p.join()

    # Verificar que todos los procesos devolvieron el mismo resultado
    assert len(set(resultados)) == 1, "Los resultados deberían ser idénticos"
    print(f'Todos iguales: {resultados[0]}')
