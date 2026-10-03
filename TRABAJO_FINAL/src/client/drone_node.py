# src/client/drone_node.py

import socket
import time
import json
import random
import argparse
import sys

# ==============================================================================
# Módulo: Cliente TCP (Simulador de Drone FPV)
# Materia: Computación II / Diseño de Bases de Datos II
# Objetivo: Conectarse al servidor C2, enviar telemetría en formato JSON y 
# simular el comportamiento de vuelo y consumo de batería de un nodo del enjambre.
# ==============================================================================

def configurar_argumentos():
    """
    Parsea los argumentos para apuntar al servidor correcto e identificar al dron.
    """
    parser = argparse.ArgumentParser(description="Nodo Cliente FPV para Sistema C2")
    parser.add_argument('--host', type=str, default='127.0.0.1', help='IP del servidor C2 (localhost por defecto)')
    parser.add_argument('--port', type=int, default=5000, help='Puerto del servidor C2')
    parser.add_argument('--id', type=str, required=True, help='Identificador único del dron (ej. D-Alpha)')
    return parser.parse_args()

def generar_telemetria(drone_id, lat_base, lon_base, bateria):
    """
    Genera un documento JSON denormalizado.
    Justificación BD2: Estructuramos la ubicación bajo el estándar GeoJSON
    (type: Point, coordinates: [longitud, latitud]). Esto es un requisito ESTRICTO
    para que MongoDB pueda crear el índice geoespacial '2dsphere' más adelante.
    """
    # Simulamos un pequeño movimiento aleatorio sumando/restando a las coordenadas base
    lat_actual = lat_base + random.uniform(-0.005, 0.005)
    lon_actual = lon_base + random.uniform(-0.005, 0.005)
    
    # Simulamos descarga de batería
    bateria_actual = max(0, bateria - random.uniform(0.5, 2.0))

    documento = {
        "drone_id": drone_id,
        "timestamp": time.time(),
        "status": "active" if bateria_actual > 15 else "low_battery",
        "battery_pct": round(bateria_actual, 2),
        "location": {
            "type": "Point",
            # IMPORTANTE: GeoJSON exige el orden [Longitud, Latitud]
            "coordinates": [round(lon_actual, 6), round(lat_actual, 6)]
        }
    }
    return documento, lat_actual, lon_actual, bateria_actual

def main():
    args = configurar_argumentos()
    
    # 1. INICIALIZACIÓN DEL CLIENTE TCP
    # A diferencia del servidor, este socket es un cliente activo que busca conectarse
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Intentamos enlazar (conectar) con el host y puerto especificados
        print(f"[INIT] Conectando el dron '{args.id}' al C2 Táctico en {args.host}:{args.port}...")
        client_socket.connect((args.host, args.port))
        print("[SUCCESS] Enlace establecido. Transmitiendo telemetría...")
        
        # Coordenadas base arbitrarias (Por ejemplo, el centro de tu zona de vuelo)
        lat_actual = -32.8908  # Latitud aproximada (ej. Mendoza)
        lon_actual = -68.8272  # Longitud aproximada
        bateria = 100.0

        # 2. BUCLE DE TRANSMISIÓN CONTINUA
        while bateria > 0:
            # Generamos el payload (carga útil) con los datos del dron
            telemetria, lat_actual, lon_actual, bateria = generar_telemetria(
                args.id, lat_actual, lon_actual, bateria
            )
            
            # Serializamos el diccionario de Python a un string JSON válido
            payload_json = json.dumps(telemetria)
            
            # Enviamos por la red. Los sockets de bajo nivel requieren bytes, por eso codificamos a utf-8.
            # Le agregamos un salto de línea (\n) por si necesitamos delimitar mensajes continuos en el stream.
            mensaje = f"{payload_json}\n".encode('utf-8')
            client_socket.sendall(mensaje)
            
            print(f"[TX] {args.id} | Batería: {telemetria['battery_pct']}% | Pos: {telemetria['location']['coordinates']}")
            
            # Simulamos el retardo de transmisión. Un pulso cada 3 segundos.
            time.sleep(3)

        print(f"[OFFLINE] {args.id} sin energía. Apagando sistemas.")

    except ConnectionRefusedError:
        print("[ERROR] Conexión rechazada. ¿El servidor C2 está encendido?")
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Piloto abortó la misión (Ctrl+C). Desconectando...")
    finally:
        # 3. CIERRE LIMPIO
        # Siempre cerramos el descriptor de archivo para liberar recursos del SO
        client_socket.close()

if __name__ == '__main__':
    main()