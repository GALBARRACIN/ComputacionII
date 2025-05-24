import os
import time

# Simula atención de cliente
def atender_cliente(n):
    pid = os.fork()
    if pid == 0:
        print(f"[HIJO {n}] Atendiendo cliente")
        time.sleep(2)  # Simula tiempo de atención
        print(f"[HIJO {n}] Finalizado")
        os._exit(0)

def ejecutar():
    # Crear 5 procesos hijos, uno por cliente
    for cliente in range(5):
        atender_cliente(cliente)

    # Esperar a que todos los hijos terminen
    for _ in range(5):
        os.wait()
