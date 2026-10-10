# src/ui/dashboard.py

import streamlit as st
import folium
from streamlit_folium import st_folium
import sys
import os

# ==============================================================================
# RESOLUCIÓN DE RUTAS (PYTHONPATH)
# Al ejecutar el script directamente, Python pierde el contexto del paquete 'src'.
# Calculamos la ruta absoluta al directorio padre y la inyectamos en sys.path.
# ==============================================================================
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)

from src.db.mongo_setup import get_database

# ==============================================================================
# Módulo: Interfaz Visual y Renderizado GIS (Frontend)
# Consumo de MongoDB y mapeo geoespacial en tiempo real.
# ==============================================================================

# Configura el layout de la página web para ocupar todo el ancho del monitor
st.set_page_config(page_title="Radar C2 Táctico", layout="wide")

def obtener_datos_drones():
    """
    Se conecta a la BD y extrae EXCLUSIVAMENTE la última coordenada de cada dron.
    
    Justificación técnica: Si hiciéramos un find() normal, traeríamos todo el 
    historial de vuelo, sobrecargando la memoria y dibujando mil puntos por dron.
    Usamos el Aggregation Framework para filtrar y quedarnos con el dato más fresco.
    """
    db = get_database()
    coleccion = db['telemetria']
    
    pipeline = [
        # 1. $sort: Ordenamos toda la colección por timestamp de mayor a menor.
        # Esto pone los registros más recientes al principio.
        {"$sort": {"timestamp": -1}},
        
        # 2. $group: Agrupamos por el identificador único del dron.
        {"$group": {
            "_id": "$drone_id",
            # Al usar $first, nos quedamos con el primer registro del grupo 
            # (que es el más nuevo gracias al $sort previo).
            
            # El campo 'location.coordinates' es un array GeoJSON [longitud, latitud].
            # $arrayElemAt extrae el índice 1 (Latitud) y el índice 0 (Longitud).
            "lat": {"$first": {"$arrayElemAt": ["$location.coordinates", 1]}},
            "lon": {"$first": {"$arrayElemAt": ["$location.coordinates", 0]}},
            
            "bateria": {"$first": "$battery_pct"},
            "estado": {"$first": "$status"}
        }}
    ]
    
    return list(coleccion.aggregate(pipeline))

def main():
    st.title("🛰️ Sistema C2 Táctico - Enjambre FPV")
    st.markdown("Monitoreo en tiempo real. **Base de Datos:** MongoDB | **Concurrencia:** Celery + TCP Sockets")

    # Botón que fuerza a Streamlit a reejecutar todo el script de arriba a abajo, 
    # consultando a MongoDB nuevamente.
    if st.button("🔄 Actualizar Radar"):
        st.rerun()

    datos = obtener_datos_drones()

    if not datos:
        st.warning("No hay telemetría registrada en la base de datos.")
        return

    # ======================================================================
    # RENDERIZADO DEL MAPA TÁCTICO (Folium)
    # ======================================================================
    
    # Truco para forzar el mapa oscuro (Dark Matter) esquivando el bloqueo de API Key
    url_mapa_oscuro = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    attr_mapa_oscuro = '&copy; OpenStreetMap &copy; CARTO'
    
    # Inicializamos el mapa centrado en Mendoza con el tema oscuro
    mapa_c2 = folium.Map(location=[-32.8908, -68.8272], zoom_start=14, tiles=url_mapa_oscuro, attr=attr_mapa_oscuro)

    # DIBUJAR EL ALCANCE DEL RADAR (Círculo de cobertura)
    folium.Circle(
        location=[-32.8908, -68.8272],
        radius=1000, # Alcance de 1000 metros (1 km)
        color="cyan", # Color táctico
        weight=2,
        fill=True,
        fill_opacity=0.08,
        tooltip="Área de Cobertura del C2 (1 km a la redonda)"
    ).add_to(mapa_c2)

    # Iteramos sobre los resultados agrupados de Mongo
    for dron in datos:
        # Lógica condicional: Verde neón táctico si está activo, rojo si es crítico
        color_marcador = "#39FF14" if dron['estado'] == "active" else "#FF0000"

        # Usamos RegularPolygonMarker para crear el triángulo estilo Call of Duty / UAV
        folium.RegularPolygonMarker(
            location=[dron['lat'], dron['lon']],
            number_of_sides=3, # 3 lados = Triángulo
            radius=10, # Tamaño del marcador
            color=color_marcador,
            weight=1,
            fill=True,
            fill_color=color_marcador,
            fill_opacity=0.8,
            rotation=30, # Rota el triángulo para que la punta mire hacia arriba
            popup=f"<b>{dron['_id']}</b><br>Batería: {dron['bateria']}%", # Ventana al clickear
            tooltip=f"ID: {dron['_id']} | Estado: {dron['estado'].upper()}" # Texto al posar el mouse
        ).add_to(mapa_c2)

    # Inyecta el objeto HTML/JS de Folium dentro de la app de Streamlit
    st_folium(mapa_c2, width=1200, height=600)

    # ======================================================================
    # DATAFRAME DE RESPALDO (Tabla visual)
    # ======================================================================
    st.subheader("📊 Estado General del Enjambre")
    
    # Mapeamos la salida de Mongo a un diccionario más prolijo para la tabla
    datos_tabla = [
        {
            "Dron ID": d["_id"],
            "Estado": d["estado"].upper(),
            "Batería (%)": d["bateria"],
            "Latitud": d["lat"],
            "Longitud": d["lon"]
        }
        for d in datos
    ]
    # Renderiza una tabla interactiva (permite ordenar columnas)
    st.dataframe(datos_tabla, use_container_width=True)

if __name__ == '__main__':
    main()