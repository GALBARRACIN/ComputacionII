import os

fifo_path = "/tmp/fifo_temperatura"

print("Monitor de temperatura activo...")

# Abrir el FIFO en modo lectura
with open(fifo_path, "r") as fifo:
    while True:
        mensaje = fifo.readline().strip()  # Leer línea del FIFO
        if not mensaje:
            continue  # Evitar procesar líneas vacías
        
        print(f"Recibido: {mensaje}")

        # Extraer la temperatura del mensaje
        temperatura = float(mensaje.split(": ")[1].replace("°C", ""))
        if temperatura > 28:
            print(f"⚠ ALERTA: Temperatura alta ({temperatura}°C)")
