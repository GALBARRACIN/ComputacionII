import os

def ejecutar():
    # Crear un proceso hijo
    pid = os.fork()
    if pid == 0:
        # Código del hijo
        print("[HIJO] PID:", os.getpid(), "PPID:", os.getppid())
    else:
        # Código del padre
        print("[PADRE] PID:", os.getpid(), "Hijo:", pid)
