from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import JSON

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
    chats = db.relationship("Chat", backref="usuario", lazy=True)
    licencia_id = db.Column(db.String(36), db.ForeignKey("licencias.id"), nullable=True)  # Relación con licencias

class Documento(db.Model):
    __tablename__ = 'documentos'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    titulo =db.Column(db.Text, nullable=True)
    fecha_publicacion = db.Column(db.DateTime)
    folder = db.Column(db.String(255))
    ruta = db.Column(db.Text)
    jurisdiccion = db.Column(db.String(255), nullable=True)


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    contenido = db.Column(MutableList.as_mutable(db.JSON), nullable=True, default=list)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    contexto = db.Column(db.Text, nullable=True)
    preferencia = db.Column(JSON, default={"searchType": None,"document":""})

    def guardar_mensaje(self, chat_id, usuario_id, user_question, bot_response):
        chat = Chat.query.filter_by(id=chat_id, id_usuario=usuario_id).first()

        if chat:
            nuevo_contenido = [
                {"text": user_question, "sender": "user"},
                {"text": bot_response, "sender": "bot"}
            ]

            chat.contenido.extend(nuevo_contenido)
            flag_modified(chat, "contenido")
            db.session.commit()

            print("Mensaje guardado exitosamente.")
        else:
            print(f"No se encontró el chat con ID {chat_id} y usuario ID {usuario_id}.")

class Licencia(db.Model):
    __tablename__ = "licencias"

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    nombre_licencia = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    usuarios = db.relationship("Usuario", backref="licencia", lazy=True)


