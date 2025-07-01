# jerarquia_procesos.py

import os
import time

def main():
    print(f"[PADRE] PID: {os.getpid()}")
    
    hijos = []

    for i in range(2):
        pid = os.fork()
        if pid == 0:
            print(f"[HIJO {i+1}] PID: {os.getpid()} - PPID: {os.getppid()}")
            time.sleep(10)  # Deja tiempo para inspección con pstree o ps
            os._exit(0)
        else:
            hijos.append(pid)

    # Padre espera a los hijos
    for pid in hijos:
        os.waitpid(pid, 0)

    print("[PADRE] Todos los hijos han terminado.")

if __name__ == "__main__":
    main()
