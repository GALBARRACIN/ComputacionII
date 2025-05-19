import os
import time

fifo_path = "/tmp/fifo_multi"

# Crear el FIFO si no existe
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print("Productor 2 enviando datos al FIFO...")

# Bucle infinito para escribir en el FIFO periódicamente
while True:
    with open(fifo_path, "w") as fifo:
        fifo.write("Soy productor 2\n")  # Mensaje único de este productor
        fifo.flush()  # Asegurar que los datos se envían de inmediato
        print("Mensaje enviado por productor 2")
    time.sleep(1.5)  # Espera de 1.5 segundos entre envíos
