# Instructivo de Uso y Workflows — OmniSuite Studio

> **Guía paso a paso para maximizar el rendimiento creativo y técnico.**  
> Marca Oficial: **Tu Tiendita IA** · Sitio web: [tutiendita-ia.store](https://tutiendita-ia.store)

---

## 📋 Índice Rápido
1. [Instalación Rápida: All in One vs. Personalizada](#1-instalación-rápida-all-in-one-vs-personalizada)
2. [Workflow 1: Animadores 3D & Diseñadores CGI](#workflow-1-animadores-3d--diseñadores-cgi)
3. [Workflow 2: Community Managers & Creadores de Contenido Móvil (9:16)](#workflow-2-community-managers--creadores-de-contenido-móvil-916)
4. [Workflow 3: Editores Audiovisuales & Cineastas (Premiere / DaVinci)](#workflow-3-editores-audiovisuales--cineastas-premiere--davinci)
5. [Workflow 4: Podcasters, Productores & Transcripción de Entrevistas](#workflow-4-podcasters-productores--transcripción-de-entrevistas)
6. [Atajos, Optimización RTX & Resolución de Problemas](#6-atajos-optimización-rtx--resolución-de-problemas)

---

## 1. Instalación Rápida: All in One vs. Personalizada

Podés instalar la Suite de dos maneras muy sencillas:

### Método A: Instalador Interactivo OmniSuite Hub (Recomendado)
1. Abrí **`OmniSuite Studio.exe`** (o hacé doble clic en el acceso directo del Escritorio).
2. Verás las 4 herramientas con sus casillas de selección:
   - Presioná **`✨ Seleccionar Todo (All in One)`** si querés contar con el estudio completo.
   - O marcá/desmarcá individualmente las que prefieras (por ejemplo, solo *OmniBoost* y *OmniFlow*).
3. Elegí la modalidad:
   - **`🚀 Instalación en Sistema`**: Registra las aplicaciones en Windows y crea accesos directos en el Menú Inicio.
   - **`💼 Despliegue Portable`**: Te permite elegir un pendrive, disco SSD portátil o carpeta local para llevar las aplicaciones a cualquier PC sin instalar nada.
4. Presioná el botón amarillo **`🚀 Iniciar Instalación / Despliegue`** y observá la barra de progreso.

### Método B: Asistente Estándar de Windows (`OmniSuite Studio Instalador Completo 1.0.exe`)
1. Ejecutá el archivo `.exe` desde la carpeta `Instaladores\00 OmniSuite Studio\Instalador\`.
2. En la pantalla de componentes, seleccioná tu perfil:
   - **Instalación Completa (All-in-One)**
   - **Solo Herramientas de Video (Booster, Flow, Scale)**
   - **Personalizada**
3. Hacé clic en Siguiente y el instalador colocará todo de forma silenciosa y ordenada.

---

## Workflow 1: Animadores 3D & Diseñadores CGI
*(Para usuarios de Blender, Maya, 3ds Max, Cinema 4D, Unreal Engine y estilo Pixar)*

### El Problema
Renderizar 60 cuadros por segundo o resoluciones 4K en un motor de trazado de rayos (Cycles, Arnold, V-Ray, Redshift, Lumen) es computacionalmente muy costoso.

### El Procedimiento Óptimo:
1. **Configuración en tu software 3D**:
   - Renderizá tu animación a **24 FPS** en **1080p** (ahorro inmediato de más del 60% del tiempo de cálculo de tu GPU).
   - Exportá como `.mp4` o secuencia de video con compresión estándar.
2. **Paso 1 — Restaurar y pulir con OmniBoost Studio**:
   - Abrí **OmniBoost Studio**.
   - Cargá tu video renderizado.
   - En *Tipo de Video / Perfil*, elegí: **`🎨 Animación 3D & CGI (Pixar, Disney, Gaming, Unreal Engine)`**.
   - En *Aceleración GPU*, seleccioná **`NVIDIA GeForce RTX (NVENC p7)`** (o AMD Radeon AMF).
   - Presioná **Mejorar Video**. OmniBoost limpiará el ruido estático de muestreo en sombras y realzará la volumetría de la iluminación.
3. **Paso 2 — Elevar la fluidez a 60 o 120 FPS con OmniFlow FPS Booster**:
   - Cargá el video resultante (`_boosted.mp4`) en **OmniFlow FPS Booster**.
   - En *Tasa Destino*, seleccioná **`60 FPS`** (o `120 FPS` para pantallas gamer de alta tasa de refresco).
   - En *Método*, elegí **`Universal Adaptativo`**.
   - Presioná **Elevar FPS**.
4. **Resultado**: Tu animación tendrá la suavidad fluida de una película de Pixar o Disney lista para festivales o portafolio, habiendo ahorrado horas de cómputo en tu placa de video.

---

## Workflow 2: Community Managers & Creadores de Contenido Móvil (9:16)
*(Para TikTok, Instagram Reels, YouTube Shorts y contenido vertical viral)*

### El Problema
Los videos grabados originalmente en horizontal (16:9) se ven chicos o con bordes negros en el teléfono. Además, el 85% de los usuarios mira videos sin sonido, por lo que los subtítulos sincronizados son obligatorios.

### El Procedimiento Óptimo:
1. **Adaptar y Reescalar con OmniScale Studio**:
   - Abrí **OmniScale Studio**.
   - Cargá tu video grabado con celular o cámara horizontal.
   - En *Resolución Destino*, elegí: **`1080x1920 (9:16 Vertical Reels / TikTok / Shorts)`** o **`Auto-Adaptativo 1080p`**.
   - En *Tipo de Contenido*, seleccioná **`Lanczos + FidelityFX CAS`**.
   - Presioná **Reescalar Video**.
2. **Subtitulado Automático con Transcriptor Local**:
   - Abrí **Transcriptor Local**.
   - Cargá el video vertical generado.
   - En la tarjeta de Hablantes, ingresá tu nombre (ej. "Facundo" o "Valentina").
   - Presioná **Iniciar Transcripción**.
   - En segundos, Whisper large-v3-turbo analizará el audio y creará:
     - El archivo **`.SRT`** sincronizado con timestamps precisos.
     - El archivo **`.TXT`** para armar el copy o descripción del posteo.
3. **Quemar los subtítulos en tu editor**:
   - Abrí CapCut, DaVinci Resolve o Premiere Pro.
   - Arrastrá el video reescalado y el archivo `.SRT`.
   - Elegí tu tipografía y colores preferidos. ¡Listo para publicar en redes sociales con máxima retención!

---

## Workflow 3: Editores Audiovisuales & Cineastas (Premiere / DaVinci)
*(Para documentales, cortometrajes, publicidad y coloristas)*

### El Problema
Tomas de drone o cámaras mirrorless con compresión de 8 bits que presentan banding en cielos y pérdida de nitidez en planos generales.

### El Procedimiento Óptimo:
1. Abrí **OmniBoost Studio**.
2. Seleccioná el perfil **`🎬 Cine & Películas Reales (Piel natural, preserva grano 35mm)`**.
3. Si necesitás ajuste milimétrico, pasá al perfil **`🎛️ Personalizado`**:
   - *Nitidez CAS*: 35% a 50% (resalta texturas de ropa y cabello sin bordes blancos).
   - *De-banding*: 60% a 80% (suaviza degradados en cielos o atardeceres).
   - *Denoise*: 20% a 30% (limpieza suave en sombras sin empastar).
4. Exportá en **CRF 16 (Master sin pérdida perceptible)**.
5. El material resultante ingresará a DaVinci Resolve o Premiere Pro con mayor latitud para corrección de color y etalonaje.

---

## Workflow 4: Podcasters, Productores & Transcripción de Entrevistas
*(Para creadores de podcasts, periodistas, clases y peritajes)*

### El Problema
Entrevistas largas donde participan varias personas y se requiere saber quién dijo cada frase sin perder horas desgrabando manualmente.

### El Procedimiento Óptimo:
1. Abrí **Transcriptor Local**.
2. Cargá el audio o video en la pestaña **Transcripción**.
3. En la sección de los 4 Hablantes, asigná los nombres reales de los participantes:
   - Hablante 1 (Birome): "Conductor"
   - Hablante 2 (Malvón): "Invitado 1"
   - Hablante 3 (Yema): "Invitado 2"
   - Hablante 4 (Celeste): "Preguntas del Público"
4. Presioná **Iniciar Transcripción**.
5. Al terminar, hacé clic en **`Abrir en Visor`** (Pestaña "Visor y Editor"):
   - Podés escuchar cualquier fragmento presionando el botón ▶ en color Birome.
   - Si una palabra técnica o nombre propio necesita corrección, editalo directamente en la tarjeta del segmento.
   - Presioná **`Guardar Cambios y Re-exportar Todo`**: se regenerarán instantáneamente el archivo de subtítulos `.SRT`, el informe en Word `.DOCX` con tablas estadísticas y el `.TXT`.

---

## 6. Atajos, Optimización RTX & Resolución de Problemas

### Maximizar la Velocidad con Placas NVIDIA RTX
- Asegurate de tener instalados los drivers Game Ready o Studio más recientes de NVIDIA (GeForce Experience o la app de NVIDIA).
- En OmniBoost, OmniFlow y OmniScale, elegí siempre la opción **`NVIDIA GeForce RTX (NVENC p7 + Spatial/Temporal AQ)`**.
- En Transcriptor Local, el motor detectará automáticamente si tenés GPU compatible con CUDA para activar el modo de coma flotante semi-precisión (**float16**), procesando audios a velocidades de hasta 10x en tiempo real.

### ¿Tenés procesador sin placa de video dedicada?
- Todas las herramientas cuentan con modo universal por CPU (`libx264` multihilo y Whisper float32). Funcionan al 100% en cualquier laptop o PC con Windows 10 u 11.

---

*Para soporte, nuevos modelos y recursos de IA, visitá la tienda oficial de **Tu Tiendita IA** · [https://tutiendita-ia.store](https://tutiendita-ia.store)*
