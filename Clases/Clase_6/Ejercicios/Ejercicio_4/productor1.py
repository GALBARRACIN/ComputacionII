import os
import time

fifo_path = "/tmp/fifo_multi"

# Crear el FIFO si no existe
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print("Productor 1 enviando datos al FIFO...")

# Ciclo de escritura periódica
while True:
    with open(fifo_path, "w") as fifo:
        fifo.write("Soy productor 1\n")
        fifo.flush()  # Forzar envío de datos
        print("Mensaje enviado por productor 1")
    time.sleep(1)  # Esperar antes de enviar otro mensaje
