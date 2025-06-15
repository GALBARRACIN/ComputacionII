from multiprocessing import Process, Pipe, Queue
from procesos.generador import generador
from procesos.analizador_frecuencia import analizador_frecuencia
from procesos.analizador_presion import analizador_presion
from procesos.analizador_oxigeno import analizador_oxigeno
from procesos.verificador import verificador


def main():
    # Crear Pipes para enviar datos del generador a cada analizador
    p_frec_out, p_frec_in = Pipe(duplex=False)
    p_pres_out, p_pres_in = Pipe(duplex=False)
    p_oxi_out, p_oxi_in = Pipe(duplex=False)

    # Crear Queues para enviar resultados de cada analizador al verificador
    q_frec = Queue()
    q_pres = Queue()
    q_oxi = Queue()

    # Crear procesos de análisis
    proc_frec = Process(target=analizador_frecuencia, args=(p_frec_out, q_frec))
    proc_pres = Process(target=analizador_presion, args=(p_pres_out, q_pres))
    proc_oxi = Process(target=analizador_oxigeno, args=(p_oxi_out, q_oxi))

    # Crear proceso generador
    proc_gen = Process(target=generador, args=(p_frec_in, p_pres_in, p_oxi_in))

    # Crear proceso verificador
    proc_verif = Process(target=verificador, args=(q_frec, q_pres, q_oxi))

    # Iniciar todos los procesos
    proc_frec.start()
    proc_pres.start()
    proc_oxi.start()
    proc_verif.start()
    proc_gen.start()

    # Esperar a que finalicen
    proc_gen.join()
    proc_frec.join()
    proc_pres.join()
    proc_oxi.join()
    proc_verif.join()

    print("\n✅ Tarea 2 completada: bloques verificados, almacenados y encadenados.")


if __name__ == "__main__":
    main()
