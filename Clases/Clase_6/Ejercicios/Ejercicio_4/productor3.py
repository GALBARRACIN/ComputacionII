import os
import time

fifo_path = "/tmp/fifo_multi"

# Crear el FIFO si no existe
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print("Productor 3 enviando datos al FIFO...")

# Bucle infinito para escribir en el FIFO periódicamente
while True:
    with open(fifo_path, "w") as fifo:
        fifo.write("Soy productor 3\n")  # Mensaje único de este productor
        fifo.flush()  # Asegurar que los datos se envían de inmediato
        print("Mensaje enviado por productor 3")
    time.sleep(2)  # Espera de 2 segundos entre envíos
