import signal
import threading
import time

# Variable global para controlar la ejecución del contador
contador_activo = True
lock = threading.Lock()

def signal_handler_pause(signum, frame):
    global contador_activo
    with lock:
        contador_activo = False
        print("[INFO] Contador pausado por señal SIGUSR1.")

def signal_handler_resume(signum, frame):
    global contador_activo
    with lock:
        contador_activo = True
        print("[INFO] Contador reanudado por señal SIGUSR2.")

def contador():
    global contador_activo
    n = 30
    while n > 0:
        with lock:
            if contador_activo:
                print(f"[CONTADOR] Tiempo restante: {n} segundos")
                n -= 1
        time.sleep(1)

    print("[CONTADOR] Finalizado.")

if __name__ == "__main__":
    # Registrar señales
    signal.signal(signal.SIGUSR1, signal_handler_pause)
    signal.signal(signal.SIGUSR2, signal_handler_resume)

    # Iniciar hilo de contador
    hilo_contador = threading.Thread(target=contador)
    hilo_contador.start()

    print("[INFO] En ejecución. Enviar SIGUSR1 para pausar y SIGUSR2 para reanudar.")

    # Mantener el programa activo
    hilo_contador.join()
