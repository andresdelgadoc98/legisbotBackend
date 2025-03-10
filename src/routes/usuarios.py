from flask import request, jsonify, Blueprint
from db.db import Usuario, db
from flask_cors import cross_origin
import bcrypt
import jwt
from datetime import datetime, timedelta

from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
SECRET_KEY = os.getenv("SECRET_KEY")

ACCESS_TOKEN_EXPIRATION = 15
REFRESH_TOKEN_EXPIRATION = 7


main = Blueprint('users', __name__)

@main.route("", methods=["POST"])
@cross_origin(origin='*')
def registro():
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        email = data.get("email")
        contraseña = data.get("contraseña")

        if not nombre or not email or not contraseña:
            return jsonify({"error": "Faltan datos"}), 400

        if Usuario.query.filter_by(email=email).first():
            return jsonify({"error": "El email ya está registrado"}), 400

        contraseña_hasheada = bcrypt.hashpw(contraseña.encode("utf-8"), bcrypt.gensalt())

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            contraseña=contraseña_hasheada.decode("utf-8"),
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"mensaje": "Usuario registrado exitosamente", "id": nuevo_usuario.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route("/login", methods=["POST"])
@cross_origin(origin='*')
def login():
    try:
        data = request.get_json()
        print(data)
        email = data.get("email")
        contraseña = data.get("password")

        if not email or not contraseña:
            return jsonify({"error": "Faltan datos"}), 400

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            return jsonify({"error": "Credenciales inválidas"}), 401

        if not bcrypt.checkpw(contraseña.encode("utf-8"), usuario.contraseña.encode("utf-8")):
            return jsonify({"error": "Credenciales inválidas"}), 401
        usuario_id = str(usuario.id)
        access_token = jwt.encode(
            {
                "sub": usuario_id,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION),
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        refresh_token = jwt.encode(
            {
                "sub": usuario_id,
                "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@main.route("/refresh_token", methods=["POST"])
@cross_origin(origin='*')
def refresh_token():
    try:
        data = request.get_json()
        refresh_token = data.get("refresh_token")

        if not refresh_token:
            return jsonify({"error": "Refresh token no proporcionado"}), 400
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Refresh token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Refresh token inválido"}), 401

        usuario_id = payload.get("sub")
        if not usuario_id:
            return jsonify({"error": "Refresh token inválido"}), 401

        access_token = jwt.encode(
            {
                "sub": usuario_id,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        return jsonify({
            "mensaje": "Access token renovado exitosamente",
            "access_token": access_token,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('<uuid:usuario_id>', methods=['GET'])
@cross_origin(origin='*')
def obtener_usuario(usuario_id):
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({
            "email": usuario.email,
            "nombre": usuario.nombre
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500