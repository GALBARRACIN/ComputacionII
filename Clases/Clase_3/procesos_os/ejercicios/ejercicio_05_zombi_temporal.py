import os
import time

def ejecutar():
    # Crear un hijo que termine enseguida
    pid = os.fork()
    if pid == 0:
        print("[HIJO] Finalizando")
        os._exit(0)
    else:
        # El padre no llama a wait() inmediatamente
        print("[PADRE] No llamaré a wait() aún. Observa el zombi con 'ps -el'")
        time.sleep(15)  # Durante este tiempo el hijo es zombi
        os.wait()  # Finalmente recoge al hijo
