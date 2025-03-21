from flask import Flask
from flask_socketio import SocketIO
from .routes import socket
from .routes import rag
from .routes import documents
from .routes import chats
from .routes import usuarios
from .routes import token
from .routes import licencias
from .routes import notification
from db.db import db
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

socketio = SocketIO(ping_timeout=60, ping_interval=25, cors_allowed_origins="*", async_mode='eventlet')


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(rag.main, url_prefix='/')
    app.register_blueprint(documents.main, url_prefix='/api/documents')
    app.register_blueprint(chats.main, url_prefix='/api/chats')
    app.register_blueprint(usuarios.main, url_prefix='/api/users')
    app.register_blueprint(token.main, url_prefix='/api/token')
    app.register_blueprint(licencias.main, url_prefix='/api/licencias')
    app.register_blueprint(notification.main, url_prefix='/api/notification')

    socketio.init_app(app)
    socket.init_socketio(socketio,app)

    with app.app_context():
        db.create_all()

    return app
