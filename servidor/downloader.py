import yt_dlp
import os
import shutil
from core import OPCIONES_YTDLP, CARPETA_DESCARGAS

def ejecutar_descarga(url: str, job_id: str, on_progreso=None, on_completado=None, on_error=None):
    
    # 1. Creamos una carpeta temporal única para este job
    carpeta_temporal = os.path.join(CARPETA_DESCARGAS, f"temp_{job_id}")
    os.makedirs(carpeta_temporal, exist_ok=True)

    def hook_progreso(d):
        if d['status'] == 'downloading':
            if on_progreso:
                on_progreso({
                    'jobId': job_id,
                    'porcentaje': d.get('_percent_str', '0%').strip(),
                    'velocidad': d.get('_speed_str', 'N/A').strip(),
                    'eta': d.get('_eta_str', 'N/A').strip(),
                    'descargado': d.get('downloaded_bytes', 0),
                    'total': d.get('total_bytes') or d.get('total_bytes_estimate', 0),
                })
        elif d['status'] == 'finished':
            print(f'[{job_id}] Archivo temporal listo: {d["filename"]}')

    # 2. Preparamos las opciones para este job específico
    opciones = OPCIONES_YTDLP.copy()
    opciones['progress_hooks'] = [hook_progreso]
    # Guardamos temporalmente en la subcarpeta
    opciones['outtmpl'] = os.path.join(carpeta_temporal, '%(title)s.%(ext)s')

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # 3. Movemos el archivo final a la carpeta principal
            ruta_temporal_archivo = ydl.prepare_filename(info)
            # Ajuste por si yt-dlp cambió la extensión al fusionar
            if not os.path.exists(ruta_temporal_archivo) and ruta_temporal_archivo.endswith('.webm'):
                ruta_temporal_archivo = ruta_temporal_archivo.replace('.webm', '.mp4')

            nombre_archivo = os.path.basename(ruta_temporal_archivo)
            ruta_final = os.path.join(CARPETA_DESCARGAS, nombre_archivo)

            if os.path.exists(ruta_temporal_archivo):
                shutil.move(ruta_temporal_archivo, ruta_final)

            if on_completado:
                on_completado({
                    'jobId': job_id,
                    'titulo': info.get('title'),
                    'archivo': ruta_final,
                })
                
    except Exception as e:
        print(f'[{job_id}] Error en descarga: {e}')
        if on_error:
            on_error({'jobId': job_id, 'mensaje': str(e)})
    finally:
        # 4. Limpiamos la carpeta temporal (opcional, pero recomendado)
        if os.path.exists(carpeta_temporal):
            try:
                shutil.rmtree(carpeta_temporal)
            except Exception as e:
                print(f'[{job_id}] No se pudo borrar carpeta temporal: {e}')