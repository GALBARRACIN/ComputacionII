from multiprocessing import Process, Queue
import time  # Se usa para simular tiempos de procesamiento

def productor(q):
    """Función que simula un proceso productor, enviando mensajes a la Queue."""
    mensajes = ["Mensaje 1", "Mensaje 2", "Mensaje 3", "Mensaje 4", "Mensaje 5"]

    for msg in mensajes:
        print(f"[Productor] Enviando: {msg}")  # Muestra el mensaje que se está enviando
        q.put(msg)  # Agrega el mensaje a la Queue
        time.sleep(0.5)  # Simula una pequeña espera antes de enviar el siguiente mensaje

    q.put(None)  # Envía una señal de terminación para indicar que no hay más mensajes

def consumidor(q):
    """Función que simula un proceso consumidor, recibiendo mensajes desde la Queue."""
    while True:
        mensaje = q.get()  # Extrae un mensaje de la Queue

        if mensaje is None:  # Si el mensaje es None, significa que no hay más datos
            break  # Se termina el ciclo y el proceso consumidor finaliza

        print(f"[Consumidor] Recibido: {mensaje}")  # Muestra el mensaje recibido
        time.sleep(1)  # Simula procesamiento más lento en el consumidor

if __name__ == "__main__":
    # Crear la Queue compartida entre los procesos
    queue = Queue()

    # Crear los procesos para productor y consumidor
    productor_proceso = Process(target=productor, args=(queue,))
    consumidor_proceso = Process(target=consumidor, args=(queue,))

    # Iniciar los procesos
    productor_proceso.start()
    consumidor_proceso.start()

    # Esperar a que ambos procesos terminen
    productor_proceso.join()
    consumidor_proceso.join()

    print("Comunicación entre procesos finalizada.")  # Mensaje final cuando todo ha terminado
