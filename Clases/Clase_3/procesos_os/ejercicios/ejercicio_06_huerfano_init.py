import os
import time

def ejecutar():
    # Crear un hijo
    pid = os.fork()
    if pid > 0:
        print("[PADRE] Terminando")  # El padre termina inmediatamente
        os._exit(0)
    else:
        # El hijo sigue ejecutándose y se vuelve huérfano
        print("[HIJO] Ahora soy huérfano. Mi nuevo padre será init/systemd")
        time.sleep(10)  # Permite tiempo para observarlo con herramientas del sistema
