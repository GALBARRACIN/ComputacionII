import os

# Crea un nuevo proceso (hijo)
pid = os.fork()

if pid == 0:
    # Este bloque lo ejecuta el proceso hijo
    print("Hijo: PID =", os.getpid())
else:
    # Este bloque lo ejecuta el proceso padre
    print("Padre: PID del hijo =", pid)
