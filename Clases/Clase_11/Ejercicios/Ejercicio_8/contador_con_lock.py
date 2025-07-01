# contador_con_lock.py

from multiprocessing import Process, Value, Lock
import time

def incrementar(contador, lock):
    for _ in range(100000):
        with lock:
            contador.value += 1

def main():
    contador = Value('i', 0)
    lock = Lock()

    p1 = Process(target=incrementar, args=(contador, lock))
    p2 = Process(target=incrementar, args=(contador, lock))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(f"Valor final del contador (con Lock): {contador.value}")

if __name__ == "__main__":
    main()

# Resultado esperado:
# Siempre da 200000, gracias a la exclusión mutua.