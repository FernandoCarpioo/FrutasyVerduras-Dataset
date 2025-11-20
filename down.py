import os
from icrawler.builtin import BingImageCrawler

# Búsquedas mejoradas para uvas
uvas_map = {
    "Uva_verde": '"grape" "bunch" "green" "fresh"',
    "Uva_roja": '"grape" "bunch" "red" "fresh"'
}

def descargar_uvas():
    base_dir = "Uvas"

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for carpeta, termino_busqueda in uvas_map.items():
        print(f"\n--------------------------------------------------")
        print(f"Carpeta destino: {carpeta}")
        print(f"Buscando: {termino_busqueda}")
        print(f"--------------------------------------------------")

        ruta_destino = os.path.join(base_dir, carpeta)

        crawler = BingImageCrawler(
            downloader_threads=4,
            storage={'root_dir': ruta_destino}
        )

        crawler.crawl(
            keyword=termino_busqueda,
            filters=dict(type='photo'),
            max_num=100
        )

if __name__ == "__main__":
    descargar_uvas()
    print("\n\n✅ ¡Descarga de uvas finalizada!")
