import os

def ejecutar():
    # Crear 3 procesos hijos en paralelo
    for _ in range(3):
        pid = os.fork()
        if pid == 0:
            print(f"[HIJO] PID: {os.getpid()}  Padre: {os.getppid()}")
            os._exit(0)

    # Esperar a que todos los hijos terminen
    for _ in range(3):
        os.wait()
