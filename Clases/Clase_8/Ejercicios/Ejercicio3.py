from multiprocessing import Process, Value, Lock

def incrementar(valor, n):
    """Incrementa el valor compartido n veces SIN usar Lock."""
    for _ in range(n):
        valor.value += 1

def incrementar_seguro(valor, n, lock):
    """Incrementa el valor compartido n veces usando Lock."""
    for _ in range(n):
        with lock:
            valor.value += 1

if __name__ == '__main__':
    N = 50_000  # Número de incrementos por proceso
    contador = Value('i', 0)  # Entero compartido
    lock = Lock()  # Lock para sincronización

    print("Ejecutando sin protección...")
    p1 = Process(target=incrementar, args=(contador, N))
    p2 = Process(target=incrementar, args=(contador, N))
    p1.start(); p2.start(); p1.join(); p2.join()
    print(f"Valor final sin Lock: {contador.value}\n")

    # Reiniciar contador
    contador.value = 0  

    print("Ejecutando con protección...")
    p1 = Process(target=incrementar_seguro, args=(contador, N, lock))
    p2 = Process(target=incrementar_seguro, args=(contador, N, lock))
    p1.start(); p2.start(); p1.join(); p2.join()
    print(f"Valor final con Lock: {contador.value}")
