# src/db/mongo_setup.py

import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# ==============================================================================
# Módulo: Configuración de Base de Datos y Mapeo GIS
# Materia: Diseño de Bases de Datos II
# Objetivo: Establecer la conexión con el contenedor MongoDB y configurar 
# la colección con índices geoespaciales para el esquema denormalizado.
# ==============================================================================

# Constantes de conexión (apuntando al localhost donde Docker expone el puerto 27017)
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "c2_tactico_db"
COLLECTION_NAME = "telemetria"

def get_database():
    """
    Establece la conexión con el servidor MongoDB usando el driver oficial (pymongo).
    """
    try:
        # El serverSelectionTimeoutMS en 2000ms evita que el programa se quede colgado
        # infinitamente si olvidaste levantar el contenedor de Docker.
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        
        # Forzamos un ping a la base de datos para verificar que realmente responde
        client.admin.command('ping')
        print("[DB INFO] Conexión exitosa a MongoDB.")
        
        return client[DB_NAME]
    
    except ConnectionFailure:
        print("[DB ERROR] No se pudo conectar a MongoDB.")
        print("¿Ejecutaste 'docker-compose up -d' en tu terminal?")
        sys.exit(1)

def initialize_database():
    """
    Inicializa la estructura documental. 
    Justificación para el examen: En MongoDB no creamos tablas fijas, pero SÍ 
    es una excelente práctica pre-configurar los índices de nuestras colecciones 
    antes de inyectar datos de forma masiva.
    """
    db = get_database()
    coleccion = db[COLLECTION_NAME]

    print(f"[DB INFO] Verificando índices en la colección '{COLLECTION_NAME}'...")

    # ==========================================================================
    # REQUISITO CRÍTICO BD II: CREACIÓN DEL ÍNDICE GEOESPACIAL (2dsphere)
    # ==========================================================================
    # Creamos un índice de tipo '2dsphere' sobre el campo anidado 'location'.
    # Este índice permite hacer consultas analíticas de proximidad sobre una esfera 
    # (la Tierra), utilizando la especificación GeoJSON que armamos en el cliente.
    # El parámetro 'background=True' permite que el índice se construya sin bloquear 
    # operaciones de lectura/escritura concurrentes en un entorno de producción.
    coleccion.create_index([("location", "2dsphere")], background=True)
    
    print("[DB SUCCESS] Índice geoespacial '2dsphere' configurado correctamente.")
    print("La base de datos está lista para recibir coordenadas del enjambre FPV.")
    
    return db, coleccion

if __name__ == '__main__':
    # Punto de entrada para probar la conexión ejecutando el script directamente
    initialize_database()