# exec_reemplazo.py

import os
import time

def main():
    pid = os.fork()

    if pid == 0:
        # Proceso hijo
        print(f"[HIJO] PID: {os.getpid()} - Reemplazando con 'ls -l'")
        os.execlp("ls", "ls", "-l")  # Reemplaza el proceso con 'ls -l'
        # No se ejecuta si exec fue exitoso
        print("[HIJO] Esto no debería imprimirse si exec funciona correctamente.")
    else:
        # Proceso padre
        print(f"[PADRE] PID: {os.getpid()} - Hijo creado con PID {pid}")
        os.waitpid(pid, 0)
        print("[PADRE] Hijo finalizado.")

if __name__ == "__main__":
    main()
