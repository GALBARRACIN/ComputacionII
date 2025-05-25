import signal
import time

# Manejador temporal que ignora SIGINT
def ignore_sigint(signum, frame):
    print("[INFO] SIGINT (Ctrl+C) recibido, pero ignorado temporalmente...")

# Restaurar comportamiento por defecto después de 5 segundos
def restore_sigint():
    signal.signal(signal.SIGINT, signal.default_int_handler)
    print("[INFO] SIGINT restaurado. Ahora puede interrumpir el programa con Ctrl+C.")

if __name__ == "__main__":
    print("[INFO] Ignorando SIGINT por 5 segundos...")
    
    # Configurar SIGINT para ser ignorado
    signal.signal(signal.SIGINT, ignore_sigint)
    
    # Esperar 5 segundos antes de restaurar el comportamiento por defecto
    for i in range(5, 0, -1):
        print(f"[INFO] Tiempo restante: {i} segundos")
        time.sleep(1)
    
    restore_sigint()

    print("[INFO] SIGINT restaurado. Presiona Ctrl+C para salir.")
    
    # Mantener el programa activo indefinidamente
    while True:
        time.sleep(1)
