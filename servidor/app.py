from flask import Flask
from core import socketio, SECRET_KEY, PUERTO
from routes import init_routes
import sockets
import atexit

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# FORZAMOS el uso de hilos nativos en lugar de eventlet
socketio.init_app(app, async_mode='threading')

init_routes(app)

def cerrar_pool():
    print("Apagando servidor. Cerrando hilos...")
    sockets.pool.shutdown(wait=False)
atexit.register(cerrar_pool)

if __name__ == '__main__':
    print(f'Servidor escuchando en http://127.0.0.1:{PUERTO}')
    # Apagamos use_reloader para que no reinicie al guardar test_socket.py
    socketio.run(app, host='127.0.0.1', port=PUERTO, debug=True, use_reloader=False)