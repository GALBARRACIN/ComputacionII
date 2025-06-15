from multiprocessing import Process, Pipe, Queue
from procesos.generador import generador
from procesos.analizador_frecuencia import analizador_frecuencia
from procesos.analizador_presion import analizador_presion
from procesos.analizador_oxigeno import analizador_oxigeno


def main():
    # Crear Pipes de entrada para cada proceso analizador (1 vía por tipo de señal)
    p_frec_out, p_frec_in = Pipe(duplex=False)
    p_pres_out, p_pres_in = Pipe(duplex=False)
    p_oxi_out, p_oxi_in = Pipe(duplex=False)

    # Crear Queues de salida de cada proceso analizador (para resultados)
    q_frec = Queue()
    q_pres = Queue()
    q_oxi = Queue()

    # Lanzar procesos de análisis
    proc_frec = Process(target=analizador_frecuencia, args=(p_frec_out, q_frec))
    proc_pres = Process(target=analizador_presion, args=(p_pres_out, q_pres))
    proc_oxi = Process(target=analizador_oxigeno, args=(p_oxi_out, q_oxi))

    # Lanzar proceso generador
    proc_gen = Process(target=generador, args=(p_frec_in, p_pres_in, p_oxi_in))

    # Iniciar todos los procesos
    proc_frec.start()
    proc_pres.start()
    proc_oxi.start()
    proc_gen.start()

    # Esperar que todos terminen
    proc_gen.join()
    proc_frec.join()
    proc_pres.join()
    proc_oxi.join()

    print("\nTarea 1 completada: generación y análisis concurrente finalizados.\n")

    # Test: imprimir resultados generados por cada analizador
    print("📊 Resultados de Frecuencia:")
    while not q_frec.empty():
        print(q_frec.get())

    print("\n📊 Resultados de Presión:")
    while not q_pres.empty():
        print(q_pres.get())

    print("\n📊 Resultados de Oxígeno:")
    while not q_oxi.empty():
        print(q_oxi.get())


if __name__ == "__main__":
    main()
