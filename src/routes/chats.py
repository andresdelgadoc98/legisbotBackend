from flask import request, jsonify, Blueprint
from db.db import Chat, Usuario, db
from flask_cors import cross_origin
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from src.utils.middlewares import token_required
from sqlalchemy import exc
main = Blueprint('chats', __name__)
@main.route("", methods=["POST"])
@cross_origin(origin='*')
@token_required
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

@main.route("<id_usuario>", methods=["GET"])
@cross_origin(origin='*')
@token_required
def obtener_chats_usuario(id_usuario):

    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    chats = Chat.query.filter_by(id_usuario=id_usuario).order_by(desc(Chat.fecha_creacion)).all()

    chats_json = [{
        "id": chat.id,
        "titulo": chat.titulo,
        "fecha_creacion": chat.fecha_creacion.isoformat() if chat.fecha_creacion else None
    } for chat in chats]


    return jsonify(chats_json), 200

@main.route("obtener_contenido_chat", methods=["GET"])
@cross_origin(origin='*')
@token_required
def obtener_contenido_chat():

    chat_id = request.args.get('chat_id', type=str)
    usuario_id = request.args.get('usuario_id', type=str)
    print(chat_id)
    print( usuario_id)
    if not chat_id or not usuario_id:
        return jsonify({"error": "Se requieren chat_id y usuario_id"}), 400

    try:
        chat = Chat.query.filter_by(id=chat_id, id_usuario=usuario_id).one()
        return jsonify({
            "chat_id": chat.id,
            "usuario_id": chat.id_usuario,
            "contenido": chat.contenido,
            "preferencia": chat.preferencia
        }), 200

    except NoResultFound:
        return jsonify([]), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("<chat_id>", methods=["DELETE"])
@cross_origin(origin='*')
@token_required
def eliminar_chat(chat_id):
    chat = Chat.query.get(chat_id)
    if not chat:
        return jsonify({"error": "Chat no encontrado"}), 404
    db.session.delete(chat)
    db.session.commit()
    return jsonify({"mensaje": "Chat eliminado correctamente"}), 200

@main.route("<chat_id>/contexto", methods=["PUT"])
@cross_origin(origin='*')
@token_required
def editar_contexto(chat_id):
    chat = Chat.query.get(chat_id)
    if not chat:
        return jsonify({"error": "Chat no encontrado"}), 404

    data = request.get_json()
    nuevo_contexto = data.get("contexto")

    if not nuevo_contexto:
        return jsonify({"error": "El campo 'contexto' es requerido"}), 400

    chat.contexto = nuevo_contexto
    db.session.commit()

    return jsonify({"mensaje": "Contexto actualizado correctamente"}), 200

@main.route("<chat_id>/contexto", methods=["GET"])
@cross_origin(origin='*')
@token_required
def obtener_contexto(chat_id):
    chat = Chat.query.get(chat_id)
    if not chat:
        return jsonify({"error": "Chat no encontrado"}), 404

    return jsonify({"contexto": chat.contexto}), 200


@main.route('<chat_id>/preferencia', methods=['PUT'])
@cross_origin(origin='*')
@token_required
def actualizar_preferencia(chat_id):
    chat = Chat.query.get(chat_id)
    if not chat:
        return jsonify({"error": "Chat no encontrado"}), 404

    data = request.get_json()
    if not data or "preferencia" not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        chat.preferencia = data["preferencia"]
        db.session.commit()
        return jsonify({"mensaje": "Preferencia actualizada correctamente", "preferencia": chat.preferencia}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('<chat_id>/title', methods=['PUT'])
@cross_origin(origin='*')
def update_chat_title(chat_id):
    print(chat_id)
    try:
        data = request.get_json()
        if not data or 'titulo' not in data:
            return jsonify({'error': 'El título es requerido'}), 400
        nuevo_titulo = data['titulo']
        if len(nuevo_titulo) > 45:
            return jsonify({'error': 'El título no puede exceder 45 caracteres'}), 400
        chat = Chat.query.get_or_404(chat_id)
        chat.titulo = nuevo_titulo
        db.session.commit()
        return jsonify({
            'message': 'Título actualizado exitosamente',
            'chat': {
                'id': chat.id,
                'titulo': chat.titulo,
                'fecha_creacion': chat.fecha_creacion.isoformat()
            }
        }), 200

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Error de integridad en la base de datos'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500