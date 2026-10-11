# src/ui/dashboard.py

import streamlit as st
import folium
from streamlit_folium import st_folium
import sys
import os
import time  # Necesario para el intervalo de actualización automática (Polling)
import math  # Necesario para las funciones trigonométricas de la fórmula de Haversine

# ==============================================================================
# RESOLUCIÓN DE RUTAS (PYTHONPATH)
# Al ejecutar el script directamente con Streamlit, Python pierde el contexto 
# del paquete 'src'. Calculamos la ruta absoluta a la raíz del proyecto y la 
# inyectamos en sys.path para poder importar mongo_setup sin errores.
# ==============================================================================
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)

from src.db.mongo_setup import get_database

# Constantes tácticas: Coordenadas del Centro de Comando (Mendoza) y Radio de alcance
LAT_BASE = -32.8908
LON_BASE = -68.8272
RADIO_C2_METROS = 1000

# ==============================================================================
# Módulo: Interfaz Visual y Renderizado GIS (Frontend)
# Consumo de MongoDB y mapeo geoespacial en tiempo real con soporte de Polling.
# ==============================================================================

# Configura el layout de la página web para ocupar todo el ancho del monitor
st.set_page_config(page_title="Radar C2 Táctico", layout="wide")

def obtener_datos_drones():
    """
    Se conecta a la BD y extrae EXCLUSIVAMENTE la última coordenada de cada dron.
    
    Justificación técnica (BD II): Si hiciéramos un find() normal, traeríamos todo el 
    historial de vuelo, sobrecargando la memoria RAM y dibujando miles de puntos por dron.
    Usamos el Aggregation Framework para filtrar en el motor de BD y quedarnos solo 
    con la posición más reciente de cada unidad.
    """
    db = get_database()
    coleccion = db['telemetria']
    
    pipeline = [
        # 1. $sort: Ordenamos toda la colección por timestamp de mayor a menor (-1).
        # Esto garantiza que los registros más recientes queden primeros.
        {"$sort": {"timestamp": -1}},
        
        # 2. $group: Agrupamos los documentos por el identificador único del dron.
        {"$group": {
            "_id": "$drone_id",
            # Al usar $first, tomamos únicamente el primer documento de cada grupo 
            # (que es el más actual gracias al $sort de la etapa anterior).
            
            # El campo 'location.coordinates' sigue el estándar GeoJSON: [longitud, latitud].
            # $arrayElemAt extrae el índice 1 (Latitud) y el índice 0 (Longitud).
            "lat": {"$first": {"$arrayElemAt": ["$location.coordinates", 1]}},
            "lon": {"$first": {"$arrayElemAt": ["$location.coordinates", 0]}},
            
            "bateria": {"$first": "$battery_pct"},
            "estado": {"$first": "$status"}
        }}
    ]
    return list(coleccion.aggregate(pipeline))

def limpiar_base_datos():
    """
    Función auxiliar para borrar los documentos residuales de pruebas anteriores.
    Ejecuta un delete_many({}) sobre la colección para iniciar la demostración en limpio.
    """
    db = get_database()
    db['telemetria'].delete_many({})

