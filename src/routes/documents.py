from flask import jsonify,Blueprint,send_file,abort
from flask_cors import cross_origin
from dotenv import load_dotenv
import json
import os
from src.utils.middlewares import token_required
from flask import request, jsonify, Blueprint
from db.db import Documento,db
import requests
from src.utils.utils_notification import check_jurisprudencias

load_dotenv()
main = Blueprint('documents', __name__)
"""
@main.route('', methods=['GET'])
@cross_origin(origin='*')
@token_required
def response():
    ruta_archivo = 'db/db.json'
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        datos_folder = json.load(archivo)
    return jsonify(datos_folder),200
"""


def get_URL(jurisdiccion,file):
    URL =""
    if(jurisdiccion == "tamaulipas"):
        URL = "https://www.congresotamaulipas.gob.mx/" + file
    elif(jurisdiccion == "federal"):
        URL = "https://www.diputados.gob.mx/LeyesBiblio/" + file

    return URL

@main.route('/documentos/<jurisdiccion>/<nombre_documento>', methods=['GET'])
def ver_documento(jurisdiccion,nombre_documento):
    try:
        print(jurisdiccion)
        print(nombre_documento)
        file = os.path.join(os.getcwd(),"db/documents/",jurisdiccion, nombre_documento)

        if not os.path.exists(file):
            abort(404, description="Documento no encontrado")
        return send_file(file, as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('', methods=['GET'])
def filtrar_por_jurisdiccion():
    jurisdiccion = request.args.get('jurisdiccion')

    if not jurisdiccion:
        return jsonify({"error": "El parámetro 'jurisdiccion' es requerido"}), 400
    documentos = Documento.query.filter_by(jurisdiccion=jurisdiccion).all()
    if not documentos:
        return jsonify({"message": "No se encontraron documentos para la jurisdicción especificada"}), 404

    resultados = [{
        "uuid": str(doc.uuid),
        "name": doc.titulo,
        "fecha_publicacion": doc.fecha_publicacion.isoformat() if doc.fecha_publicacion else None,
        "folder": doc.folder,
        "file": doc.ruta_actualizada,
        "jurisdiccion": doc.jurisdiccion
    } for doc in documentos]

    return jsonify(resultados), 200

@main.route('/jurisprudencias', methods=['POST'])
def get_jurisprudencias():
    try:
        data = request.get_json() or {}
        year_week = data.get("yearWeek", "")
        transformed_response =  check_jurisprudencias(year_week)
        return jsonify(transformed_response), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

