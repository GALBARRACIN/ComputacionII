import os
import time

# Función para crear un hijo y esperar que termine
def crear_hijo(nombre):
    pid = os.fork()
    if pid == 0:
        print(f"[HIJO {nombre}] PID: {os.getpid()}")
        time.sleep(1)  # Simula trabajo
        os._exit(0)
    else:
        os.wait()  # Espera al hijo

def ejecutar():
    # Crear hijo A, luego hijo B
    crear_hijo("A")
    crear_hijo("B")
