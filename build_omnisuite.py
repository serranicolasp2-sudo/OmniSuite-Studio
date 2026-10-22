#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
from pathlib import Path

suite_dir = Path(__file__).resolve().parent
apps_dir = suite_dir.parent
venv_py = apps_dir / "Transcriptor" / "entorno" / "Scripts" / "python.exe"
python_exec = str(venv_py) if venv_py.exists() else sys.executable

cmd = [
    python_exec,
    "-m", "PyInstaller",
    "--noconsole",
    "--name", "OmniSuite Studio",
    "--icon", str(suite_dir / "iconos" / "omnisuite.ico"),
    "--add-data", f"{suite_dir / 'iconos'};iconos",
    "--add-data", f"{suite_dir / 'ui_theme.py'};.",
    "--distpath", str(suite_dir / "dist"),
    "--workpath", str(suite_dir / "build"),
    "--noconfirm",
    str(suite_dir / "app_omnisuite_hub.py")
]

print("Compilando OmniSuite Studio.exe con PyInstaller...")
res = subprocess.run(cmd, cwd=str(suite_dir))
if res.returncode == 0:
    print("[OK] PyInstaller completado exitosamente!")
else:
    print("[ERROR] Fallo la compilacion con PyInstaller.")
