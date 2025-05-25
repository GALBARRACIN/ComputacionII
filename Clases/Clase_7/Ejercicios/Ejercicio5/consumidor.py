import os
import signal
import time

# Registrar PID en archivo temporal
pid = os.getpid()
with open("consumidor_pid.txt", "w") as f:
    f.write(str(pid))

print(f"[CONSUMIDOR] PID registrado: {pid}")

def procesar_trabajo(signum, frame):
    with open("trabajos.txt", "r") as f:
        trabajos = f.readlines()

    if trabajos:
        trabajo = trabajos.pop(0)
        print(f"[CONSUMIDOR] Procesando trabajo: {trabajo.strip()}")

        with open("trabajos.txt", "w") as f:
            f.writelines(trabajos)  # Mantener los trabajos no procesados

if __name__ == "__main__":
    signal.signal(signal.SIGUSR1, procesar_trabajo)

    print("[CONSUMIDOR] Esperando trabajos...")

    while True:
        time.sleep(1)  # Mantener proceso activo
