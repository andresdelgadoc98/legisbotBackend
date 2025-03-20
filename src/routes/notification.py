from flask import request, jsonify, Blueprint
from db.db import Usuario, db
from flask_cors import cross_origin

main = Blueprint('notification', __name__)

@main.route("/uuid:usuario_id>", methods=["GET"])
@cross_origin(origin='*')
def get_token_notification(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"token_notification": usuario.token_notification})


@main.route("<uuid:usuario_id>", methods=["PUT"])
@cross_origin(origin='*')
def update_token_notification(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.json
    new_token = data.get("token_notification")

    if not new_token:
        return jsonify({"error": "El token_notification es requerido"}), 400

    usuario.token_notification = new_token
    db.session.commit()

    return jsonify({"message": "Token actualizado correctamente", "token_notification": usuario.token_notification})

@main.route("<uuid:usuario_id>", methods=["DELETE"])
@cross_origin(origin='*')
def delete_token_notification(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    usuario.token_notification = None
    db.session.commit()
    return jsonify({"message": "Token eliminado correctamente"})
