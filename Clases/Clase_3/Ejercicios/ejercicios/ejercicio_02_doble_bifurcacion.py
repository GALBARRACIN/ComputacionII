import os

def ejecutar():
    # Crear dos procesos hijos independientes
    for i in range(2):
        pid = os.fork()
        if pid == 0:
            # Cada hijo imprime su PID y el de su padre
            print(f"[HIJO {i}] PID: {os.getpid()}  Padre: {os.getppid()}")
            os._exit(0)  # Finaliza el hijo

    # El padre espera a ambos hijos
    for _ in range(2):
        os.wait()
