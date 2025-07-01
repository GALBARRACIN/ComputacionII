# pipe_lsof.py

import os
import time

def main():
    r, w = os.pipe()

    pid = os.fork()

    if pid == 0:
        # Hijo: cerrar lectura y escribir
        os.close(r)
        mensaje = "Hola desde el hijo.\n"
        os.write(w, mensaje.encode())
        os.close(w)
        os._exit(0)
    else:
        # Padre: cerrar escritura y leer
        os.close(w)
        data = os.read(r, 1024)
        print(f"[PADRE] Recibido: {data.decode()}")
        os.close(r)
        os.waitpid(pid, 0)
        time.sleep(10)  # Mantener proceso vivo para inspección

if __name__ == "__main__":
    main()
