# pipe_padre_hijo.py

import os

def main():
    # Crear el pipe: r (lectura), w (escritura)
    r, w = os.pipe()

    pid = os.fork()

    if pid == 0:
        # Proceso hijo: escritor
        os.close(r)  # Cerramos el descriptor de lectura
        mensaje = "Hola padre, soy tu hijo.\n"
        os.write(w, mensaje.encode('utf-8'))  # Escribimos en binario
        os.close(w)  # Cerramos el descriptor de escritura
        os._exit(0)

    else:
        # Proceso padre: lector
        os.close(w)  # Cerramos el descriptor de escritura
        mensaje = os.read(r, 1024)  # Leemos del pipe
        print(f"[PADRE] Mensaje recibido del hijo: {mensaje.decode('utf-8')}")
        os.close(r)
        os.waitpid(pid, 0)

if __name__ == "__main__":
    main()
