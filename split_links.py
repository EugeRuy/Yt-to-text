"""
split_links.py
--------------
Lee un único archivo .txt dentro de la carpeta 'Convertir' que contiene
una URL por línea y lo divide en archivos de 10 links cada uno.

Uso:
    python split_links.py
    python split_links.py --carpeta "MiCarpeta" --chunk 20
    
"""

import sys
import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Divide un .txt de links en partes iguales.")
    parser.add_argument(
        "--carpeta",
        default="Convertir",
        help="Nombre de la carpeta fuente (default: Convertir)",
    )
    parser.add_argument(
        "--chunk",
        type=int,
        default=10,
        help="Cantidad de links por archivo de salida (default: 10)",
    )
    return parser.parse_args()


def encontrar_txt_unico(carpeta: Path) -> Path:
    """Valida que exista exactamente un .txt en la carpeta y lo devuelve."""
    if not carpeta.exists():
        sys.exit(f"[ERROR] La carpeta '{carpeta}' no existe.")
    if not carpeta.is_dir():
        sys.exit(f"[ERROR] '{carpeta}' no es una carpeta.")

    txts = list(carpeta.glob("*.txt"))

    if len(txts) == 0:
        sys.exit(f"[ERROR] No se encontró ningún archivo .txt en '{carpeta}'.")
    if len(txts) > 1:
        nombres = ", ".join(f.name for f in txts)
        sys.exit(
            f"[ERROR] Se encontraron {len(txts)} archivos .txt en '{carpeta}'.\n"
            f"        Solo debe haber uno. Archivos encontrados: {nombres}"
        )

    return txts[0]


def leer_links(archivo: Path) -> list[str]:
    """Lee el archivo línea a línea y descarta líneas vacías."""
    links: list[str] = []

    # Lectura con buffer implícito del sistema — eficiente para ~2000 líneas y más
    with archivo.open("r", encoding="utf-8", errors="replace") as f:
        for linea in f:
            link = linea.strip()
            if link:
                links.append(link)

    return links


def dividir_y_guardar(links: list[str], carpeta_salida: Path, chunk: int) -> int:
    """Divide la lista en bloques y escribe cada uno en un archivo numerado."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    total = len(links)
    # Calcula cuántos archivos se necesitan sin cargar todo en memoria de golpe
    num_archivos = (total + chunk - 1) // chunk

    for i in range(num_archivos):
        inicio = i * chunk
        fin = inicio + chunk
        bloque = links[inicio:fin]

        archivo_salida = carpeta_salida / f"{i + 1}.txt"
        with archivo_salida.open("w", encoding="utf-8") as f:
            f.write("\n".join(bloque) + "\n")

    return num_archivos


def main() -> None:
    args = parse_args()

    carpeta = Path(args.carpeta)
    archivo_fuente = encontrar_txt_unico(carpeta)

    print(f"[INFO] Archivo encontrado: {archivo_fuente}")

    links = leer_links(archivo_fuente)

    if not links:
        sys.exit("[ERROR] El archivo existe pero no contiene links válidos.")

    print(f"[INFO] Total de links leídos: {len(links)}")

    # Los archivos generados se guardan dentro de Convertir/output/
    carpeta_salida = carpeta / "output"
    num_archivos = dividir_y_guardar(links, carpeta_salida, args.chunk)

    print(f"[OK]   Se generaron {num_archivos} archivo(s) en '{carpeta_salida}/'")
    print(f"       Cada archivo contiene hasta {args.chunk} links.")


if __name__ == "__main__":
    main()