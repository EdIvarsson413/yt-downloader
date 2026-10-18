from flask import jsonify

def init_routes(app):
    @app.route('/')
    def inicio():
        return jsonify({'status': 'ok', 'mensaje': 'Servidor activo'})