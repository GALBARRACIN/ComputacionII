from multiprocessing import Process, Value, Lock
import random
import time

def cajero(balance, lock):
    """Simula operaciones bancarias con estrategia de back-off cuando el Lock está ocupado."""
    for _ in range(20):  # Número de transacciones por proceso
        monto = random.uniform(-200, 200)  # Depósitos/retiros aleatorios
        intento = 0

        while intento < 5:  # Intentar hasta 5 veces
            time.sleep(0.1 * (2 ** intento))  # Back-off exponencial
            with lock:
                if balance.value + monto >= 0:  # Verifica que el retiro sea posible
                    balance.value += monto
                    print(f"PID {Process().pid}: {'Depósito' if monto > 0 else 'Retiro'} de {monto:.2f}. Nuevo balance: {balance.value:.2f}")
                    break  # Sale del ciclo si la operación fue exitosa
            intento += 1

if __name__ == "__main__":
    balance = Value('d', 1000.0)  # Balance inicial compartido
    lock = Lock()
    num_cajeros = 4  # Número de procesos cajeros

    procesos = [Process(target=cajero, args=(balance, lock)) for _ in range(num_cajeros)]

    for p in procesos:
        p.start()

    for p in procesos:
        p.join()

    print(f"\nBalance final después de las transacciones: {balance.value:.2f}")
