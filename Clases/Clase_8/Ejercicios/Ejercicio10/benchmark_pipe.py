from multiprocessing import Process, Pipe
import time

def test_pipe(conn):
    """Envía un millón de enteros a través de Pipe() y mide el tiempo."""
    inicio = time.time()
    conn.send(list(range(1_000_000)))
    conn.recv()  # Espera confirmación
    fin = time.time()
    return fin - inicio

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=test_pipe, args=(child_conn,))
    p.start()
    p.join()
    print(f"Tiempo Pipe: {test_pipe(parent_conn):.2f} segundos")
