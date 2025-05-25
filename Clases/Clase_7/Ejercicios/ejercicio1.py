import signal
import sys
import time
import atexit

# Función de limpieza que se ejecuta al finalizar el proceso
def cleanup():
    print("\n[INFO] Limpiando recursos antes de salir...")

# Función manejadora de señales
def handle_sigterm(signum, frame):
    print("\n[INFO] Señal SIGTERM recibida. Finalizando proceso de manera controlada.")
    sys.exit(0)  # Termina el programa de forma segura

# Registrar la función de limpieza para ejecutarse al salir
atexit.register(cleanup)

# Configurar el manejador de señal para SIGTERM
signal.signal(signal.SIGTERM, handle_sigterm)

print("[INFO] Proceso en ejecución. PID:", sys.pid if hasattr(sys, 'pid') else "No disponible")
print("[INFO] Esperando SIGTERM para finalizar...")

# Mantener el proceso activo indefinidamente
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[INFO] SIGINT detectado (Ctrl+C). Saliendo...")
