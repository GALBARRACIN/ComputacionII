# zombi.py

import os
import time

def main():
    pid = os.fork()

    if pid == 0:
        # Proceso hijo
        print(f"[HIJO] PID: {os.getpid()} - Finalizando inmediatamente.")
        os._exit(0)

    else:
        # Proceso padre
        print(f"[PADRE] PID: {os.getpid()} - Hijo creado con PID {pid}")
        print("[PADRE] Durmiendo 10 segundos sin esperar al hijo...")
        time.sleep(10)

        print("[PADRE] Recolectando estado del hijo con waitpid.")
        os.waitpid(pid, 0)
        print("[PADRE] Estado del hijo recolectado. Fin.")

if __name__ == "__main__":
    main()