def calcular_distancia_metros(lat1, lon1, lat2, lon2):
    """
    Fórmula de Haversine: Calcula la distancia ortodrómica (real en metros) entre 
    dos coordenadas GPS tomando en cuenta la curvatura esférica de la Tierra.
    """
    R = 6371000  # Radio medio de la Tierra en metros
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi / 2) ** 2) + \
        math.cos(phi1) * math.cos(phi2) * \
        (math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return round(R * c, 2)

def main():
    # ======================================================================
    # ENCABEZADO CENTRADO (Estética de la UI)
    # ======================================================================
    st.markdown("<h1 style='text-align: center;'>🛰️ Sistema C2 Táctico - Enjambre FPV</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Monitoreo en tiempo real. <b>Base de Datos:</b> MongoDB | <b>Concurrencia:</b> Celery + TCP Sockets</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Contenedor de columnas para centrar los controles operativos del radar
    col_esp1, col_auto, col_btn_act, col_btn_limpiar, col_esp2 = st.columns([2, 2, 2, 2, 2])
    
    with col_auto:
        # Checkbox para activar el barrido automático (Polling cada 2 segundos)
        auto_refresh = st.checkbox("📡 Activar Auto-Rastreo (2s)")
            
    with col_btn_act:
        # Fuerza a Streamlit a reejecutar el script de arriba a abajo manualmente
        if st.button("🔄 Forzar Actualización", use_container_width=True):
            st.rerun()
            
    with col_btn_limpiar:
        if st.button("🗑️ Limpiar Historial", use_container_width=True):
            limpiar_base_datos()
            st.rerun()

    datos = obtener_datos_drones()

    if not datos:
        st.markdown("<br><h4 style='text-align: center; color: gray;'>Radar en espera. No hay telemetría registrada.<br>Iniciá los clientes (drones) en la terminal para comenzar.</h4>", unsafe_allow_html=True)
        # Si el auto-rastreo está activo, sigue consultando la BD aunque esté vacía
        if auto_refresh:
            time.sleep(2)
            st.rerun()
        return

    # ======================================================================
    # RENDERIZADO DEL MAPA CENTRADO (Folium + OpenStreetMap)
    # ======================================================================
    # Usamos columnas para ubicar el mapa exactamente en el centro de la pantalla
    col_mapa1, col_mapa_centro, col_mapa2 = st.columns([1, 10, 1])
    
    with col_mapa_centro:
        # Inicializamos el mapa con OpenStreetMap (open-source, no requiere API Key)
        mapa_c2 = folium.Map(location=[LAT_BASE, LON_BASE], zoom_start=14, tiles="OpenStreetMap")

        # Dibujamos el perímetro de cobertura del radar (1000 metros a la redonda)
        folium.Circle(
            location=[LAT_BASE, LON_BASE],
            radius=RADIO_C2_METROS,
            color="#0088ff",
            weight=2,
            fill=True,
            fill_opacity=0.1,
            tooltip="Área de Cobertura del C2 (1 km a la redonda)"
        ).add_to(mapa_c2)

        datos_tabla = []

        # Iteramos sobre los resultados agrupados que devolvió MongoDB
        for dron in datos:
            # 1. Calculamos a qué distancia en metros está el dron respecto a la base
            distancia = calcular_distancia_metros(LAT_BASE, LON_BASE, dron['lat'], dron['lon'])
            
            # 2. Lógica Táctica: Evaluamos si se encuentra dentro del radio de cobertura
            if distancia <= RADIO_C2_METROS:
                cobertura = "🟢 EN RANGO"
                # Verde si la batería es normal ('active'), rojo si es crítica ('low_battery')
                color_marcador = "green" if dron['estado'] == "active" else "red"
                opacidad = 0.9
            else:
                cobertura = "⚪ SEÑAL PERDIDA"
                # Gris semi-transparente: muestra la última posición conocida fuera del radar
                color_marcador = "gray"
                opacidad = 0.5

            # Dibujamos el marcador triangular estilo UAV
            folium.RegularPolygonMarker(
                location=[dron['lat'], dron['lon']],
                number_of_sides=3,
                radius=12,
                color=color_marcador,
                weight=2,
                fill=True,
                fill_color=color_marcador,
                fill_opacity=opacidad,
                rotation=30,
                popup=f"<b>{dron['_id']}</b><br>Batería: {dron['bateria']}%<br>Distancia: {distancia}m",
                tooltip=f"ID: {dron['_id']} | {cobertura} ({distancia}m)"
            ).add_to(mapa_c2)

            # Agregamos los datos procesados de este dron a la lista para la tabla inferior
            datos_tabla.append({
                "Dron ID": dron["_id"],
                "Cobertura": cobertura,
                "Distancia a Base": f"{distancia} m",
                "Estado Energía": dron["estado"].upper(),
                "Batería (%)": dron["bateria"],
                "Latitud": dron["lat"],
                "Longitud": dron["lon"]
            })

        # Renderiza el mapa en Streamlit sin recargar eventos innecesarios (returned_objects=[])
        st_folium(mapa_c2, width=1000, height=500, returned_objects=[])

    # ======================================================================
    # DATAFRAME DE RESPALDO (Tabla visual centrada)
    # ======================================================================
    st.markdown("<br><h3 style='text-align: center;'>📊 Estado General del Enjambre</h3>", unsafe_allow_html=True)
    
    col_tabla1, col_tabla_centro, col_tabla2 = st.columns([1, 8, 1])
    with col_tabla_centro:
        st.dataframe(datos_tabla, use_container_width=True)

    # ======================================================================
    # LÓGICA DE ACTUALIZACIÓN EN TIEMPO REAL (POLLING)
    # ======================================================================
    # Si el operador activó el checkbox, esperamos 2 segundos y forzamos
    # la recarga del script para consultar las nuevas coordenadas en MongoDB.
    if auto_refresh:
        time.sleep(2)
        st.rerun()

if __name__ == '__main__':
    main()