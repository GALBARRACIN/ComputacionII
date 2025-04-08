import os
import time

# Crea un proceso hijo
pid = os.fork()

if pid == 0:
    # El hijo hace una tarea y termina
    print("Hijo: trabajando...")
    time.sleep(2)
    print("Hijo: terminado")
    exit(0)
else:
    # El padre espera al hijo con wait()
    print("Padre: esperando al hijo...")
    os.wait()
    print("Padre: el hijo terminó.")
