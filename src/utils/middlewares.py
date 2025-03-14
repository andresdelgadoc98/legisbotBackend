import os
import requests
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify
import jwt
from db.db import Usuario,Licencia
from datetime import datetime
SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
SECRET_KEY_ACCESS = os.getenv("SECRET_KEY_ACCESS")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                "message": "Token is missing",
                "statusCode": 403
            }), 403

        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        else:
            return jsonify({
                "message": "Invalid token format",
                "statusCode": 403
            }), 403
        try:
            data = jwt.decode(token, SECRET_KEY_ACCESS, algorithms=["HS256"])
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({
                "message": "Token has expired",
                "statusCode": 403
            }), 403
        except jwt.InvalidTokenError:
            return jsonify({
                "message": "Invalid token",
                "statusCode": 403
            }), 403

    return decorated


def validar_licencia(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("refresh_token")
        if not token:
            return jsonify({"error": "Token no proporcionado"}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY_REFRESH, algorithms=["HS256"])
            usuario_id = payload.get("sub")
            if not usuario_id:
                return jsonify({"error": "Token inválido: falta el ID del usuario"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        usuario = Usuario.query.get(usuario_id)
        print(usuario)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404


        if not usuario.licencia_id:
            return jsonify({"error": "El usuario no tiene una licencia asociada"}), 403

        licencia = Licencia.query.get(usuario.licencia_id)
        if not licencia:
            return jsonify({"error": "Licencia no encontrada"}), 404

        fecha_actual = datetime.utcnow().date()
        if fecha_actual < licencia.fecha_inicio:
            return jsonify({"error": "La licencia no ha comenzado"}), 403
        if fecha_actual > licencia.fecha_fin:
            return jsonify({"error": "La licencia ha expirado"}), 403

        return f(*args, **kwargs)

    return wrapper