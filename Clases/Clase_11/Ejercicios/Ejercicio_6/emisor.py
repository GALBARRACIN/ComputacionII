# emisor.py

import time

fifo_path = "/tmp/mi_fifo"

with open(fifo_path, 'w') as fifo:
    for i in range(5):
        mensaje = f"Mensaje {i + 1}\n"
        print(f"[EMISOR] Enviando: {mensaje.strip()}")
        fifo.write(mensaje)
        fifo.flush()
        time.sleep(1)
