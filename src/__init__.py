from flask import Flask
from flask_socketio import SocketIO
from .routes import socket
from .routes import rag
from .routes import documents
from .routes import chats
from .routes import usuarios
from db.db import db
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Crear la instancia de SocketIO
socketio = SocketIO(ping_timeout=60, ping_interval=25, cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)

    # Usar las variables de entorno
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(rag.main, url_prefix='/')
    app.register_blueprint(documents.main, url_prefix='/documents')
    app.register_blueprint(chats.main, url_prefix='/chats')
    app.register_blueprint(usuarios.main, url_prefix='/users')
    socketio.init_app(app)
    socket.init_socketio(socketio)

    with app.app_context():
        db.create_all()

    return app
