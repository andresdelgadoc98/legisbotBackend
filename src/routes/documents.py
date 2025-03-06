from flask import jsonify,Blueprint,send_file,abort
from flask_cors import cross_origin
from dotenv import load_dotenv
import json
import os



load_dotenv()
main = Blueprint('documents', __name__)

@main.route('', methods=['GET'])
@cross_origin(origin='*')
def response():
    ruta_archivo = 'db/db.json'
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        datos_folder = json.load(archivo)
    return jsonify(datos_folder),200

@main.route('/documentos/<nombre_documento>', methods=['GET'])
def ver_documento(nombre_documento):
    try:
        # Construir la ruta completa del documento
        file = os.path.join(os.getcwd(), "db/pdfs/", nombre_documento)
        print(file)
        # Verificar si el archivo existe
        if not os.path.exists(file):
            abort(404, description="Documento no encontrado")

        # Enviar el archivo como respuesta
        return send_file(file, as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500