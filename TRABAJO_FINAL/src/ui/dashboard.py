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
    historial de vuelo, sobrecargando la memoria. Usamos el Aggregation Framework 
    para filtrar y quedarnos solo con la posición más reciente.
    """
    db = get_database()
    coleccion = db['telemetria']
    
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$drone_id",
            "lat": {"$first": {"$arrayElemAt": ["$location.coordinates", 1]}},
            "lon": {"$first": {"$arrayElemAt": ["$location.coordinates", 0]}},
            "bateria": {"$first": "$battery_pct"},
            "estado": {"$first": "$status"}
        }}
    ]
    return list(coleccion.aggregate(pipeline))

def limpiar_base_datos():
    """
    Función auxiliar para borrar los datos residuales de pruebas anteriores.
    Permite arrancar la demostración del examen en limpio.
    """
    db = get_database()
    db['telemetria'].delete_many({})

def main():
    # ======================================================================
    # ENCABEZADO CENTRADO (Estética de la UI)
    # ======================================================================
    st.markdown("<h1 style='text-align: center;'>🛰️ Sistema C2 Táctico - Enjambre FPV</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Monitoreo en tiempo real. <b>Base de Datos:</b> MongoDB | <b>Concurrencia:</b> Celery + TCP Sockets</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Contenedor de columnas para centrar los botones
    col_espacio1, col_btn1, col_btn2, col_espacio2 = st.columns([3, 2, 2, 3])
    
    with col_btn1:
        if st.button("🔄 Actualizar Radar", use_container_width=True):
            st.rerun()
            
    with col_btn2:
        if st.button("🗑️ Limpiar Historial", use_container_width=True):
            limpiar_base_datos()
            st.rerun()

    datos = obtener_datos_drones()

    if not datos:
        st.markdown("<br><h4 style='text-align: center; color: gray;'>Radar en espera. No hay telemetría registrada.<br>Iniciá los clientes (drones) en la terminal para comenzar.</h4>", unsafe_allow_html=True)
        return

    # ======================================================================
    # RENDERIZADO DEL MAPA CENTRADO
    # ======================================================================
    # Usamos columnas para forzar al mapa a ubicarse exactamente en el centro
    col_mapa1, col_mapa_centro, col_mapa2 = st.columns([1, 10, 1])
    
    with col_mapa_centro:
        # Mapa blanco clásico (OpenStreetMap)
        mapa_c2 = folium.Map(location=[-32.8908, -68.8272], zoom_start=14, tiles="OpenStreetMap")

        # Círculo de cobertura del radar (Cian para que resalte en el mapa blanco)
        folium.Circle(
            location=[-32.8908, -68.8272],
            radius=1000,
            color="#0088ff",
            weight=2,
            fill=True,
            fill_opacity=0.1,
            tooltip="Área de Cobertura del C2 (1 km a la redonda)"
        ).add_to(mapa_c2)

        # Iteramos sobre los drones para dibujarlos
        for dron in datos:
            color_marcador = "green" if dron['estado'] == "active" else "red"

            folium.RegularPolygonMarker(
                location=[dron['lat'], dron['lon']],
                number_of_sides=3,
                radius=12,
                color=color_marcador,
                weight=2,
                fill=True,
                fill_color=color_marcador,
                fill_opacity=0.9,
                rotation=30,
                popup=f"<b>{dron['_id']}</b><br>Batería: {dron['bateria']}%",
                tooltip=f"ID: {dron['_id']} | Estado: {dron['estado'].upper()}"
            ).add_to(mapa_c2)

        st_folium(mapa_c2, width=1000, height=500, returned_objects=[])

    # ======================================================================
    # TABLA DE DATOS CENTRADA
    # ======================================================================
    st.markdown("<br><h3 style='text-align: center;'>📊 Estado General del Enjambre</h3>", unsafe_allow_html=True)
    
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
    
    # Centramos la tabla usando la misma técnica de columnas
    col_tabla1, col_tabla_centro, col_tabla2 = st.columns([2, 6, 2])
    with col_tabla_centro:
        st.dataframe(datos_tabla, use_container_width=True)

if __name__ == '__main__':
    main()