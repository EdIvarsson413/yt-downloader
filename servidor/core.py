import os
from flask_socketio import SocketIO

# --- Configuración Base ---
SECRET_KEY = 'cambia-esto-por-algo-seguro'
PUERTO = 2208

# Carpeta de descargas (se crea si no existe)
CARPETA_DESCARGAS = os.path.join(os.path.dirname(__file__), 'descargas')
os.makedirs(CARPETA_DESCARGAS, exist_ok=True)

# Opciones base para yt-dlp
OPCIONES_YTDLP = {
    # 'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b',
    'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b',
    'merge_output_format': 'mp4',
    'quiet': True,
    'no_warnings': True,
    # 'ffmpeg_location': r'C:\Users\Eadweard\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin',
}

# --- Extensiones ---
# Se crea aquí sin la app para evitar importaciones circulares.
# La app se vinculará en app.py
socketio = SocketIO(cors_allowed_origins="*")