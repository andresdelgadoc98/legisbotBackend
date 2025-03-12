from flask import request, jsonify, Blueprint
from flask_cors import cross_origin
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from src.utils.middlewares import validar_licencia

load_dotenv()

SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
SECRET_KEY_ACCESS = os.getenv("SECRET_KEY_ACCESS")
ACCESS_TOKEN_EXPIRATION = int(os.getenv("ACCESS_TOKEN_EXPIRATION"))


main = Blueprint('token', __name__)


@main.route("/refresh_token", methods=["POST"])
@cross_origin(origin='*', supports_credentials=True)
@validar_licencia
def get_acces_token():
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return jsonify({"error": "Refresh token no proporcionado"}), 403
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY_REFRESH, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Refresh token expirado"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Refresh token inválido"}), 403

        usuario_id = payload.get("sub")
        if not usuario_id:
            return jsonify({"error": "Refresh token inválido"}), 403

        access_token = jwt.encode(
            {
                "sub": usuario_id,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION),
            },
            SECRET_KEY_ACCESS,
            algorithm="HS256",
        )
        print("acces token refresh:",access_token)
        return jsonify({
            "mensaje": "Access token renovado exitosamente",
                "access_token": access_token,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/very_refresh_token", methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)

def very_refresh_token():
    try:
        refresh_token = request
        print("very_token", refresh_token)
        if not refresh_token:
            return jsonify({
                "message": "Token is missing",
                "statusCode": 403
            }), 403
        data = jwt.decode(refresh_token, SECRET_KEY_REFRESH, algorithms=["HS256"])
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

    return jsonify({
        "mensaje": "Token verificado exitosamente",
    }), 200


@main.route("/very_access_token", methods=["POST"])
@cross_origin(origin='*',supports_credentials=True)
def very_access_token():
    try:
        data = request.get_json()
        refresh_token = data.get("refresh_token")
        print("very_token", refresh_token)
        if not refresh_token:
            return jsonify({
                "message": "Token is missing",
                "statusCode": 403
            }), 403
        data = jwt.decode(refresh_token, SECRET_KEY_ACCESS, algorithms=["HS256"])
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

    return jsonify({
        "mensaje": "Token verificado exitosamente",
    }), 200