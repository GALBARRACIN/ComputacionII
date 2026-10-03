# src/server/c2_server.py

import socket
import select
import argparse
import sys

# ==============================================================================
# Módulo: Servidor C2 Táctico (Comando y Control)
# Materia: Computación II
# Objetivo: Manejar múltiples conexiones TCP de drones concurrentemente
# mediante multiplexación I/O (select), evitando el uso de hilos (threads).
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
    
    # 1. CREACIÓN DEL SOCKET TCP MAESTRO
    # AF_INET = Familia de direcciones IPv4. 
    # SOCK_STREAM = Protocolo TCP (orientado a conexión, garantiza entrega de paquetes).
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SO_REUSEADDR permite reutilizar el puerto inmediatamente si reiniciamos el script.
    # Justificación para el examen: Evita el molesto error "Address already in use" de Linux 
    # cuando un socket queda en estado TIME_WAIT tras cerrar el servidor.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 2. VINCULACIÓN Y ESCUCHA (BIND & LISTEN)
    server_socket.bind((args.host, args.port))
    
    # El backlog (10) define el tamaño de la cola de conexiones pendientes. 
    # Soporta ráfagas de hasta 10 drones intentando conectarse en el mismo milisegundo.
    server_socket.listen(10)
    
    # CRÍTICO: Hacemos que el socket del servidor sea NO BLOQUEANTE.
    # Si fuera bloqueante, el método accept() detendría todo el programa. Al ser asíncrono,
    # delegamos el control del flujo a la función 'select'.
    server_socket.setblocking(False)
    
    print(f"[START] Radar C2 Táctico operando en {args.host}:{args.port}")
    print("[INFO] Esperando telemetría GIS (Multiplexación asíncrona con select)...")
    
    # 3. LISTAS DE CONTROL PARA MULTIPLEXACIÓN (SELECT)
    # inputs: Sockets de los que queremos LEER datos. Inicialmente solo está el server_socket
    # esperando nuevas peticiones de conexión.
    inputs = [server_socket]
    
    # outputs: Sockets a los que queremos ESCRIBIR (actualmente no lo usamos activamente, 
    # pero es requerido por la firma de select).
    outputs = []
    
    # exceptions: Sockets para monitorear errores fuera de banda.
    exceptions = [server_socket]

    try:
        # 4. BUCLE PRINCIPAL ASÍNCRONO DE I/O
        while inputs:
            # select.select bloquea el hilo SOLO hasta que al menos un socket de las listas
            # cambie de estado (esté listo para lectura, escritura o lance error).
            # Esto es lo que permite atender a MÚLTIPLES clientes concurrentes con un solo hilo.
            readable, writable, exceptional = select.select(inputs, outputs, exceptions)

            # Iteramos sobre los sockets que tienen datos listos para ser leídos
            for s in readable:
                
                # CASO A: El socket listo es el servidor. Significa que un NUEVO drone quiere conectarse.
                if s is server_socket:
                    client_socket, client_address = s.accept()
                    # El socket del cliente TAMBIÉN debe ser no bloqueante
                    client_socket.setblocking(False)
                    # Lo agregamos a nuestra lista maestra de lectura
                    inputs.append(client_socket)
                    print(f"[CONEXIÓN] Drone enlazado desde {client_address}")
                
                # CASO B: El socket listo es un cliente. Significa que un drone YA CONECTADO nos envió datos.
                else:
                    try:
                        # Recibimos hasta 1024 bytes de carga útil (telemetría GIS)
                        data = s.recv(1024)
                        if data:
                            mensaje = data.decode('utf-8').strip()
                            # Aquí es donde más adelante parsearemos el JSON, enviaremos a Celery (Computación II)
                            # y guardaremos el documento en MongoDB (Base de Datos II).
                            print(f"[TELEMETRÍA] {s.getpeername()}: {mensaje}")
                        else:
                            # Si data está vacío (0 bytes), el protocolo TCP indica un cierre limpio de conexión
                            print(f"[DESCONEXIÓN LIMPIA] Drone {s.getpeername()} fuera de línea.")
                            inputs.remove(s)
                            s.close()
                    except ConnectionResetError:
                        # Manejo de excepciones si un drone pierde energía o cae, rompiendo el socket abruptamente
                        print("[ALERTA CRÍTICA] Conexión perdida (RST) de forma abrupta.")
                        inputs.remove(s)
                        s.close()

            # Manejo de sockets con errores de capa de red
            for s in exceptional:
                print(f"[ERROR TCP] Excepción en la conexión de {s.getpeername()}")
                inputs.remove(s)
                s.close()

    except KeyboardInterrupt:
        # Capturamos Ctrl+C para realizar un apagado elegante (Graceful Shutdown)
        print("\n[SHUTDOWN] Cerrando sockets y apagando el servidor C2...")
        for s in inputs:
            s.close()
        sys.exit(0)

if __name__ == '__main__':
    main()