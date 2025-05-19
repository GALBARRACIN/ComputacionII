import os

fifo_path = "/tmp/fifo_multi"

print("Lector esperando datos en el FIFO...")

# Abrir el FIFO en modo lectura
with open(fifo_path, "r") as fifo:
    while True:
        mensaje = fifo.readline().strip()  # Leer línea del FIFO
        if not mensaje:
            continue  # Evitar procesamiento de líneas vacías
        
        print(f"Mensaje recibido: {mensaje}")
