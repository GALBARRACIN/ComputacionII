# huerfano.py

import os
import time

def main():
    pid = os.fork()

    if pid == 0:
        # Proceso hijo
        print(f"[HIJO] PID: {os.getpid()} - Esperando que el padre termine.")
        time.sleep(15)  # Tiempo suficiente para que el padre haya finalizado
        ppid = os.getppid()
        print(f"[HIJO] Nuevo PPID (debería ser 1 o systemd): {ppid}")
        print("[HIJO] Finalizando.")
    else:
        # Proceso padre
        print(f"[PADRE] PID: {os.getpid()} - Hijo creado con PID {pid}")
        print("[PADRE] Finalizando inmediatamente para dejar huérfano al hijo.")
        os._exit(0)

if __name__ == "__main__":
    main()
