import os
import sys
import random
import time

def generator_process(write_pipe):
    """Genera números aleatorios entre 1 y 100."""
    try:
        with os.fdopen(write_pipe, 'w') as pipe:
            print("Generador: Produciendo 10 números aleatorios...")
            for _ in range(10):
                num = random.randint(1, 100)
                pipe.write(f"{num}\n")
                pipe.flush()
                print(f"Generador: Generé el número {num}")
                time.sleep(0.5)  # Pequeña pausa para mejor visualización
    except Exception as e:
        print(f"Error en generador: {e}")
    finally:
        print("Generador: Terminando...")

def filter_process(read_pipe, write_pipe):
    """Filtra solo los números pares."""
    try:
        with os.fdopen(read_pipe, 'r') as in_pipe, os.fdopen(write_pipe, 'w') as out_pipe:
            print("Filtro: Filtrando números pares...")
            for line in in_pipe:
                num = int(line.strip())
                if num % 2 == 0:  # Solo procesar números pares
                    out_pipe.write(f"{num}\n")
                    out_pipe.flush()
                    print(f"Filtro: Pasando número par {num}")
                else:
                    print(f"Filtro: Descartando número impar {num}")
                time.sleep(0.3)  # Pequeña pausa
    except Exception as e:
        print(f"Error en filtro: {e}")
    finally:
        print("Filtro: Terminando...")

def square_process(read_pipe):
    """Calcula el cuadrado de los números recibidos."""
    try:
        with os.fdopen(read_pipe, 'r') as pipe:
            print("Cuadrador: Calculando cuadrados...")
            results = []
            for line in pipe:
                num = int(line.strip())
                square = num * num
                results.append((num, square))
                print(f"Cuadrador: {num}² = {square}")
                time.sleep(0.3)  # Pequeña pausa
            
            # Mostrar resumen final
            print("\nResultados finales:")
            for num, square in results:
                print(f"{num}² = {square}")
            print(f"Total de números procesados: {len(results)}")
    except Exception as e:
        print(f"Error en cuadrador: {e}")
    finally:
        print("Cuadrador: Terminando...")

def main():
    # Crear pipes para conectar los procesos
    pipe1_r, pipe1_w = os.pipe()  # Conecta generador -> filtro
    pipe2_r, pipe2_w = os.pipe()  # Conecta filtro -> cuadrador
    
    # Crear el primer proceso hijo (generador)
    pid1 = os.fork()
    
    if pid1 == 0:  # Proceso generador
        # Cerrar pipes no utilizados
        os.close(pipe1_r)
        os.close(pipe2_r)
        os.close(pipe2_w)
        
        # Ejecutar la función generadora
        generator_process(pipe1_w)
        sys.exit(0)
    
    # Crear el segundo proceso hijo (filtro)
    pid2 = os.fork()
    
    if pid2 == 0:  # Proceso filtro
        # Cerrar pipes no utilizados
        os.close(pipe1_w)
        os.close(pipe2_r)
        
        # Ejecutar la función de filtrado
        filter_process(pipe1_r, pipe2_w)
        sys.exit(0)
    
    # Proceso principal (cuadrador)
    # Cerrar pipes no utilizados
    os.close(pipe1_r)
    os.close(pipe1_w)
    os.close(pipe2_w)
    
    # Ejecutar la función cuadradora
    square_process(pipe2_r)
    
    # Esperar a que los procesos hijos terminen
    os.waitpid(pid1, 0)
    os.waitpid(pid2, 0)
    
    print("Pipeline completado.")

if __name__ == "__main__":
    main()