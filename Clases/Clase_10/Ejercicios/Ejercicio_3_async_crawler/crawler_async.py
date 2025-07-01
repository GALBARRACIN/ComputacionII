import asyncio
import aiohttp
import time

URLS = [
    "http://python.org",
    "http://example.com",
    "https://www.djangoproject.com/",
    "https://flask.palletsprojects.com/",
    "http://invalid.url.that.will.fail",  # Para simular error
    "https://docs.python.org/3/library/asyncio.html"
]

async def fetch(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            content = await response.text()
            size = len(content)
            print(f"✅ {url}: {size} bytes")
            return url, size
    except Exception as e:
        print(f"❌ {url}: {e}")
        return url, -1

async def crawl_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return dict(results)

if __name__ == "__main__":
    start = time.time()
    results = asyncio.run(crawl_all(URLS))
    print("\n📊 Resultados:")
    for url, size in results.items():
        estado = f"{size} bytes" if size != -1 else "Falló"
        print(f"- {url}: {estado}")
    print(f"\n⏱️ Tiempo total: {time.time() - start:.2f} segundos")
