from multiprocessing import Process, Value, Lock
import time

def cronometro_worker(valor_compartido, lock):
    """Cada segundo actualiza el tiempo compartido."""
    for _ in range(5):
        time.sleep(1)
        with lock:
            valor_compartido.value = time.time()

def monitor(valor_compartido, lock):
    """Verifica inconsistencias temporales cada 0.5 segundos."""
    tiempo_anterior = 0.0
    for _ in range(10):  # Monitorea durante 5 segundos
        time.sleep(0.5)
        with lock:
            tiempo_actual = valor_compartido.value
        
        if tiempo_anterior != 0.0 and abs(tiempo_actual - tiempo_anterior) > 1:
            print(f"⚠️ Inconsistencia detectada: Salto de {tiempo_actual - tiempo_anterior:.2f} segundos")
        
        tiempo_anterior = tiempo_actual

if __name__ == "__main__":
    valor_compartido = Value('d', 0.0)  # Valor compartido en memoria
    lock = Lock()  # Lock para acceso seguro
    
    # Crear trabajadores que actualizan el tiempo
    procesos_worker = [Process(target=cronometro_worker, args=(valor_compartido, lock)) for _ in range(3)]
    
    # Crear proceso de monitoreo
    monitor_proceso = Process(target=monitor, args=(valor_compartido, lock))

    # Iniciar procesos
    for p in procesos_worker:
        p.start()
    monitor_proceso.start()

    # Esperar finalización
    for p in procesos_worker:
        p.join()
    monitor_proceso.join()

    print("Finalización completa.")
