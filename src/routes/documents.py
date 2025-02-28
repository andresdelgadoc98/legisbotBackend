from flask import jsonify,Blueprint
from flask_cors import cross_origin
from dotenv import load_dotenv
import json
load_dotenv()
main = Blueprint('documents', __name__)
@main.route('', methods=['GET'])
@cross_origin(origin='*')
def response():
    ruta_archivo = 'db/db.json'
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        datos_folder = json.load(archivo)
    return jsonify(datos_folder),200
