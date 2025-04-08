import os

# Crea un nuevo proceso
pid = os.fork()

if pid == 0:
    # El hijo reemplaza su código con el comando 'ls -l'
    os.execlp("ls", "ls", "-l")
else:
    # El padre espera a que el hijo termine
    os.wait()
    print("Padre: el proceso hijo finalizó.")
