#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OmniSuite Studio — Centro de Control e Instalador Interactivo Multiapp
Diseño: Premium Minimalista "Tu Tiendita IA" (https://tutiendita-ia.store)
Orientado a: Creadores de Contenido, Animadores 3D, Editores Audiovisuales, Productores y CMs.
"""

import os
import sys
import subprocess
import threading
import queue
import time
import webbrowser
import shutil
import zipfile
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.scrolledtext as scrolledtext
from PIL import Image, ImageTk

CURRENT_DIR = Path(__file__).resolve().parent
APPS_DIR = CURRENT_DIR.parent
if str(APPS_DIR) not in sys.path:
    sys.path.insert(0, str(APPS_DIR))
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from ui_theme import (
    COLOR_BIROME, COLOR_BIROME_HOVER, COLOR_TINTA, COLOR_MALVON, COLOR_MALVON_HOVER,
    COLOR_YEMA, COLOR_CINTA, COLOR_PAPEL, COLOR_PLATA, COLOR_PERIWINKLE,
    BG_APP, BG_CARD, CHIP_BG, CHIP_BORDER, BG_CARD_BORDER, BG_INPUT, BG_INPUT_BORDER,
    BG_CONSOLE, BG_CONSOLE_BORDER, TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    FONT_HERO, FONT_TITLE, FONT_SUB, FONT_LABEL, FONT_BODY, FONT_MONO, FONT_BTN, FONT_BADGE,
    setup_app_theme, PillBadge, PillButton, RoundedCard, SegmentedSwitch, create_header,
    load_icon_image
)

BRAND_URL = "https://tutiendita-ia.store"
INSTALADORES_DIR = APPS_DIR / "Instaladores"


class OmniSuiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OmniSuite Studio — Tu Tiendita IA (Edición Creadores)")
        self.root.geometry("980x920")
        self.root.minsize(900, 780)
        self.root.configure(bg=BG_APP)

        self.msg_queue = queue.Queue()
        self.is_installing = False
        self.current_tab_idx = 0

        # Configurar icono y estilo visual
        setup_app_theme(self.root, app_icon="omnisuite")

        # Variables de selección de apps
        self.sel_boost = tk.BooleanVar(value=True)
        self.sel_flow = tk.BooleanVar(value=True)
        self.sel_scale = tk.BooleanVar(value=True)
        self.sel_transcriptor = tk.BooleanVar(value=True)

        # Variables de instalación
        self.install_mode = tk.StringVar(value="portable")  # 'system' o 'portable'
        default_inst_path = str(Path(os.environ.get("LOCALAPPDATA", "C:")) / "Programs" / "Tu Tiendita IA" / "OmniSuite Studio")
        default_port_path = str(APPS_DIR / "OmniSuite Portable")
        self.dest_path_var = tk.StringVar(value=default_port_path)
        self.create_desktop_lnk = tk.BooleanVar(value=True)
        self.create_startmenu_lnk = tk.BooleanVar(value=True)

        self.status_var = tk.StringVar(value="Listo para instalar o gestionar tus aplicaciones.")
        self.progress_val = tk.DoubleVar(value=0.0)

        # Construir interfaz
        self._build_header()
        self._build_tabs()
        self._build_tab_installer()
        self._build_tab_hub()
        self._build_tab_creators_guide()
        self._build_footer()

        # Iniciar despachador de mensajes
        self.root.after(100, self._process_queue)

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=BG_APP, padx=22, pady=(14, 6))
        hdr.pack(fill="x")

        # Icono a la izquierda
        ico_img = load_icon_image("omnisuite", 56)
        if ico_img:
            lbl_ico = tk.Label(hdr, image=ico_img, bg=BG_APP)
            lbl_ico.image = ico_img
            lbl_ico.pack(side="left", padx=(0, 16))

        # Textos de título
        t_box = tk.Frame(hdr, bg=BG_APP)
        t_box.pack(side="left", fill="y")

        top_line = tk.Frame(t_box, bg=BG_APP)
        top_line.pack(anchor="w")

        tk.Label(
            top_line,
            text="OmniSuite Studio",
            font=("Segoe UI Variable Display", 21, "bold"),
            fg=TEXT_MAIN,
            bg=BG_APP
        ).pack(side="left", padx=(0, 10))

        PillBadge(top_line, "EDICIÓN CREADORES", bg_color=COLOR_YEMA, fg_color=COLOR_CINTA, font=FONT_BADGE).pack(side="left", padx=4)
        PillBadge(top_line, "ALL-IN-ONE", bg_color=CHIP_BG, fg_color=COLOR_PERIWINKLE, border_color=CHIP_BORDER).pack(side="left", padx=4)

        sub_text = "Suite Audiovisual & IA para Creadores, Animadores 3D, Editores y CMs · 100% Offline"
        tk.Label(t_box, text=sub_text, font=FONT_SUB, fg=TEXT_MUTED, bg=BG_APP).pack(anchor="w", pady=(2, 0))

        # Enlace a la tienda a la derecha
        r_box = tk.Frame(hdr, bg=BG_APP)
        r_box.pack(side="right", fill="y", padx=(10, 0))

        btn_web = tk.Button(
            r_box,
            text="🌐 tutiendita-ia.store",
            font=("Segoe UI Semibold", 10, "underline"),
            bg=CHIP_BG,
            fg=COLOR_PERIWINKLE,
            activebackground=COLOR_BIROME,
            activeforeground=COLOR_PAPEL,
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: webbrowser.open(BRAND_URL)
        )
        btn_web.pack(side="top", anchor="e")

        tk.Label(r_box, text="Marca Oficial: Tu Tiendita IA", font=("Segoe UI", 9), fg=TEXT_DIM, bg=BG_APP).pack(side="top", anchor="e", pady=(2, 0))

        # Separador estilizado de marca (filete Birome/Yema)
        sep_f = tk.Frame(self.root, bg=BG_APP, height=2)
        sep_f.pack(fill="x", padx=22, pady=(4, 8))
        tk.Frame(sep_f, bg=COLOR_BIROME, height=2, width=120).pack(side="left")
        tk.Frame(sep_f, bg=COLOR_YEMA, height=2, width=80).pack(side="left")
        tk.Frame(sep_f, bg=COLOR_MALVON, height=2, width=50).pack(side="left")
        tk.Frame(sep_f, bg=BG_CARD_BORDER, height=1).pack(side="left", fill="x", expand=True)

    def _build_tabs(self):
        tab_box = tk.Frame(self.root, bg=BG_APP, padx=22, pady=(0, 6))
        tab_box.pack(fill="x")

        self.tab_switch = SegmentedSwitch(
            tab_box,
            segments=["📦 Instalador Multiapp", "🎛️ Centro de Control (Hub)", "💡 Guía para Creadores"],
            initial_idx=0,
            command=self._on_tab_change
        )
        self.tab_switch.pack(anchor="w")

        # Contenedor para las páginas
        self.page_container = tk.Frame(self.root, bg=BG_APP, padx=22)
        self.page_container.pack(fill="both", expand=True)

        self.pages = []

    def _on_tab_change(self, idx):
        self.current_tab_idx = idx
        for i, page in enumerate(self.pages):
            if i == idx:
                page.pack(fill="both", expand=True)
            else:
                page.pack_forget()

    # =========================================================================
    # PESTAÑA 1: INSTALADOR MULTIAPP (ALL IN ONE O POR SEPARADO)
    # =========================================================================
    def _build_tab_installer(self):
        page = tk.Frame(self.page_container, bg=BG_APP)
        self.pages.append(page)
        page.pack(fill="both", expand=True)

        # 1. Barra de Selección Rápida
        top_bar = tk.Frame(page, bg=BG_APP)
        top_bar.pack(fill="x", pady=(4, 8))

        tk.Label(top_bar, text="Seleccioná las aplicaciones a instalar:", font=FONT_TITLE, fg=TEXT_MAIN, bg=BG_APP).pack(side="left")

        btn_box = tk.Frame(top_bar, bg=BG_APP)
        btn_box.pack(side="right")

        tk.Button(
            btn_box, text="✨ Seleccionar Todo (All in One)", font=("Segoe UI Semibold", 9),
            bg=COLOR_BIROME, fg=COLOR_PAPEL, activebackground=COLOR_BIROME_HOVER, relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
            command=self._select_all
        ).pack(side="left", padx=4)

        tk.Button(
            btn_box, text="🎬 Solo Video Tools", font=("Segoe UI Semibold", 9),
            bg=CHIP_BG, fg=TEXT_MAIN, activebackground=COLOR_BIROME, relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
            command=self._select_video_only
        ).pack(side="left", padx=4)

        tk.Button(
            btn_box, text="🧹 Deseleccionar", font=("Segoe UI", 9),
            bg=CHIP_BG, fg=TEXT_MUTED, activebackground=BG_CARD_BORDER, relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
            command=self._deselect_all
        ).pack(side="left", padx=4)

        # 2. Tarjetas de las 4 Apps
        cards_frame = tk.Frame(page, bg=BG_APP)
        cards_frame.pack(fill="both", expand=True, pady=(0, 6))

        # Configurar 4 filas para las apps
        cards_frame.columnconfigure(0, weight=1)

        self._build_app_card(
            cards_frame, row=0,
            title="OmniBoost Studio — Video Booster Ultra",
            badge="🎬 PARA EDITORES & ANIMADORES 3D",
            badge_color=COLOR_BIROME,
            desc="Restaura nitidez con FidelityFX CAS, remueve banding en cielos/fondos de IA (Kling/Runway/Sora), denoise inteligente y realce de rango dinámico sin quemar luces.",
            size_str="~135 MB · Aceleración RTX NVENC p7 & AMD AMF",
            var=self.sel_boost,
            icon_key="omniboost"
        )

        self._build_app_card(
            cards_frame, row=1,
            title="OmniFlow FPS Booster — Interpolación HFR",
            badge="⚡ FLUIDEZ 60 / 120 FPS & SLOW-MOTION",
            badge_color=COLOR_MALVON,
            desc="Multiplica la fluidez de renders 3D (Pixar/CGI) y tomas a 24/30 fps mediante flujo óptico bidireccional. Elimina judder en paneos y morphing en animación 2D.",
            size_str="~135 MB · Flujo Óptico Adaptativo & NVENC",
            var=self.sel_flow,
            icon_key="omniflow"
        )

        self._build_app_card(
            cards_frame, row=2,
            title="OmniScale Studio — Upscaler 1080p / 2K / 4K",
            badge="📱 REELS / TIKTOK / SHORTS (9:16 VERTICAL)",
            badge_color=COLOR_YEMA,
            badge_fg=COLOR_CINTA,
            desc="Reescalado inteligente Lanczos con preservación de grano fílmico y detección automática de orientación (16:9 horizontal, 9:16 móvil vertical o 1:1 cuadrado).",
            size_str="~135 MB · Lanczos + FidelityFX CAS",
            var=self.sel_scale,
            icon_key="omniscale"
        )

        self._build_app_card(
            cards_frame, row=3,
            title="Transcriptor Local — Diarización 4 Hablantes",
            badge="🎙️ PODCASTS, ENTREVISTAS & SUBTÍTULOS",
            badge_color=COLOR_PERIWINKLE,
            badge_fg=COLOR_TINTA,
            desc="Whisper large-v3-turbo y Pyannote Audio 3.1. Reconoce quién habla, genera subtítulos .SRT sincronizados, informes .DOCX y permite editar segmentos con reproductor.",
            size_str="~1.77 GB · Modelos Locales 100% Offline",
            var=self.sel_transcriptor,
            icon_key="transcriptor"
        )

        # 3. Opciones de Instalación (Destino, Tipo y Accesos directos)
        opt_card = RoundedCard(page, bg_color=BG_CARD, border_color=BG_CARD_BORDER)
        opt_card.pack(fill="x", pady=6)
        opt_f = opt_card.body

        r1 = tk.Frame(opt_f, bg=BG_CARD)
        r1.pack(fill="x", pady=2)

        tk.Label(r1, text="Modalidad de Despliegue:", font=FONT_LABEL, fg=TEXT_MUTED, bg=BG_CARD).pack(side="left", padx=(0, 10))

        tk.Radiobutton(
            r1, text="💼 Despliegue Portable (Pendrive / Carpeta Autónoma)", variable=self.install_mode, value="portable",
            font=FONT_BODY, fg=TEXT_MAIN, bg=BG_CARD, selectcolor=COLOR_TINTA, activebackground=BG_CARD, activeforeground=TEXT_MAIN,
            command=self._on_mode_change
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            r1, text="🚀 Instalación en Sistema (Programas de Windows)", variable=self.install_mode, value="system",
            font=FONT_BODY, fg=TEXT_MAIN, bg=BG_CARD, selectcolor=COLOR_TINTA, activebackground=BG_CARD, activeforeground=TEXT_MAIN,
            command=self._on_mode_change
        ).pack(side="left", padx=10)

        # Ruta destino
        r2 = tk.Frame(opt_f, bg=BG_CARD)
        r2.pack(fill="x", pady=(6, 2))

        tk.Label(r2, text="Carpeta Destino:", font=FONT_LABEL, fg=TEXT_MUTED, bg=BG_CARD).pack(side="left", padx=(0, 10))
        self.entry_dest = tk.Entry(r2, textvariable=self.dest_path_var, font=FONT_BODY, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat", bd=1)
        self.entry_dest.pack(side="left", fill="x", expand=True, padx=4)

        tk.Button(
            r2, text="Examinar...", font=("Segoe UI", 9), bg=CHIP_BG, fg=TEXT_MAIN, activebackground=COLOR_BIROME,
            relief="flat", bd=0, padx=12, pady=3, cursor="hand2", command=self._browse_dest
        ).pack(side="left", padx=(4, 0))

        # Checkboxes de accesos directos
        r3 = tk.Frame(opt_f, bg=BG_CARD)
        r3.pack(fill="x", pady=(4, 0))

        tk.Checkbutton(
            r3, text="Crear accesos directos en el Escritorio", variable=self.create_desktop_lnk,
            font=FONT_BODY, fg=TEXT_MAIN, bg=BG_CARD, selectcolor=COLOR_TINTA, activebackground=BG_CARD, activeforeground=TEXT_MAIN
        ).pack(side="left", padx=(0, 20))

        tk.Checkbutton(
            r3, text="Registrar en el Menú Inicio (Tu Tiendita IA - OmniSuite)", variable=self.create_startmenu_lnk,
            font=FONT_BODY, fg=TEXT_MAIN, bg=BG_CARD, selectcolor=COLOR_TINTA, activebackground=BG_CARD, activeforeground=TEXT_MAIN
        ).pack(side="left")

        # 4. Botón de Acción Principal y Progreso
        action_box = tk.Frame(page, bg=BG_APP)
        action_box.pack(fill="x", pady=(6, 4))

        self.btn_install = tk.Button(
            action_box,
            text="🚀 Iniciar Instalación / Despliegue de la Suite",
            font=("Segoe UI Variable Display", 13, "bold"),
            bg=COLOR_YEMA,
            fg=COLOR_CINTA,
            activebackground="#FFDD66",
            activeforeground=COLOR_CINTA,
            relief="flat",
            bd=0,
            padx=24,
            pady=10,
            cursor="hand2",
            command=self._start_installation
        )
        self.btn_install.pack(fill="x", pady=(0, 6))

        # Barra de progreso y estado
        prog_f = tk.Frame(page, bg=BG_APP)
        prog_f.pack(fill="x", pady=(0, 4))

        tk.Label(prog_f, textvariable=self.status_var, font=FONT_LABEL, fg=TEXT_MUTED, bg=BG_APP).pack(anchor="w", pady=(0, 2))

        self.progress_bar = ttk.Progressbar(prog_f, variable=self.progress_val, maximum=100)
        self.progress_bar.pack(fill="x")

        # Consola de log colapsable
        self.log_text = scrolledtext.ScrolledText(page, height=4, font=FONT_MONO, bg=BG_CONSOLE, fg=TEXT_MUTED, relief="flat", bd=1)
        self.log_text.pack(fill="x", pady=(4, 0))
        self._log("OmniSuite Studio inicializado. Seleccioná las herramientas que deseás instalar y presioná 'Iniciar'.")

    def _build_app_card(self, parent, row, title, badge, badge_color, desc, size_str, var, icon_key, badge_fg=COLOR_PAPEL):
        card = RoundedCard(parent, bg_color=BG_CARD, border_color=BG_CARD_BORDER)
        card.grid(row=row, column=0, sticky="nsew", pady=3)
        b = card.body

        # Checkbox grande
        chk = tk.Checkbutton(
            b, variable=var, bg=BG_CARD, activebackground=BG_CARD, selectcolor=COLOR_TINTA,
            relief="flat", bd=0, cursor="hand2"
        )
        chk.pack(side="left", padx=(0, 8))

        # Icono de la app
        ico_img = load_icon_image(icon_key, 46)
        if ico_img:
            lbl_ico = tk.Label(b, image=ico_img, bg=BG_CARD, cursor="hand2")
            lbl_ico.image = ico_img
            lbl_ico.pack(side="left", padx=(0, 12))
            lbl_ico.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))

        # Contenido textual
        mid = tk.Frame(b, bg=BG_CARD)
        mid.pack(side="left", fill="both", expand=True)

        t_row = tk.Frame(mid, bg=BG_CARD)
        t_row.pack(anchor="w")

        lbl_t = tk.Label(t_row, text=title, font=("Segoe UI Semibold", 12), fg=TEXT_MAIN, bg=BG_CARD, cursor="hand2")
        lbl_t.pack(side="left", padx=(0, 8))
        lbl_t.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))

        PillBadge(t_row, badge, bg_color=badge_color, fg_color=badge_fg, font=("Segoe UI Bold", 8)).pack(side="left")

        tk.Label(mid, text=desc, font=FONT_BODY, fg=TEXT_MUTED, bg=BG_CARD, wraplength=590, justify="left").pack(anchor="w", pady=(1, 1))

        # Tamaño y estado a la derecha
        r_f = tk.Frame(b, bg=BG_CARD)
        r_f.pack(side="right", padx=(8, 0))

        tk.Label(r_f, text=size_str, font=("Segoe UI", 9), fg=TEXT_DIM, bg=BG_CARD).pack(anchor="e")

    # =========================================================================
    # PESTAÑA 2: CENTRO DE CONTROL (HUB)
    # =========================================================================
    def _build_tab_hub(self):
        page = tk.Frame(self.page_container, bg=BG_APP)
        self.pages.append(page)

        hdr_hub = tk.Frame(page, bg=BG_APP)
        hdr_hub.pack(fill="x", pady=(6, 8))

        tk.Label(hdr_hub, text="Tus Herramientas de Creación Audiovisual", font=FONT_TITLE, fg=TEXT_MAIN, bg=BG_APP).pack(side="left")
        tk.Label(hdr_hub, text="Hacé clic en 'Lanzar' para abrir cualquier aplicación directamente.", font=FONT_SUB, fg=TEXT_MUTED, bg=BG_APP).pack(side="right")

        hub_list = [
            (
                "OmniBoost Studio",
                "Video Booster Ultra & Restauración",
                "🎬 Cine, animación 3D, CGI y tomas de IA.",
                "Video Booster",
                "OmniBoost Studio.exe",
                ["Lanzar OmniBoost.bat", "Lanzar Video Booster.bat"],
                "app_video_booster.py",
                "omniboost"
            ),
            (
                "OmniFlow FPS Booster",
                "Interpolador de Cuadros 60 / 120 FPS",
                "⚡ Máxima fluidez sin judder ni distorsión.",
                "FPS Booster 60fps",
                "OmniFlow FPS Booster.exe",
                ["Lanzar OmniFlow.bat", "Lanzar FPS Booster.bat", "Lanzar FPS Booster 60fps.bat"],
                "app_fps_booster.py",
                "omniflow"
            ),
            (
                "OmniScale Studio",
                "Upscaler Universal 1080p / 2K / 4K",
                "📱 Adaptativo 9:16 vertical para Reels, TikTok y 16:9.",
                "Upscaler 1080p",
                "OmniScale Studio.exe",
                ["Lanzar OmniScale.bat", "Lanzar Upscaler 1080p.bat"],
                "app_upscaler.py",
                "omniscale"
            ),
            (
                "Transcriptor Local",
                "Diarización de 4 Hablantes & Whisper",
                "🎙️ Subtítulos .SRT, informes .DOCX y editor de audio.",
                "Transcriptor",
                "Transcriptor.exe",
                ["Lanzar Transcriptor.bat", "transcribir.bat"],
                "main.py",
                "transcriptor"
            ),
        ]

        for title, sub, target_desc, folder_name, exe_name, bat_names, py_name, ico_key in hub_list:
            c = RoundedCard(page, bg_color=BG_CARD, border_color=BG_CARD_BORDER)
            c.pack(fill="x", pady=5)
            b = c.body

            ico = load_icon_image(ico_key, 46)
            if ico:
                lbl = tk.Label(b, image=ico, bg=BG_CARD)
                lbl.image = ico
                lbl.pack(side="left", padx=(0, 14))

            m = tk.Frame(b, bg=BG_CARD)
            m.pack(side="left", fill="both", expand=True)

            tk.Label(m, text=title, font=("Segoe UI Semibold", 13), fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w")
            tk.Label(m, text=sub, font=("Segoe UI", 10, "italic"), fg=COLOR_PERIWINKLE, bg=BG_CARD).pack(anchor="w")
            tk.Label(m, text=target_desc, font=FONT_BODY, fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(2, 0))

            btn_box = tk.Frame(b, bg=BG_CARD)
            btn_box.pack(side="right")

            app_folder = APPS_DIR / folder_name
            if not app_folder.exists():
                app_folder = CURRENT_DIR.parent / folder_name

            tk.Button(
                btn_box, text="📂 Carpeta", font=("Segoe UI", 9), bg=CHIP_BG, fg=TEXT_MAIN,
                relief="flat", bd=0, padx=10, pady=5, cursor="hand2",
                command=lambda p=app_folder: os.startfile(p) if p.exists() else messagebox.showwarning("Aviso", f"No se encontró la carpeta:\n{p}")
            ).pack(side="left", padx=4)

            tk.Button(
                btn_box, text="📖 LEEME", font=("Segoe UI", 9), bg=CHIP_BG, fg=TEXT_MAIN,
                relief="flat", bd=0, padx=10, pady=5, cursor="hand2",
                command=lambda p=app_folder / "LEEME.md": os.startfile(p) if p.exists() else messagebox.showwarning("Aviso", "No se encontró el LEEME.md")
            ).pack(side="left", padx=4)

            tk.Button(
                btn_box, text="▶ Iniciar", font=("Segoe UI Semibold", 10), bg=COLOR_BIROME, fg=COLOR_PAPEL,
                activebackground=COLOR_BIROME_HOVER, relief="flat", bd=0, padx=16, pady=5, cursor="hand2",
                command=lambda t=title, fn=folder_name, en=exe_name, bn=bat_names, pn=py_name: self._launch_app(t, fn, en, bn, pn)
            ).pack(side="left", padx=(4, 0))

    # =========================================================================
    # PESTAÑA 3: GUÍA PARA CREADORES & WORKFLOWS
    # =========================================================================
    def _build_tab_creators_guide(self):
        page = tk.Frame(self.page_container, bg=BG_APP)
        self.pages.append(page)

        txt = scrolledtext.ScrolledText(page, font=("Segoe UI", 10), bg=BG_CARD, fg=TEXT_MAIN, relief="flat", bd=1, padx=16, pady=14)
        txt.pack(fill="both", expand=True, pady=6)

        guide_content = """💡 GUÍA DE PRODUCCIÓN PARA CREADORES — OMNISUITE STUDIO
================================================================================
Desarrollado para la comunidad de Tu Tiendita IA (sitio web: tutiendita-ia.store)

Esta suite fue concebida para potenciar los cuatro pilares fundamentales del contenido moderno:

--------------------------------------------------------------------------------
1. ANIMADORES 3D & DISEÑADORES CGI (Pixar / Unreal Engine / Blender)
--------------------------------------------------------------------------------
• El Desafío: Renders pesados de 24 fps que tardan horas en computar cada cuadro adicional.
• El Flujo Recomendado:
  1. Renderizá tu animación en 1080p a 24 fps para ahorrar entre 60% y 80% de tiempo de render 3D.
  2. Pasalo por OmniBoost Studio con el perfil "Animación 3D & CGI": resaltará la iluminación volumétrica y limpiará el ruido de muestreo.
  3. Ejecutá OmniFlow FPS Booster con el método "Universal Adaptativo" a 60 FPS o 120 FPS. Obtendrás una animación con fluidez de película Pixar sin tiempos de render prohibitivos.

--------------------------------------------------------------------------------
2. COMMUNITY MANAGERS (CMs) & CREADORES DE REELS / TIKTOK / SHORTS
--------------------------------------------------------------------------------
• El Desafío: Videos horizontales o de baja calidad que deben adaptarse al formato vertical 9:16 y subtitularse al instante para no perder retención.
• El Flujo Recomendado:
  1. Utilizá OmniScale Studio con resolución "Auto-Adaptativo 1080p" o "1080x1920 (9:16 Vertical)": escala tu video con nitidez Lanczos sin deformar ni aplastar caras.
  2. Subí el clip a Transcriptor Local: Whisper large-v3-turbo extraerá los subtítulos con puntuación perfecta y generará el archivo .SRT sincronizado al milisegundo.
  3. Importá el .SRT en Premiere, CapCut o DaVinci Resolve para quemar subtítulos dinámicos de alta conversión.

--------------------------------------------------------------------------------
3. EDITORES AUDIOVISUALES & CINEASTAS (DaVinci Resolve / Premiere Pro)
--------------------------------------------------------------------------------
• El Desafío: Material comprimido de drones o smartphones con banding severo y pérdida de microtexturas.
• El Flujo Recomendado:
  1. Procesá tus planos en OmniBoost Studio con el perfil "Cine & Películas Reales": el algoritmo CAS resaltará poros, telas y detalles sin crear halos falsos, protegiendo el grano orgánico de 35mm.
  2. Si el material proviene de IA (Kling, Runway, Sora), usá el perfil "Videos de IA": el filtro de de-banding (gradfun) eliminará los escalones de color en degradados y cielos.

--------------------------------------------------------------------------------
4. PODCASTERS, PERIODISTAS & PRODUCTORES DE ENTREVISTAS
--------------------------------------------------------------------------------
• El Desafío: Grabar entrevistas largas con múltiples participantes y transcribirlas a mano o pagar suscripciones caras por minuto que suben audios privados a la nube.
• El Flujo Recomendado:
  1. Ingresá el audio o video en Transcriptor Local.
  2. Asigná los nombres de hasta 4 participantes (con sus colores Birome, Malvón, Yema y Celeste).
  3. En minutos tendrás un informe profesional en Word (.DOCX) listo para entregar a clientes, y un visor donde podés reproducir y corregir cada fragmento con un solo clic.

================================================================================
"""
        txt.insert("1.0", guide_content)
        txt.configure(state="disabled")

    def _build_footer(self):
        ftr = tk.Frame(self.root, bg=BG_APP, padx=22, pady=(6, 12))
        ftr.pack(fill="x")

        tk.Label(
            ftr,
            text="Tu Tiendita IA © 2026 · Ecosistema Creativo Multiapp · Todos los derechos reservados",
            font=("Segoe UI", 9),
            fg=TEXT_DIM,
            bg=BG_APP
        ).pack(side="left")

        link = tk.Label(
            ftr,
            text="Visitar Tienda Oficial: tutiendita-ia.store ↗",
            font=("Segoe UI Semibold", 9, "underline"),
            fg=COLOR_PERIWINKLE,
            bg=BG_APP,
            cursor="hand2"
        )
        link.pack(side="right")
        link.bind("<Button-1>", lambda e: webbrowser.open(BRAND_URL))

    # =========================================================================
    # LÓGICA DE CONTROL Y EVENTOS
    # =========================================================================
    def _select_all(self):
        self.sel_boost.set(True)
        self.sel_flow.set(True)
        self.sel_scale.set(True)
        self.sel_transcriptor.set(True)

    def _select_video_only(self):
        self.sel_boost.set(True)
        self.sel_flow.set(True)
        self.sel_scale.set(True)
        self.sel_transcriptor.set(False)

    def _deselect_all(self):
        self.sel_boost.set(False)
        self.sel_flow.set(False)
        self.sel_scale.set(False)
        self.sel_transcriptor.set(False)

    def _on_mode_change(self):
        mode = self.install_mode.get()
        if mode == "system":
            default_p = str(Path(os.environ.get("LOCALAPPDATA", "C:")) / "Programs" / "Tu Tiendita IA" / "OmniSuite Studio")
        else:
            default_p = str(APPS_DIR / "OmniSuite Portable")
        self.dest_path_var.set(default_p)

    def _browse_dest(self):
        d = filedialog.askdirectory(initialdir=self.dest_path_var.get(), title="Seleccionar Carpeta de Destino")
        if d:
            self.dest_path_var.set(d)

    def _launch_app(self, title: str, folder_name: str, exe_name: str, bat_names: list, py_name: str):
        """
        Lanza la aplicación seleccionada con fallback en cascada:
        1. Ejecutable compilado (.exe) en modo instalado o portable.
        2. Lanzador por lotes (.bat) en modo desarrollo local.
        3. Script directo (.py) ejecutado con el intérprete Python correspondiente.
        """
        # Directorios candidatos donde puede residir la aplicación
        candidate_dirs = [
            CURRENT_DIR / folder_name,
            CURRENT_DIR.parent / folder_name,
            APPS_DIR / folder_name,
        ]
        if getattr(sys, "frozen", False):
            candidate_dirs.insert(0, Path(sys.executable).parent / folder_name)
            candidate_dirs.insert(1, Path(sys.executable).parent)

        target_dir = None
        for d in candidate_dirs:
            if d.exists() and d.is_dir():
                target_dir = d
                break

        if not target_dir:
            target_dir = CURRENT_DIR.parent / folder_name

        # 1. Buscar ejecutable compilado (.exe)
        exe_candidates = [
            target_dir / exe_name,
            target_dir / "dist" / exe_name,
            target_dir / folder_name / exe_name,
        ]
        for ec in exe_candidates:
            if ec.exists():
                try:
                    subprocess.Popen([str(ec)], cwd=str(ec.parent))
                    self._log(f"Iniciando ejecutable: {ec.name}...")
                    return
                except Exception as e:
                    self._log(f"Aviso al iniciar {ec.name}: {e}")

        # 2. Buscar lanzador .bat
        for bn in bat_names:
            bp = target_dir / bn
            if bp.exists():
                try:
                    subprocess.Popen([str(bp)], shell=True, cwd=str(target_dir))
                    self._log(f"Iniciando lanzador por lotes: {bn}...")
                    return
                except Exception as e:
                    self._log(f"Aviso al iniciar {bn}: {e}")

        # 3. Buscar script .py directo
        py_path = target_dir / py_name
        if py_path.exists():
            # Buscar si el subproyecto tiene su propio entorno virtual
            venv_python = target_dir / "entorno" / "Scripts" / "python.exe"
            python_exec = str(venv_python) if venv_python.exists() else sys.executable
            try:
                subprocess.Popen([python_exec, str(py_path)], cwd=str(target_dir))
                self._log(f"Iniciando script Python: {py_name} con {Path(python_exec).name}...")
                return
            except Exception as e:
                self._log(f"Error al iniciar {py_name}: {e}")

        messagebox.showerror(
            "Lanzador No Encontrado",
            f"No se pudo localizar el ejecutable (.exe), script (.bat) ni fuente ({py_name}) para {title}.\n\n"
            f"Carpeta inspeccionada:\n{target_dir}"
        )

    def _log(self, msg: str):
        self.msg_queue.put(("log", msg))

    def _process_queue(self):
        try:
            while not self.msg_queue.empty():
                m_type, val = self.msg_queue.get_nowait()
                if m_type == "log":
                    self.log_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {val}\n")
                    self.log_text.see("end")
                elif m_type == "status":
                    self.status_var.set(val)
                elif m_type == "progress":
                    self.progress_val.set(val)
                elif m_type == "done":
                    self._on_install_completed(val)
        finally:
            self.root.after(100, self._process_queue)

    def _start_installation(self):
        selected = []
        if self.sel_boost.get():
            selected.append("OmniBoost Studio")
        if self.sel_flow.get():
            selected.append("OmniFlow FPS Booster")
        if self.sel_scale.get():
            selected.append("OmniScale Studio")
        if self.sel_transcriptor.get():
            selected.append("Transcriptor Local")

        if not selected:
            messagebox.showwarning("Atención", "Por favor seleccioná al menos una aplicación para instalar.")
            return

        dest = Path(self.dest_path_var.get().strip())
        if not dest:
            messagebox.showwarning("Atención", "Por favor indicá la carpeta de destino.")
            return

        mode = self.install_mode.get()
        confirm = messagebox.askyesno(
            "Confirmar Instalación",
            f"Se van a desplegar {len(selected)} aplicaciones en modo {mode.upper()}:\n\n" +
            "\n".join([f"• {s}" for s in selected]) +
            f"\n\nDestino:\n{dest}\n\n¿Deseás continuar?"
        )
        if not confirm:
            return

        self.is_installing = True
        self.btn_install.configure(state="disabled", text="⏳ Desplegando Aplicaciones...")
        self.progress_val.set(5.0)
        self.status_var.set("Preparando entorno de instalación...")

        threading.Thread(target=self._worker_install, args=(selected, dest, mode), daemon=True).start()

    def _worker_install(self, selected_apps, dest_dir: Path, mode: str):
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            self._log(f"Carpeta destino confirmada: {dest_dir}")

            total_steps = len(selected_apps) * 2 + 1
            curr_step = 0

            # Mapeo de paquetes
            pkg_info = {
                "OmniBoost Studio": {
                    "inst_exe": INSTALADORES_DIR / "01 Video Booster" / "Instalador" / "OmniBoost Studio Instalador 1.0.exe",
                    "portable_zip": INSTALADORES_DIR / "01 Video Booster" / "Portable" / "OmniBoost Studio Portable.zip",
                    "portable_folder": INSTALADORES_DIR / "01 Video Booster" / "Portable" / "OmniBoost Studio Portable",
                    "exe_name": "OmniBoost Studio.exe",
                    "ico": APPS_DIR / "iconos" / "omniboost.ico"
                },
                "OmniFlow FPS Booster": {
                    "inst_exe": INSTALADORES_DIR / "02 FPS Booster" / "Instalador" / "OmniFlow FPS Booster Instalador 1.0.exe",
                    "portable_zip": INSTALADORES_DIR / "02 FPS Booster" / "Portable" / "OmniFlow FPS Booster Portable.zip",
                    "portable_folder": INSTALADORES_DIR / "02 FPS Booster" / "Portable" / "OmniFlow FPS Booster Portable",
                    "exe_name": "OmniFlow FPS Booster.exe",
                    "ico": APPS_DIR / "iconos" / "omniflow.ico"
                },
                "OmniScale Studio": {
                    "inst_exe": INSTALADORES_DIR / "03 Upscaler" / "Instalador" / "OmniScale Studio Instalador 1.0.exe",
                    "portable_zip": INSTALADORES_DIR / "03 Upscaler" / "Portable" / "OmniScale Studio Portable.zip",
                    "portable_folder": INSTALADORES_DIR / "03 Upscaler" / "Portable" / "OmniScale Studio Portable",
                    "exe_name": "OmniScale Studio.exe",
                    "ico": APPS_DIR / "iconos" / "omniscale.ico"
                },
                "Transcriptor Local": {
                    "inst_exe": INSTALADORES_DIR / "04 Transcriptor" / "Instalador" / "Transcriptor Instalador 1.0.exe",
                    "portable_zip": INSTALADORES_DIR / "04 Transcriptor" / "Portable" / "Transcriptor Portable.zip",
                    "portable_folder": INSTALADORES_DIR / "04 Transcriptor" / "Portable" / "Transcriptor Portable",
                    "exe_name": "Transcriptor.exe",
                    "ico": APPS_DIR / "iconos" / "transcriptor.ico"
                },
            }

            for idx, app_name in enumerate(selected_apps):
                info = pkg_info[app_name]
                curr_step += 1
                prog = (curr_step / total_steps) * 90.0
                self.msg_queue.put(("progress", prog))
                self.msg_queue.put(("status", f"Desplegando {app_name}..."))
                self._log(f"--- Procesando: {app_name} ---")

                if mode == "system" and info["inst_exe"].exists():
                    # Ejecutar instalador Inno Setup con flags de instalación silenciosa
                    cmd = f'"{info["inst_exe"]}" /VERYSILENT /SUPPRESSMSGBOXES /NORESTART'
                    self._log(f"Ejecutando instalador del sistema: {info['inst_exe'].name}")
                    res = subprocess.run(cmd, shell=True)
                    self._log(f"Instalación de {app_name} completada (código {res.returncode})")
                else:
                    # Modo portable: copiar carpeta o descomprimir zip
                    target_app_dir = dest_dir / app_name
                    if info["portable_folder"].exists():
                        self._log(f"Copiando archivos portables a {target_app_dir.name}...")
                        if target_app_dir.exists():
                            shutil.rmtree(target_app_dir)
                        shutil.copytree(info["portable_folder"], target_app_dir)
                        self._log(f"Copiado exitoso de {app_name}")
                    elif info["portable_zip"].exists():
                        self._log(f"Extrayendo paquete {info['portable_zip'].name}...")
                        with zipfile.ZipFile(info["portable_zip"], "r") as zf:
                            zf.extractall(dest_dir)
                        self._log(f"Extracción completada de {app_name}")

                # Crear accesos directos si corresponde
                if self.create_desktop_lnk.get() or self.create_startmenu_lnk.get():
                    self._create_shortcuts_for_app(app_name, info, dest_dir)

            # Copiar documentación y Hub a la carpeta destino
            doc_dst = dest_dir / "LEEME_SUITE.md"
            suite_leeme = APPS_DIR / "OmniSuite Studio" / "LEEME.md"
            if suite_leeme.exists():
                shutil.copy2(suite_leeme, doc_dst)

            self.msg_queue.put(("progress", 100.0))
            self.msg_queue.put(("status", "¡Despliegue finalizado con éxito!"))
            self.msg_queue.put(("done", True))

        except Exception as e:
            self._log(f"ERROR DURANTE EL DESPLIEGUE: {e}")
            self.msg_queue.put(("status", f"Error: {e}"))
            self.msg_queue.put(("done", False))

    def _create_shortcuts_for_app(self, app_name, info, dest_dir):
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")

            # Buscar ejecutable
            exe_target = dest_dir / app_name / info["exe_name"]
            if not exe_target.exists():
                exe_target = dest_dir / f"{app_name} Portable" / info["exe_name"]
            if not exe_target.exists():
                # En modo sistema, buscar en Program Files
                pf = Path(os.environ.get("ProgramFiles", "C:\\Program Files"))
                cand = pf / "Tu Tiendita IA" / app_name / info["exe_name"]
                if cand.exists():
                    exe_target = cand

            if not exe_target.exists():
                self._log(f"Nota: No se halló la ruta del .exe para acceso directo de {app_name}")
                return

            ico_path = info["ico"]

            # 1. Escritorio
            if self.create_desktop_lnk.get():
                desktop = Path(shell.SpecialFolders("Desktop"))
                lnk = shell.CreateShortcut(str(desktop / f"{app_name}.lnk"))
                lnk.TargetPath = str(exe_target)
                lnk.WorkingDirectory = str(exe_target.parent)
                if ico_path.exists():
                    lnk.IconLocation = f"{ico_path},0"
                lnk.Save()
                self._log(f"Acceso directo creado en Escritorio: {app_name}.lnk")

            # 2. Menú Inicio
            if self.create_startmenu_lnk.get():
                programs_f = Path(shell.SpecialFolders("Programs")) / "Tu Tiendita IA"
                programs_f.mkdir(parents=True, exist_ok=True)
                lnk_sm = shell.CreateShortcut(str(programs_f / f"{app_name}.lnk"))
                lnk_sm.TargetPath = str(exe_target)
                lnk_sm.WorkingDirectory = str(exe_target.parent)
                if ico_path.exists():
                    lnk_sm.IconLocation = f"{ico_path},0"
                lnk_sm.Save()
                self._log(f"Acceso directo creado en Menú Inicio: Tu Tiendita IA\\{app_name}.lnk")

        except Exception as err:
            self._log(f"Nota creando accesos directos: {err}")

    def _on_install_completed(self, success: bool):
        self.is_installing = False
        self.btn_install.configure(state="normal", text="🚀 Iniciar Instalación / Despliegue de la Suite")
        if success:
            dest = self.dest_path_var.get()
            ans = messagebox.askyesno(
                "¡Instalación Completada!",
                "Las aplicaciones seleccionadas de OmniSuite Studio fueron desplegadas con éxito.\n\n"
                f"Destino:\n{dest}\n\n¿Deseás abrir la carpeta de destino ahora mismo?"
            )
            if ans and os.path.exists(dest):
                os.startfile(dest)


def main():
    root = tk.Tk()
    app = OmniSuiteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
