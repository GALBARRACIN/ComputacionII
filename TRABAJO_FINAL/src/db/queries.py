# src/db/queries.py

import pprint
from src.db.mongo_setup import get_database

# ==============================================================================
# Módulo: Consultas Avanzadas y Medición de Desempeño
# Materia: Diseño de Bases de Datos II
# Objetivo: Demostrar el uso del Aggregation Framework y analizar el 
# rendimiento del índice geoespacial mediante explain("executionStats").
# ==============================================================================

def analisis_bateria_estado(coleccion):
    """
    Uso del Aggregation Framework.
    Objetivo: Agrupar los drones por su estado (ej. active vs low_battery) 
    y calcular el promedio de batería en cada grupo.
    """
    print("\n[DB II] Ejecutando Pipeline de Agregación (Estado y Batería)...")
    
    pipeline = [
        # 1. $match: Filtramos solo los registros que tengan un 'drone_id' válido.
        # Es equivalente al WHERE en SQL.
        {"$match": {"drone_id": {"$exists": True}}},
        
        # 2. $group: Agrupamos los documentos.
        # _id: El campo por el cual agrupamos (en este caso, el 'status' del dron).
        # bateria_promedio: Calculamos el promedio ($avg) del campo 'battery_pct'.
        # total_reportes: Contamos ($sum: 1) cuántos documentos entraron en este grupo.
        {"$group": {
            "_id": "$status",
            "bateria_promedio": {"$avg": "$battery_pct"},
            "total_reportes": {"$sum": 1}
        }},
        
        # 3. $project: Moldeamos la salida final. 
        # Decidimos qué campos mostrar y podemos redondear valores.
        # Aquí redondeamos el promedio a 2 decimales.
        {"$project": {
            "estado": "$_id",
            "bateria_promedio": {"$round": ["$bateria_promedio", 2]},
            "total_reportes": 1,
            "_id": 0 # Ocultamos el _id original para que la salida sea más limpia
        }}
    ]
    
    # Ejecutamos el pipeline
    resultados = list(coleccion.aggregate(pipeline))
    pprint.pprint(resultados)


def rastreo_proximidad_explain(coleccion):
    """
    Prueba de Rendimiento del Índice 2dsphere.
    Objetivo: Buscar drones cerca de una coordenada usando $near y extraer 
    las estadísticas de ejecución (executionStats) para el examen final.
    """
    print("\n[DB II] Analizando desempeño de consulta Geoespacial con explain()...")
    
    # Coordenadas de ejemplo (Centro de operaciones teórico)
    lon_objetivo = -68.8272
    lat_objetivo = -32.8908
    
    # Consulta geoespacial usando el operador $near.
    # $maxDistance está en metros (1000m = 1km a la redonda).
    query = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon_objetivo, lat_objetivo]
                },
                "$maxDistance": 1000
            }
        }
    }
    
    # CRÍTICO PARA EL EXAMEN: En lugar de usar .find(), usamos .find().explain()
    # Le pedimos específicamente las 'executionStats' al motor de MongoDB.
    explicacion = coleccion.find(query).explain()
    
    # Extraemos solo las métricas que le importan a los profesores
    stats = explicacion.get("executionStats", {})
    total_docs_examinados = stats.get("totalDocsExamined")
    total_keys_examinadas = stats.get("totalKeysExamined") # Keys = Entradas en el índice
    tiempo_ejecucion_ms = stats.get("executionTimeMillis")
    
    print("-" * 50)
    print("MÉTRICAS DE RENDIMIENTO (executionStats):")
    print(f"- Tiempo de ejecución: {tiempo_ejecucion_ms} ms")
    print(f"- Documentos devueltos/examinados: {stats.get('nReturned')} / {total_docs_examinados}")
    print(f"- Entradas de índice escaneadas: {total_keys_examinadas}")
    print("-" * 50)
    
    # Defensa oral: Si 'totalKeysExamined' es similar a 'nReturned', y NO se
    # escaneó toda la colección (COLLSCAN), significa que tu índice 2dsphere
    # está funcionando a la perfección.

def main():
    db = get_database()
    coleccion = db['telemetria']
    
    # Verificamos si hay datos antes de consultar
    if coleccion.count_documents({}) == 0:
        print("[AVISO] La colección está vacía. Encendé un dron primero para generar datos.")
        return
        
    analisis_bateria_estado(coleccion)
    rastreo_proximidad_explain(coleccion)

if __name__ == '__main__':
    main()