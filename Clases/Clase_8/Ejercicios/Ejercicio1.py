from multiprocessing import Process, current_process

def hijo():
    """Función ejecutada por cada proceso hijo"""
    print(f"[Hijo] PID: {current_process().pid}")

if __name__ == '__main__':
    print(f"[Padre] Iniciando con PID: {current_process().pid}")
    
    # Crear dos procesos hijo
    procesos = [Process(target=hijo) for _ in range(2)]
    
    # Iniciar los procesos
    for p in procesos:
        p.start()
    
    # Esperar a que terminen
    for p in procesos:
        p.join()
    
    print("[Padre] Hijos finalizados correctamente.")
