import os

def ejecutar():
    # Crear un proceso hijo
    pid = os.fork()
    if pid == 0:
        # El hijo reemplaza su código con el comando 'ls -l'
        os.execlp("ls", "ls", "-l")
    else:
        # El padre espera a que el hijo termine
        os.wait()
