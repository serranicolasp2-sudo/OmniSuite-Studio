#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ensamblar_suite_portable.py — Ensambla la versión portable del Hub y su documentación.
"""

import os
import shutil
import zipfile
from pathlib import Path

base_inst = Path(r"C:\Users\Nicolás\Desktop\Proyectos\APPS\Instaladores\00 OmniSuite Studio")
suite_src = Path(r"C:\Users\Nicolás\Desktop\Proyectos\APPS\OmniSuite Studio")

port_dir = base_inst / "Portable" / "OmniSuite Studio Portable"
port_dir.parent.mkdir(parents=True, exist_ok=True)
if port_dir.exists():
    shutil.rmtree(port_dir)

# Copiar ejecutable compilado del Hub
shutil.copytree(suite_src / "dist" / "OmniSuite Studio", port_dir)

# Copiar documentación
shutil.copy2(suite_src / "LEEME.md", base_inst / "LEEME.md")
shutil.copy2(suite_src / "INSTRUCTIVO.md", base_inst / "INSTRUCTIVO.md")
shutil.copy2(suite_src / "LEEME.md", port_dir / "LEEME.md")
shutil.copy2(suite_src / "INSTRUCTIVO.md", port_dir / "INSTRUCTIVO.md")

# Escribir LEEME PORTABLE.txt
leeme_port = """OmniSuite Studio — Centro de Control e Instalador Portable (100% Offline)
========================================================================
Diseño visual oficial de Tu Tiendita IA (sitio web: tutiendita-ia.store)

• Esta versión NO requiere instalación ni conexión a internet.
• Podés copiar esta carpeta a cualquier pendrive, disco externo o PC con Windows 10 u 11.
• Para iniciar: hacé doble clic en "OmniSuite Studio.exe".
• Consultá "LEEME.md" y "INSTRUCTIVO.md" para ver los flujos de trabajo detallados.

Características integradas:
- Interfaz gráfica oficial de Tu Tiendita IA (Modo Noche Tinta Studio).
- Menú interactivo con bordes redondeados y tarjetas de elevación.
- Instalador multiselección (All-in-One o por separado).
- Centro de control (Hub) para lanzar con un clic cualquiera de las 4 herramientas.
- Guías especializadas para animadores 3D, editores audiovisuales, CMs y podcasters.
"""

with open(port_dir / "LEEME PORTABLE.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write(leeme_port)

# Empaquetar zip portable del Hub
zip_path = base_inst / "Portable" / "OmniSuite Studio Portable.zip"
if zip_path.exists():
    zip_path.unlink()

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    for root, dirs, files in os.walk(port_dir):
        for f in files:
            full = Path(root) / f
            arc = full.relative_to(port_dir.parent)
            zf.write(full, arc)

print(f"[OK] Portable ensamblado con éxito! Zip: {zip_path.stat().st_size / (1024*1024):.1f} MB")
