# contador_sin_lock.py

from multiprocessing import Process, Value
import time

def incrementar(contador):
    for _ in range(100000):
        contador.value += 1  # No protegido, puede fallar

def main():
    contador = Value('i', 0)  # Entero compartido

    p1 = Process(target=incrementar, args=(contador,))
    p2 = Process(target=incrementar, args=(contador,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(f"Valor final del contador (sin Lock): {contador.value}")

if __name__ == "__main__":
    main()

# Resultado esperado:
# Debería dar 200000, pero muchas veces da menos (por colisiones concurrentes)