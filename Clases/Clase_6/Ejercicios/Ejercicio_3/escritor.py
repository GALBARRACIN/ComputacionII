import os

fifo_path = "/tmp/fifo_archivo"

# Crear el FIFO si no existe
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print("Escribe mensajes para enviar al FIFO (escribe 'exit' para salir).")

# Ciclo para enviar líneas al FIFO
while True:
    mensaje = input("> ")  # Leer entrada del usuario
    if mensaje.lower() == "exit":
        break  # Finalizar si el usuario escribe "exit"
    
    with open(fifo_path, "w") as fifo:
        fifo.write(mensaje + "\n")  # Enviar mensaje al FIFO
