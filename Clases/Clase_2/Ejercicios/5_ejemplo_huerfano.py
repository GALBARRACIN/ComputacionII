import os
import time

# Crea un hijo
pid = os.fork()

if pid > 0:
    # El padre termina antes que el hijo
    print("Padre: terminando.")
    exit(0)
else:
    # El hijo sigue vivo y se convierte en huérfano
    time.sleep(5)
    print("Hijo: soy huérfano. Nuevo padre:", os.getppid())  # Debería mostrar 1 (init o systemd)
