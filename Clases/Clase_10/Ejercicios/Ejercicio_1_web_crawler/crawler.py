import threading
import requests
import time

# Lista de URLs a crawlear
URLS_TO_CRAWL = [
    "http://python.org",
    "http://example.com",
    "https://www.djangoproject.com/",
    "https://flask.palletsprojects.com/",
    "http://invalid.url.that.will.fail",  # Para probar manejo de errores
    "https://docs.python.org/3/library/threading.html"
]

# Diccionario de resultados compartido y su lock
results = {}
results_lock = threading.Lock()

def crawl_url(url, thread_id):
    print(f"[{thread_id}] Iniciando crawl para {url}")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        content_size = len(response.text)
        print(f"[{thread_id}] Descargado {url} ({content_size} bytes)")
    except requests.exceptions.RequestException as e:
        print(f"[{thread_id}] Error al acceder a {url}: {e}")
        content_size = -1
    # Sección crítica
    with results_lock:
        results[url] = content_size

if __name__ == "__main__":
    start = time.time()
    threads = []

    for idx, url in enumerate(URLS_TO_CRAWL):
        thread = threading.Thread(target=crawl_url, args=(url, idx), name=f"Crawler-{idx}")
        threads.append(thread)
        thread.start()

    # Esperar a todos los hilos
    for thread in threads:
        thread.join()

    print("\n📊 Resultados:")
    for url, size in results.items():
        estado = f"{size} bytes" if size != -1 else "❌ Falló"
        print(f"- {url}: {estado}")

    print(f"\n⏱️ Tiempo total: {time.time() - start:.2f} segundos")
