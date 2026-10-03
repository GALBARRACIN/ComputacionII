# src/server/c2_server.py

import socket
import select
import argparse
import sys
import os
import json

# ==============================================================================
# SOLUCIÓN AL ERROR ModuleNotFoundError
# Calculamos la ruta absoluta de la raíz del proyecto y la agregamos al sistema
# para que Python pueda importar 'src.tasks.worker' sin problemas de rutas.
# ==============================================================================
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)

# Ahora sí, importamos la tarea asíncrona de Celery
from src.tasks.worker import procesar_telemetria

# ==============================================================================
# Módulo: Servidor C2 Táctico (Comando y Control)
# Materia: Computación II
# Objetivo: Manejar conexiones TCP concurrentemente (select), usar IPC (Pipes)
# para alertas del sistema, y delegar inserciones de BD a Celery (Redis).
# ==============================================================================

def configurar_argumentos():
    """
    Cumple el requisito de parseo de argumentos por línea de comandos (argparse).
    Permite parametrizar el servidor sin modificar el código fuente.
    """
    parser = argparse.ArgumentParser(description="Servidor C2 Táctico para enjambre FPV")
    # --host: 0.0.0.0 significa que escuchará en todas las interfaces de red de tu Linux
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Dirección IP de escucha del radar')
    # --port: Puerto TCP donde los clientes (drones) enviarán su telemetría
    parser.add_argument('--port', type=int, default=5000, help='Puerto TCP del servidor')
    
    return parser.parse_args()

def main():
    args = configurar_argumentos()
    
    # ==========================================================================
    # 1. CREACIÓN DEL PIPE PARA COMUNICACIÓN INTER-PROCESOS (IPC)
    # ==========================================================================
    # os.pipe() crea un canal de comunicación a nivel kernel de Debian.
    # Devuelve dos descriptores: pipe_r (para Leer alertas) y pipe_w (para Escribir).
    pipe_r, pipe_w = os.pipe()
    # Hacemos que la lectura del pipe sea NO BLOQUEANTE para que funcione con select
    os.set_blocking(pipe_r, False)

    # ==========================================================================
    # 2. CREACIÓN DEL SOCKET TCP MAESTRO
    # ==========================================================================
    # AF_INET = Familia IPv4. SOCK_STREAM = Protocolo TCP.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SO_REUSEADDR permite reutilizar el puerto inmediatamente si reiniciamos.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # VINCULACIÓN Y ESCUCHA (BIND & LISTEN)
    server_socket.bind((args.host, args.port))
    server_socket.listen(10)
    
    # CRÍTICO: Socket del servidor NO BLOQUEANTE. 
    # Delegamos el control del flujo a la función 'select'.
    server_socket.setblocking(False)
    
    print(f"[START] Radar C2 Táctico operando en {args.host}:{args.port}")
    print("[INFO] Esperando telemetría GIS (Multiplexación asíncrona de Sockets y Pipes)...")
    
    # ==========================================================================
    # 3. LISTAS DE CONTROL PARA MULTIPLEXACIÓN (SELECT)
    # ==========================================================================
    # inputs: Archivos que queremos LEER. Vigilará nuevos drones (server_socket)
    # y también vigilará alertas del sistema operativo (pipe_r).
    inputs = [server_socket, pipe_r]
    outputs = []
    exceptions = [server_socket]

    try:
        # ======================================================================
        # 4. BUCLE PRINCIPAL ASÍNCRONO DE I/O
        # ======================================================================
        while inputs:
            # select bloquea el hilo SOLO hasta que un socket o el pipe tenga datos listos
            readable, writable, exceptional = select.select(inputs, outputs, exceptions)

            for s in readable:
                
                # CASO A: NUEVA CONEXIÓN DE UN DRON
                if s is server_socket:
                    client_socket, client_address = s.accept()
                    client_socket.setblocking(False)
                    inputs.append(client_socket)
                    print(f"[CONEXIÓN] Drone enlazado desde {client_address}")
                
                # CASO B: LECTURA DEL PIPE DE ALERTAS (Requisito IPC)
                elif s is pipe_r:
                    alerta_bytes = os.read(pipe_r, 1024)
                    alerta_str = alerta_bytes.decode('utf-8').strip()
                    print(f"\n[!!! ALERTA IPC CRÍTICA !!!] -> {alerta_str}\n")

                # CASO C: RECEPCIÓN DE TELEMETRÍA (Datos de un dron conectado)
                else:
                    try:
                        data = s.recv(1024)
                        if data:
                            # Parseamos los mensajes separados por saltos de línea
                            mensajes = data.decode('utf-8').strip().split('\n')
                            
                            for msg in mensajes:
                                if not msg: continue
                                
                                # 1. INTEGRACIÓN CON CELERY (Requisito Concurrencia)
                                # Enviamos el JSON a Redis. El '.delay()' asegura que 
                                # este servidor no se frene esperando a la Base de Datos.
                                procesar_telemetria.delay(msg)
                                
                                # 2. EVALUACIÓN DE ESTADO PARA DISPARAR EL PIPE
                                try:
                                    doc = json.loads(msg)
                                    # Si detectamos batería baja, escribimos en el pipe
                                    if doc.get("status") == "low_battery":
                                        msg_alerta = f"Dron {doc.get('drone_id')} con batería crítica al {doc.get('battery_pct')}%"
                                        os.write(pipe_w, msg_alerta.encode('utf-8'))
                                except json.JSONDecodeError:
                                    pass

                        else:
                            # Cierre limpio de conexión TCP (0 bytes recibidos)
                            print(f"[DESCONEXIÓN LIMPIA] Drone {s.getpeername()} fuera de línea.")
                            inputs.remove(s)
                            s.close()

                    except ConnectionResetError:
                        print("[ALERTA TCP] Conexión perdida abruptamente (RST).")
                        inputs.remove(s)
                        s.close()

            # Manejo de sockets con errores de capa de red
            for s in exceptional:
                print(f"[ERROR TCP] Excepción en descriptor.")
                inputs.remove(s)
                s.close()

    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Cerrando sockets, pipes y apagando el servidor C2...")
        for s in inputs:
            # Manejamos el cierre diferenciando pipes (enteros) de sockets (objetos)
            if isinstance(s, int):
                os.close(s)
            else:
                s.close()
        os.close(pipe_w)
        sys.exit(0)

if __name__ == '__main__':
    main()