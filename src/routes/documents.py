from flask import jsonify,Blueprint,send_file,abort
from flask_cors import cross_origin
from dotenv import load_dotenv
import json
import os
from src.utils.middlewares import token_required
from flask import request, jsonify, Blueprint
from db.db import Documento,db
import requests
from datetime import datetime

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
        external_url = "https://sjfsemanal.scjn.gob.mx/services/sjftesismicroservice/api/public/tesis?page=0&size=20&isSJFSemanal=true"
        data = request.get_json() or {}
        year_week = data.get("yearWeek", "")
        payload = {
            "classifiers": [],
            "searchTerms": [
                {
                    "expression": year_week,
                    "fields": ["semana"],
                    "fieldsUser": "",
                    "fieldsText": "",
                    "operator": 1,
                    "operatorUser": "O",
                    "operatorText": "O",
                    "lsFields": [],
                    "esInicial": False,
                    "noHighlight": False,
                    "excludeTerms": True
                }
            ],
            "bFacet": True,
            "idApp": "SJFSEMANAL",
            "lbSearch": [],
            "filterMatrix": [
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["1"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["6"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 6
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["1"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["60"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 60
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["1"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["1"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 1
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["1"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["2"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 2
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["1"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["50"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 50
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["1"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["7"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 7
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["0"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["6"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 6
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["0"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["60"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 60
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["0"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["1"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 1
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["0"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["2"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 2
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["0"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["50"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 50
                },
                {
                    "filters": [
                        {"name": "idTipoTesis", "value": ["0"], "allSelected": False, "visible": False,
                         "isMatrix": False},
                        {"name": "numInstancia", "value": ["7"], "allSelected": False, "visible": False,
                         "isMatrix": False}
                    ],
                    "instancia": 7
                }
            ],
            "filterExpression": ""
        }
        response = requests.post(
            external_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()

        transformed_documents = [
            {
                "id": doc["id"],
                "title": doc["rubro"],
                "date": datetime.strptime(doc["fechaPublicacion"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d"),
                "summary": "No viola el principio de proporcionalidad del artículo 22 constitucional." if doc[
                                                                                                              "id"] == "2030098" else "Resumen no disponible",
                # Ejemplo, puedes personalizar esto
                "source": f"{doc['instanciaAbr']}; {doc['epocaAbr']}; {doc['fuente']}; {doc['claveTesis']}; {'J' if doc['ta_tj'] == 1 else 'TA'}; Publicación: {doc['textoPublicacion'].split(' y,')[0]}"
            }
            for doc in data["documents"]
        ]

        transformed_response = {
            "documents": transformed_documents,
            "classifiers": data["classifiers"],
            "total": data["total"],
            "totalPage": data["totalPage"]
        }

        return jsonify(transformed_response), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

