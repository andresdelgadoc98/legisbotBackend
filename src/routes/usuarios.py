from flask import request, jsonify, Blueprint,make_response
from db.db import Usuario, db,Licencia
from flask_cors import cross_origin
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from src.utils.middlewares import token_required
load_dotenv()

SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
SECRET_KEY_ACCESS = os.getenv("SECRET_KEY_ACCESS")
ACCESS_TOKEN_EXPIRATION = int(os.getenv("ACCESS_TOKEN_EXPIRATION"))
REFRESH_TOKEN_EXPIRATION = int(os.getenv("REFRESH_TOKEN_EXPIRATION"))


main = Blueprint('users', __name__)

@main.route("", methods=["POST"])
@cross_origin(origin='*')
def registro():
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        email = data.get("email")
        contraseña = data.get("contraseña")
        licencia_id =  data.get("licencia_id")
        print(licencia_id)

        if not nombre or not email or not contraseña:
            return jsonify({"error": "Faltan datos"}), 400

        if Usuario.query.filter_by(email=email).first():
            return jsonify({"error": "El email ya está registrado"}), 400

        contraseña_hasheada = bcrypt.hashpw(contraseña.encode("utf-8"), bcrypt.gensalt())

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            contraseña=contraseña_hasheada.decode("utf-8"),
            licencia_id=licencia_id
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


        access_token = jwt.encode(
            {
                "sub": usuario_id,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION),
            },
            SECRET_KEY_ACCESS,
            algorithm="HS256",
        )

        refresh_token = jwt.encode(
            {
                "sub": usuario_id,
                "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION),
            },
            SECRET_KEY_REFRESH,
            algorithm="HS256",
        )

        response = make_response(jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "access_token": access_token,
            "refresh_token":refresh_token
        }))

        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=False,
            secure=False,
            samesite="none",
            max_age=REFRESH_TOKEN_EXPIRATION * 24 * 3600
        )

        return response, 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@main.route('<uuid:usuario_id>', methods=['GET'])
@cross_origin(origin='*')
@token_required
def obtener_usuario(usuario_id):
    try:
        usuario = Usuario.query.get(usuario_id)
        licencia = Licencia.query.get(usuario.licencia_id)

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({
            "email": usuario.email,
            "nombre": usuario.nombre,
            "licencia_fecha_fin":licencia.fecha_fin,
            "licencia_nombre":licencia.nombre_licencia,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500