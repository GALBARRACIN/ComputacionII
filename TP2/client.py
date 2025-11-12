# client.py

import argparse
import asyncio
import json
import sys
import time
from typing import Optional
from urllib.parse import urlparse

import aiohttp

# Utilidades

def _normalize_server(server: str) -> str:
    # Asegura que la URL del servidor tenga esquema (http/https)
    if not server:
        raise ValueError("Servidor vacío")
    parsed = urlparse(server)
    if not parsed.scheme:
        server = "http://" + server
    return server.rstrip("/")


def _pretty(obj) -> str:
    # Formatea JSON para imprimir en consola
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except Exception:
        return str(obj)


# Lógica de cliente async
async def request_scrape(
    server: str,
    url: str,
    wait: bool = False,
    timeout: int = 30,
    poll_interval: float = 1.0,
) -> None:

    server = _normalize_server(server)

    # Timeout por operación de red (conexión/lectura). No limitamos el total del session.
    client_timeout = aiohttp.ClientTimeout(sock_connect=10, sock_read=30)

    # Usamos una sola sesión para todas las peticiones
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        # 1) Enviar solicitud de scraping
        try:
            async with session.post(f"{server}/scrape", json={"url": url}) as resp:
                text = await resp.text()
                if resp.status != 200:
                    print(f"Error al encolar (HTTP {resp.status}): {text}")
                    return
                try:
                    data = await resp.json()
                except json.JSONDecodeError:
                    print(f"Respuesta inválida JSON al encolar: {text}")
                    return
        except asyncio.TimeoutError:
            print("Timeout al conectar con el servidor al encolar.")
            return
        except aiohttp.ClientError as e:
            print(f"Error de red al encolar: {e}")
            return

        # Mostrar respuesta de encolado
        print("Encolado:", _pretty(data))
        task_id = data.get("task_id")
        if not task_id:
            print("No se recibió task_id. Fin.")
            return

        # Si no pide esperar, terminamos mostrando el task_id
        if not wait:
            print(f"Task ID: {task_id} (no se espera resultado).")
            return

        # 2) Esperar resultado consultando /status y /result
        start = time.time()
        interval = max(0.1, float(poll_interval))
        max_interval = 5.0

        while True:
            elapsed = time.time() - start
            if elapsed > timeout:
                print("Timeout esperando resultado (tiempo total excedido).")
                return

            # Consultar status
            try:
                async with session.get(f"{server}/status/{task_id}") as s:
                    if s.status != 200:
                        # Si el endpoint devuelve 404/500, lo informamos pero seguimos intentando hasta timeout
                        text = await s.text()
                        print(f"Status HTTP {s.status}: {text}")
                    else:
                        st = await s.json()
                        print("Status:", _pretty(st))
                        status_val = st.get("status")
                        if status_val == "completed":
                            # Cuando está completo, pedimos el resultado final
                            try:
                                async with session.get(f"{server}/result/{task_id}") as r:
                                    if r.status == 200:
                                        try:
                                            res = await r.json()
                                            print("Resultado final:", _pretty(res))
                                            return
                                        except json.JSONDecodeError:
                                            print("Resultado no es JSON válido.")
                                            return
                                    elif r.status == 202:
                                        # Resultado aún no listo, seguimos esperando
                                        print("Resultado aún no disponible (202).")
                                    else:
                                        text = await r.text()
                                        print(f"Error al obtener resultado (HTTP {r.status}): {text}")
                                        # Si es un error permanente, salimos
                                        if 400 <= r.status < 500:
                                            return
                            except asyncio.TimeoutError:
                                print("Timeout al solicitar resultado, reintentando...")
                            except aiohttp.ClientError as e:
                                print(f"Error de red al solicitar resultado: {e}")
                        elif status_val == "failed":
                            print("La tarea falló en el servidor de procesamiento.")
                            # Intentamos obtener detalles del resultado si existe
                            try:
                                async with session.get(f"{server}/result/{task_id}") as r2:
                                    if r2.status == 200:
                                        res = await r2.json()
                                        print("Detalle de fallo:", _pretty(res))
                            except Exception:
                                pass
                            return

            except asyncio.TimeoutError:
                print("Timeout al consultar status, reintentando...")
            except aiohttp.ClientError as e:
                print(f"Error de red al consultar status: {e}")

            # Backoff exponencial simple para no saturar el servidor
            await asyncio.sleep(interval)
            interval = min(max_interval, interval * 1.5)


# CLI

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cliente de prueba para servidor_scraping (Parte A)")
    parser.add_argument("-s", "--server", required=True, help="URL del servidor A (ej: http://127.0.0.1:8000)")
    parser.add_argument("-u", "--url", required=True, help="URL a scrapear")
    parser.add_argument("--wait", action="store_true", help="Esperar hasta obtener resultado (por defecto no)")
    parser.add_argument(
        "-t", "--timeout", type=int, default=60, help="Timeout total en segundos cuando --wait (default: 60)"
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=1.0,
        help="Intervalo inicial entre consultas de estado en segundos (default: 1.0)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        asyncio.run(
            request_scrape(
                server=args.server,
                url=args.url,
                wait=args.wait,
                timeout=args.timeout,
                poll_interval=args.poll_interval,
            )
        )
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario.")
        sys.exit(1)


if __name__ == "__main__":
    main()
