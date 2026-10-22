#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from pathlib import Path

suite_dir = Path(__file__).resolve().parent
localapp = os.environ.get("LOCALAPPDATA", "")
iscc = Path(localapp) / "Programs" / "Inno Setup 6" / "ISCC.exe"
if not iscc.exists():
    iscc = Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "Inno Setup 6" / "ISCC.exe"

iss_file = suite_dir / "OmniSuite_Installer.iss"

print(f"Compilando instalador Inno Setup con: {iscc}...")
print(f"Archivo de configuración: {iss_file}")

res = subprocess.run([str(iscc), str(iss_file)], cwd=str(suite_dir))
if res.returncode == 0:
    print("\n[OK] Instalador de la Suite compilado exitosamente!")
else:
    print(f"\n[ERROR] Inno Setup falló con código {res.returncode}")
