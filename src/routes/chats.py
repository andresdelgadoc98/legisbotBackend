from flask import request, jsonify, Blueprint
from db.db import Chat, Usuario, db
from flask_cors import cross_origin
from sqlalchemy.orm.exc import NoResultFound


main = Blueprint('chats', __name__)

@main.route("", methods=["POST"])
@cross_origin(origin='*')
def crear_chat():
    data = request.json
    titulo = data.get("titulo")
    usuario_id = data.get("id_user")
    print(data)
    if not titulo or not usuario_id:
        return jsonify({"error": "Faltan datos"}), 400

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    nuevo_chat = Chat(titulo=titulo, id_usuario=usuario_id)
    db.session.add(nuevo_chat)
    db.session.commit()

    return jsonify({"mensaje": "Chat creado", "chat_id": nuevo_chat.id}), 201


@main.route("<int:id_usuario>", methods=["GET"])
@cross_origin(origin='*')
def obtener_chats_usuario(id_usuario):
    print(id_usuario)
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    chats = Chat.query.filter_by(id_usuario=id_usuario).all()

    chats_json = [{
        "id": chat.id,
        "titulo": chat.titulo,
        "fecha_creacion": chat.fecha_creacion.isoformat() if chat.fecha_creacion else None
    } for chat in chats]

    return jsonify(chats_json), 200

@main.route("obtener_contenido_chat", methods=["GET"])
@cross_origin(origin='*')
def obtener_contenido_chat():

    chat_id = request.args.get('chat_id', type=int)
    usuario_id = request.args.get('usuario_id', type=int)
    print(chat_id)
    print( usuario_id)
    if not chat_id or not usuario_id:
        return jsonify({"error": "Se requieren chat_id y usuario_id"}), 400

    try:
        chat = Chat.query.filter_by(id=chat_id, id_usuario=usuario_id).one()

        return jsonify({
            "chat_id": chat.id,
            "usuario_id": chat.id_usuario,
            "contenido": chat.contenido
        }), 200

    except NoResultFound:
        return jsonify([]), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
