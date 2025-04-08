# Importamos los módulos de ejercicios desde la carpeta 'ejercicios'
from ejercicios import ejercicio_01_padre_hijo
from ejercicios import ejercicio_02_doble_bifurcacion
from ejercicios import ejercicio_03_exec
from ejercicios import ejercicio_04_secuencia_controlada
from ejercicios import ejercicio_05_zombi_temporal
from ejercicios import ejercicio_06_huerfano_init
from ejercicios import ejercicio_07_multiproceso_paralelo
from ejercicios import ejercicio_08_servidor_multiproceso
from ejercicios import ejercicio_09_detectar_zombis
from ejercicios import ejercicio_10_inyeccion_comandos

def mostrar_menu():
    """
    Muestra el menú de opciones con los títulos de cada ejercicio.
    """
    print("======================================")
    print(" EJERCICIOS DE PROCESOS EN PYTHON")
    print("======================================")
    print("1. Identificación de procesos padre e hijo")
    print("2. Doble bifurcación")
    print("3. Reemplazo de un proceso hijo con exec()")
    print("4. Secuencia controlada de procesos")
    print("5. Proceso zombi temporal")
    print("6. Proceso huérfano adoptado por init")
    print("7. Multiproceso paralelo")
    print("8. Simulación de servidor multiproceso")
    print("9. Detección de procesos zombis en /proc")
    print("10. Inyección de comandos en procesos huérfanos")
    print("0. Salir")
    print("======================================")

def main():
    """
    Función principal que gestiona la ejecución de los ejercicios según la opción seleccionada por el usuario.
    """
    while True:
        mostrar_menu()  # Muestra el menú
        opcion = input("Seleccione un ejercicio (0 para salir): ")  # Espera la entrada del usuario

        # Lógica de selección basada en la opción del usuario
        if opcion == "1":
            ejercicio_01_padre_hijo.ejecutar()
        elif opcion == "2":
            ejercicio_02_doble_bifurcacion.ejecutar()
        elif opcion == "3":
            ejercicio_03_exec.ejecutar()
        elif opcion == "4":
            ejercicio_04_secuencia_controlada.ejecutar()
        elif opcion == "5":
            ejercicio_05_zombi_temporal.ejecutar()
        elif opcion == "6":
            ejercicio_06_huerfano_init.ejecutar()
        elif opcion == "7":
            ejercicio_07_multiproceso_paralelo.ejecutar()
        elif opcion == "8":
            ejercicio_08_servidor_multiproceso.ejecutar()
        elif opcion == "9":
            ejercicio_09_detectar_zombis.ejecutar()
        elif opcion == "10":
            ejercicio_10_inyeccion_comandos.ejecutar()
        elif opcion == "0":
            print("Saliendo...")
            break  # Sale del bucle principal y termina el programa
        else:
            print("Opción inválida. Intente nuevamente.")

# Verifica que el script esté siendo ejecutado directamente
if __name__ == "__main__":
    main()
