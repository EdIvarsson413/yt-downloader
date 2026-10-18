from core import socketio
from flask_socketio import emit
from downloader import ejecutar_descarga
from concurrent.futures import ThreadPoolExecutor

# Creamos el pool global: máximo 3 descargas a la vez
pool = ThreadPoolExecutor(max_workers=3)

@socketio.on('connect')
def al_conectar():
    print('Cliente conectado')
    emit('bienvenida', {'mensaje': 'Conectado al servidor'})

@socketio.on('disconnect')
def al_desconectar():
    print('Cliente desconectado')

@socketio.on('descargar')
def manejar_descarga(data: dict):
    url = data.get('url')
    job_id = data.get('jobId')

    if not url or not job_id:
        emit('error', {'jobId': job_id, 'mensaje': 'Faltan url o jobId'})
        return

    print(f'[{job_id}] Tarea recibida y enviada a la cola: {url}')
    
    # Avisamos al cliente que está en cola
    emit('en_cola', {'jobId': job_id})

    # Enviamos la descarga al pool (se ejecutará cuando haya un hilo libre)
    pool.submit(ejecutar_tarea_en_hilo, url, job_id)


def ejecutar_tarea_en_hilo(url: str, job_id: str):
    """
    Esta función corre en un hilo separado. 
    OJO: Usamos socketio.emit (no emit) porque estamos fuera del contexto del cliente.
    """
    def puente_progreso(datos):
        socketio.emit('progreso', datos)

    def puente_completado(datos):
        socketio.emit('completado', datos)

    def puente_error(datos):
        socketio.emit('error', datos)

    ejecutar_descarga(
        url=url, 
        job_id=job_id,
        on_progreso=puente_progreso,
        on_completado=puente_completado,
        on_error=puente_error
    )