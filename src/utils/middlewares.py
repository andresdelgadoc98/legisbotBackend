import os
import requests
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify
import jwt
SECRET_KEY = os.getenv("SECRET_KEY")



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
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
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