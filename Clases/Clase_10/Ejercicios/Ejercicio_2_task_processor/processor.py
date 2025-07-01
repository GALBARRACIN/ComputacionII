import threading
import queue
import time
import random

NUM_WORKERS = 3
NUM_TASKS = 15
STOP_SIGNAL = "---FIN---"

def task_worker(task_queue, result_queue, worker_id):
    """ Toma tareas de la cola y pone el resultado procesado en result_queue. """
    while True:
        task = task_queue.get()
        if task is None:
            print(f"🛑 Worker-{worker_id}: terminó.")
            task_queue.task_done()
            break
        print(f"🔧 Worker-{worker_id} procesando: {task}")
        time.sleep(random.uniform(0.5, 1.5))  # Simula trabajo
        result = f"Tarea {task} procesada por Worker-{worker_id}"
        result_queue.put(result)
        task_queue.task_done()

def result_logger(result_queue):
    """ Recoge y muestra los resultados procesados. """
    while True:
        result = result_queue.get()
        if result == STOP_SIGNAL:
            print("📄 Logger: terminando.")
            result_queue.task_done()
            break
        print(f"📥 Logger: {result}")
        result_queue.task_done()

if __name__ == "__main__":
    task_queue = queue.Queue()
    result_queue = queue.Queue()

    # Iniciar hilos trabajadores
    for i in range(NUM_WORKERS):
        threading.Thread(
            target=task_worker,
            args=(task_queue, result_queue, i),
            daemon=True
        ).start()

    # Iniciar hilo registrador
    threading.Thread(
        target=result_logger,
        args=(result_queue,),
        daemon=True
    ).start()

    # Insertar tareas
    for i in range(1, NUM_TASKS + 1):
        task_queue.put(f"Tarea-{i}")
    print(f"📝 Añadidas {NUM_TASKS} tareas.")

    # Señal de cierre para cada worker
    for _ in range(NUM_WORKERS):
        task_queue.put(None)

    # Esperar a que todas las tareas sean procesadas
    task_queue.join()

    # Señal de cierre para el logger
    result_queue.put(STOP_SIGNAL)
    result_queue.join()

    print("✅ Procesamiento completo.")
