from flask import Flask
from flask_socketio import SocketIO
from .routes import socket
from .routes import rag
from .routes import documents

socketio = SocketIO(ping_timeout=60, ping_interval=25, cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    app.register_blueprint(rag.main, url_prefix='/')
    app.register_blueprint(documents.main, url_prefix='/documents')
    socketio.init_app(app)
    socket.init_socketio(socketio)
    return app