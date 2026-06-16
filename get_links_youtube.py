#!/usr/bin/env python3
"""
Extrae todos los links de videos de canales de YouTube listados en Canales.txt
y los guarda en Linksvideos.txt usando yt-dlp.

Requisitos:
    pip install yt-dlp

Uso:
    1. Crea un archivo Canales.txt en la misma carpeta con un link por línea.
    2. Ejecuta: python get_links_youtube.py
"""


import subprocess
import sys
import os
from datetime import datetime

CANALES_FILE = "Canales.txt"
LINKS_FILE = "Linksvideos.txt"


def verificar_ytdlp():
    """Verifica que yt-dlp esté instalado."""
    try:
        resultado = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True
        )
        version = resultado.stdout.strip() or resultado.stderr.strip()
        if version:
            print(f"✅ yt-dlp versión: {version}")
    except FileNotFoundError:
        print("❌ yt-dlp no está instalado.")
        print("   Instalalo con: pip install yt-dlp")
        sys.exit(1)


def leer_canales(filepath):
    """Lee el archivo de canales y devuelve una lista de URLs válidas."""
    if not os.path.exists(filepath):
        print(f"❌ No se encontró el archivo '{filepath}'.")
        print(f"   Crea '{filepath}' con un link de YouTube por línea.")
        sys.exit(1)

    canales = []
    with open(filepath, "r", encoding="utf-8") as f:
        for linea in f:
            url = linea.strip()
            if url and not url.startswith("#"):
                canales.append(url)

    if not canales:
        print(f"❌ El archivo '{filepath}' está vacío o solo tiene comentarios.")
        sys.exit(1)

    return canales


def extraer_links_canal(url):
    """
    Usa yt-dlp para extraer todos los links de videos y lives de un canal.
    Retorna una lista de URLs.
    """
    print(f"\n📡 Procesando: {url}")
    print("   (Esto puede tardar unos minutos según el tamaño del canal...)")

    # Normalizar la URL: si apunta a /videos, usamos la URL base del canal
    # yt-dlp extrae mejor con la URL base + tabs explícitas
    url_base = url.replace("/videos", "").replace("/live", "").rstrip("/")

    links = []

    # Intentar extraer videos regulares y lives por separado
    tabs = [
        (f"{url_base}/videos", "videos"),
        (f"{url_base}/streams", "lives/streams"),
    ]

    for tab_url, tipo in tabs:
        print(f"   🔍 Buscando {tipo}...")
        comando = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "url",
            "--no-warnings",
            "--ignore-errors",
            tab_url
        ]

        try:
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                encoding="utf-8"
            )

            encontrados = [
                linea.strip()
                for linea in resultado.stdout.splitlines()
                if linea.strip().startswith("http") and "youtube.com/watch" in linea
            ]

            print(f"      → {len(encontrados)} {tipo} encontrados")
            links.extend(encontrados)

            # Debug: mostrar stderr si no se encontró nada
            if not encontrados and resultado.stderr.strip():
                print(f"      ℹ️  {resultado.stderr.strip()[:200]}")

        except Exception as e:
            print(f"   ❌ Error en {tab_url}: {e}")

    # Eliminar duplicados manteniendo el orden
    vistos = set()
    links_unicos = []
    for l in links:
        if l not in vistos:
            vistos.add(l)
            links_unicos.append(l)

    return links_unicos


def guardar_links(links_por_canal, filepath):
    """Guarda todos los links en el archivo de salida."""
    links_existentes = set()
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for linea in f:
                l = linea.strip()
                if l and not l.startswith("#"):
                    links_existentes.add(l)
        print(f"\n📄 '{filepath}' ya existe con {len(links_existentes)} links.")

    nuevos_links = []
    for canal, links in links_por_canal.items():
        for link in links:
            if link not in links_existentes:
                nuevos_links.append(link)
                links_existentes.add(link)

    with open(filepath, "a", encoding="utf-8") as f:
        if nuevos_links:
            f.write(f"# Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            for link in nuevos_links:
                f.write(link + "\n")

    return len(nuevos_links)


def main():
    print("=" * 55)
    print("  Extractor de Links de YouTube con yt-dlp")
    print("=" * 55)

    verificar_ytdlp()

    canales = leer_canales(CANALES_FILE)
    print(f"\n✅ Se encontraron {len(canales)} canal(es) en '{CANALES_FILE}':")
    for c in canales:
        print(f"   • {c}")

    links_por_canal = {}
    total_encontrados = 0

    for canal in canales:
        links = extraer_links_canal(canal)
        links_por_canal[canal] = links
        total_encontrados += len(links)
        print(f"   ✅ Total del canal: {len(links)} videos/lives únicos")

    if total_encontrados == 0:
        print("\n⚠️  No se encontraron links.")
        print("   Verificá que las URLs en Canales.txt sean correctas.")
        print("   Ejemplo válido: https://www.youtube.com/@nombrecanal")
        sys.exit(0)

    nuevos = guardar_links(links_por_canal, LINKS_FILE)

    print("\n" + "=" * 55)
    print(f"  ✅ Proceso completado")
    print(f"  📊 Total encontrados : {total_encontrados}")
    print(f"  🆕 Nuevos agregados  : {nuevos}")
    print(f"  📁 Archivo de salida : {LINKS_FILE}")
    print("=" * 55)


if __name__ == "__main__":
    main()