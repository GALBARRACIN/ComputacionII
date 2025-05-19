import os
import time

fifo_path = "/tmp/fifo_buffer"

# Crear el FIFO si no existe
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print("Productor enviando datos al FIFO...")

# Escribir números en el FIFO con una pausa de 0.1 segundos
with open(fifo_path, "w") as fifo:
    for i in range(1, 101):
        fifo.write(f"{i}\n")  # Escribir número en el FIFO
        fifo.flush()  # Asegurar que los datos se envían inmediatamente
        print(f"Enviado: {i}")
        time.sleep(0.1)  # Simular flujo continuo de datos
