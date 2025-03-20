from flask import request, jsonify, Blueprint
from db.db import Usuario, db
from flask_cors import cross_origin
from src.utils.utils_notification import get_next_friday,generate_year_week,check_jurisprudencias
from firebase_admin import credentials, messaging, initialize_app

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

@main.route("/send_notifications", methods=["POST"])
@cross_origin(origin='*')
def send_notification():
    tokens_result = Usuario.query.with_entities(Usuario.token_notification).all()
    tokens = [token[0] for token in tokens_result if token[0]]
    if not tokens:
        return jsonify({"message": "No se encontraron tokens de notificación"}), 404

    next_friday = get_next_friday()
    year_week = int(generate_year_week(next_friday)) + 0
    result = check_jurisprudencias(year_week=year_week)
    print(result["total"])
    if result['documents']:
        cred = credentials.Certificate('firebase.json')
        initialize_app(cred)
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title="Jurisprudencias",
                body=f'Se Actualizaron {result["total"]} Jurisprudencias',
            ),
            data={
                'url': f'https://www.saturnodelgado.com/jurisprudencias?yearWeek={year_week}'
            },
            tokens=tokens,
        )
        response = messaging.send_each_for_multicast(message)
        print('Successfully sent message:', response)
        return jsonify({"message": f"Successfully sent message to {response.success_count} devices"}),200
    else:
        return jsonify({"message": "no se encontraron jurisprudencias "}), 404
