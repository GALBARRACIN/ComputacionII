import os
import time

# Crea un hijo
pid = os.fork()

if pid == 0:
    # El hijo termina inmediatamente
    print("Hijo: terminando...")
    exit(0)
else:
    # El padre no hace wait inmediatamente, creando un zombi temporal
    print("Padre: no hace wait, creando zombi...")
    time.sleep(10)  # Durante este tiempo, el hijo está en estado zombi
    os.wait()  # Finalmente recoge el estado del hijo
