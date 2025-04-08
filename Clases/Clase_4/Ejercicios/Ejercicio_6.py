import os
import sys
import re
import signal
import time

def setup_signal_handler():
    """Configura el manejador de señales para salir limpiamente con Ctrl+C"""
    def signal_handler(sig, frame):
        print("\nFinalizando servidor...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

def math_server(request_pipe, response_pipe):
    """
    Proceso servidor que recibe operaciones matemáticas,
    las evalúa y devuelve el resultado.
    """
    try:
        print("Servidor: Iniciando servidor de operaciones matemáticas...")
        
        # Abrir pipes para lectura/escritura
        with os.fdopen(request_pipe, 'r') as requests, os.fdopen(response_pipe, 'w') as responses:
            while True:
                # Leer una operación del cliente
                operation = requests.readline().strip()
                
                if not operation or operation.lower() == "exit":
                    print("Servidor: Recibida señal de finalización")
                    break
                
                print(f"Servidor: Recibida operación: '{operation}'")
                
                # Procesar la operación con un pequeño retraso para simular procesamiento
                time.sleep(0.5)
                result = evaluate_expression(operation)
                
                # Enviar el resultado al cliente
                responses.write(f"{result}\n")
                responses.flush()
                print(f"Servidor: Enviado resultado: '{result}'")
                
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        print("Servidor: Finalizando...")

def evaluate_expression(expression):
    """
    Evalúa una expresión matemática y devuelve el resultado.
    Maneja errores y validaciones.
    """
    try:
        # Verificar si la expresión tiene formato válido
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', expression):
            return "ERROR: Expresión inválida. Solo se permiten números y operadores +,-,*,/,(,)"
        
        # Evaluar la expresión de forma segura
        # Limitamos a operaciones matemáticas básicas
        result = eval(expression)
        return str(result)
        
    except ZeroDivisionError:
        return "ERROR: División por cero"
    except SyntaxError:
        return "ERROR: Sintaxis incorrecta"
    except Exception as e:
        return f"ERROR: {str(e)}"

def math_client(request_pipe, response_pipe):
    """
    Proceso cliente que envía operaciones matemáticas al servidor
    y muestra los resultados.
    """
    try:
        print("\nCliente: Conectando al servidor de operaciones matemáticas...")
        print("Ingrese operaciones matemáticas o 'exit' para salir")
        print("Ejemplos: '5 + 3', '10 * (2 + 3)', '15 / 2'")
        
        # Abrir pipes para lectura/escritura
        with os.fdopen(request_pipe, 'w') as requests, os.fdopen(response_pipe, 'r') as responses:
            while True:
                # Solicitar una operación al usuario
                expression = input("\nIngrese operación > ")
                
                if expression.lower() == "exit":
                    print("Cliente: Enviando señal de finalización al servidor")
                    requests.write("exit\n")
                    requests.flush()
                    break
                
                # Enviar la operación al servidor
                requests.write(f"{expression}\n")
                requests.flush()
                print(f"Cliente: Enviada operación: '{expression}'")
                
                # Recibir y mostrar el resultado
                result = responses.readline().strip()
                if result.startswith("ERROR"):
                    print(f"Cliente: Error - {result}")
                else:
                    print(f"Cliente: Resultado: {expression} = {result}")
    
    except Exception as e:
        print(f"Error en el cliente: {e}")
    finally:
        print("Cliente: Finalizando...")

def main():
    # Configurar manejador de señales
    setup_signal_handler()
    
    # Crear pipes para comunicación bidireccional
    client_to_server_r, client_to_server_w = os.pipe()  # Cliente -> Servidor
    server_to_client_r, server_to_client_w = os.pipe()  # Servidor -> Cliente
    
    # Bifurcar el proceso
    pid = os.fork()
    
    if pid > 0:  # Proceso padre (cliente)
        # Cerrar extremos no utilizados
        os.close(client_to_server_r)
        os.close(server_to_client_w)
        
        # Ejecutar cliente
        math_client(client_to_server_w, server_to_client_r)
        
        # Esperar a que el servidor termine
        try:
            os.waitpid(pid, 0)
        except:
            pass
        
        print("Terminando programa")
        
    else:  # Proceso hijo (servidor)
        # Cerrar extremos no utilizados
        os.close(client_to_server_w)
        os.close(server_to_client_r)
        
        # Ejecutar servidor
        math_server(client_to_server_r, server_to_client_w)
        
        # Salir del proceso hijo
        sys.exit(0)

if __name__ == "__main__":
    main()