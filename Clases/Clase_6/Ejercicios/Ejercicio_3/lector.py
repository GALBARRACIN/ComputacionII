import os

fifo_path = "/tmp/fifo_archivo"
output_file = "output.txt"

print("Esperando datos en el FIFO...")

# Abrir el FIFO en modo lectura y guardar datos en un archivo
with open(fifo_path, "r") as fifo, open(output_file, "a") as archivo:
    while True:
        mensaje = fifo.readline().strip()  # Leer línea del FIFO
        if not mensaje:
            break  # Salir si no hay más datos
        
        archivo.write(mensaje + "\n")  # Guardar en el archivo
        print(f"Mensaje guardado: {mensaje}")
