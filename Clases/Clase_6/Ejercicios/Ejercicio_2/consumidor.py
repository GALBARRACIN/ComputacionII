import os
import time

fifo_path = "/tmp/fifo_buffer"

# Abrir el FIFO en modo lectura
with open(fifo_path, "r") as fifo:
    prev_num = None  # Variable para detectar números faltantes
    while True:
        linea = fifo.readline().strip()  # Leer línea del FIFO
        if not linea:
            break  # Salir si no hay más datos
        
        num = int(linea)
        timestamp = time.strftime("%H:%M:%S")
        print(f"Recibido: {num} a las {timestamp}")

        # Detectar si falta un número en la secuencia
        if prev_num is not None and num != prev_num + 1:
            print(f"⚠ ADVERTENCIA: Falta el número {prev_num + 1}")

        prev_num = num  # Actualizar el último número leído
