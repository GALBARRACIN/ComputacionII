Explicación del funcionamiento
✅ Uso de multiprocessing.Queue

Se crea una instancia de Queue para compartir información entre los procesos.

El productor agrega datos a la cola usando q.put().

El consumidor recibe datos con q.get().

✅ Manejo de múltiples procesos

Se crean dos procesos independientes (Process): uno productor y otro consumidor.

Se utilizan .start() para iniciarlos y .join() para esperar a que finalicen.

✅ Sincronización y flujo de datos

La ejecución del consumidor depende de los datos del productor.

Se usa None como marcador de finalización para evitar que el consumidor espere indefinidamente.

✅ Simulación de tiempos de procesamiento

Se usa time.sleep() para reflejar una producción más rápida y un consumo más lento, demostrando posibles diferencias en velocidad entre procesos.