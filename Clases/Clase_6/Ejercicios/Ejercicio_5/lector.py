import os
import time
import errno

fifo_path = "/tmp/fifo_condicional"

# Crear el FIFO si no existe
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print("Intentando abrir el FIFO sin bloqueo...")

# Intentar abrir el FIFO sin bloquear
intentos = 5  # Número de intentos antes de salir
for intento in range(intentos):
    try:
        fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)  # Apertura sin bloqueo
        print("FIFO abierto correctamente, leyendo datos...")
        
        with os.fdopen(fd, "r") as fifo:
            mensaje = fifo.read().strip()
            if mensaje:
                print(f"Mensaje recibido: {mensaje}")
            else:
                print("FIFO abierto, pero sin datos disponibles.")
        
        break  # Salimos del bucle si la apertura fue exitosa

    except OSError as e:
        if e.errno == errno.ENXIO:  # Error cuando no hay escritores disponibles
            print(f"Intento {intento + 1}/{intentos}: No hay escritores. Reintentando...")
            time.sleep(1)  # Esperar antes de reintentar
        else:
            raise  # Otro tipo de error inesperado

else:
    print("No se pudo abrir el FIFO después de varios intentos. Saliendo.")
