from flask import Flask
from flask_socketio import SocketIO
from .routes import socket
from .routes import rag
from .routes import documents
from .routes import chats
from db.db import db  # Importar la instancia de SQLAlchemy

# Crear la instancia de SocketIO
socketio = SocketIO(ping_timeout=60, ping_interval=25, cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:%40Telemetry1@localhost/legisbot"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(rag.main, url_prefix='/')
    app.register_blueprint(documents.main, url_prefix='/documents')
    app.register_blueprint(chats.main, url_prefix='/chats')

    socketio.init_app(app)
    socket.init_socketio(socketio)

    with app.app_context():
        db.create_all()

    return app