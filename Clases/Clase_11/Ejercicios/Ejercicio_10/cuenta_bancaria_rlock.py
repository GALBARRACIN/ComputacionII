# cuenta_bancaria_rlock.py

from multiprocessing import Process, RLock, Value
import time
import os
import random

class CuentaBancaria:
    def __init__(self, saldo_inicial, lock):
        self.saldo = Value('i', saldo_inicial)
        self.lock = lock

    def depositar(self, cantidad):
        with self.lock:
            saldo_anterior = self.saldo.value
            time.sleep(0.01)  # Simula operación costosa
            self.saldo.value += cantidad
            print(f"[{os.getpid()}] Depósito: {cantidad} | Saldo: {saldo_anterior} → {self.saldo.value}")

    def retirar(self, cantidad):
        with self.lock:
            if self.saldo.value >= cantidad:
                saldo_anterior = self.saldo.value
                time.sleep(0.01)
                self.saldo.value -= cantidad
                print(f"[{os.getpid()}] Retiro: {cantidad} | Saldo: {saldo_anterior} → {self.saldo.value}")
            else:
                print(f"[{os.getpid()}] Retiro fallido: saldo insuficiente ({self.saldo.value})")

    def transferir_a_si_misma(self, cantidad):
        with self.lock:
            print(f"[{os.getpid()}] Transferencia interna de {cantidad}")
            self.retirar(cantidad)
            self.depositar(cantidad)

def operar(cuenta: CuentaBancaria):
    for _ in range(5):
        operacion = random.choice(['depositar', 'retirar', 'transferir'])
        cantidad = random.randint(10, 50)
        if operacion == 'depositar':
            cuenta.depositar(cantidad)
        elif operacion == 'retirar':
            cuenta.retirar(cantidad)
        else:
            cuenta.transferir_a_si_misma(cantidad)
        time.sleep(0.1)

def main():
    lock = RLock()
    cuenta = CuentaBancaria(saldo_inicial=100, lock=lock)

    procesos = []
    for _ in range(4):
        p = Process(target=operar, args=(cuenta,))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print(f"Saldo final: {cuenta.saldo.value}")

if __name__ == "__main__":
    main()
