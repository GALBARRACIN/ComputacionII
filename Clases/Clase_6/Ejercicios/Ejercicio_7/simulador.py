import os
import time
import random

fifo_path = "/tmp/fifo_temperatura"

# Crear el FIFO si no existe
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print("Simulador de temperatura activo...")

# Generar y enviar temperaturas al FIFO
while True:
    temperatura = round(random.uniform(20, 30), 2)  # Generar temperatura aleatoria
    timestamp = time.strftime("%H:%M:%S")  # Obtener la hora actual
    mensaje = f"{timestamp} - Temperatura: {temperatura}°C"

    with open(fifo_path, "w") as fifo:
        fifo.write(mensaje + "\n")
    
    print(f"Enviado: {mensaje}")
    time.sleep(1)  # Esperar 1 segundo antes de enviar la siguiente lectura
