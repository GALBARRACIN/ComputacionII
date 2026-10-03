# src/tasks/worker.py

import json
from celery import Celery
from src.db.mongo_setup import get_database

# ==============================================================================
# Módulo: Cola de Tareas Distribuidas (Celery + Redis)
# Materias: Computación II (Concurrencia) y Diseño de Bases de Datos II
# Objetivo: Desacoplar la recepción de red de la escritura en base de datos.
# Los workers consumen de Redis en paralelo y guardan en MongoDB.
# ==============================================================================

# 1. CONFIGURACIÓN DEL BROKER (Computación II)
# Instanciamos la aplicación Celery. 
# El 'broker' es la URL de nuestro contenedor Redis. Redis actúa como un 
# intermediario ultra-rápido: el servidor TCP deja el mensaje JSON en Redis, 
# y los workers de Celery lo toman de ahí apenas tienen tiempo libre.
app = Celery(
    'c2_workers',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# 2. CONEXIÓN A LA BASE DE DATOS (Diseño de BD II)
# Inicializamos la conexión a Mongo una sola vez cuando arranca el worker.
db = get_database()
coleccion = db['telemetria']

# 3. DEFINICIÓN DE LA TAREA DISTRIBUIDA
# El decorador @app.task le dice a Celery que esta función puede ser enviada 
# a la cola de Redis y ejecutada en segundo plano por cualquier worker disponible.
@app.task
def procesar_telemetria(payload_json):
    """
    Recibe el JSON crudo del dron, lo parsea y lo inyecta en MongoDB.
    """
    try:
        # Convertimos el string JSON que llegó por la red a un diccionario de Python
        documento = json.loads(payload_json)
        
        # INSERTAMOS EN MONGODB: Al guardar el documento, MongoDB aplica 
        # automáticamente el índice '2dsphere' sobre el campo 'location' 
        # que definimos en el paso anterior.
        resultado = coleccion.insert_one(documento)
        
        # Retornamos el ID para dejar registro en los logs del worker
        return f"Éxito: ID Mongo {resultado.inserted_id} | Dron: {documento.get('drone_id')}"
        
    except json.JSONDecodeError:
        return "Error crítico: El payload recibido no es un JSON válido."
    except Exception as e:
        # Capturamos cualquier error de base de datos para que el worker no muera
        return f"Error en BD: {str(e)}"