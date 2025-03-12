from flask import request, jsonify, Blueprint
from db.db import Licencia,db
from flask_cors import cross_origin
from datetime import datetime


main = Blueprint('licencias', __name__)

@main.route("", methods=["POST"])
@cross_origin(origin='*')
def crear_licencia():
    data = request.get_json()
    nueva_licencia = Licencia(
        nombre_licencia=data["nombreLicencia"],
        fecha_inicio=datetime.strptime(data["fechaInicio"], "%Y-%m-%d"),
        fecha_fin=datetime.strptime(data["fechaFin"], "%Y-%m-%d"),
    )
    db.session.add(nueva_licencia)
    db.session.commit()
    return jsonify({"mensaje": "Licencia creada exitosamente", "id": nueva_licencia.id}), 201

@main.route("<string:id>", methods=["PUT"])
def editar_licencia(id):
    data = request.get_json()
    licencia = Licencia.query.get_or_404(id)
    licencia.nombre_licencia = data.get("nombre_licencia", licencia.nombre_licencia)
    licencia.fecha_inicio = datetime.strptime(data.get("fecha_inicio"), "%Y-%m-%d") if data.get("fecha_inicio") else licencia.fecha_inicio
    licencia.fecha_fin = datetime.strptime(data.get("fecha_fin"), "%Y-%m-%d") if data.get("fecha_fin") else licencia.fecha_fin
    db.session.commit()
    return jsonify({"mensaje": "Licencia actualizada exitosamente"}), 200

@main.route("<string:id>", methods=["GET"])
def obtener_licencia(id):
    licencia = Licencia.query.get_or_404(id)
    return jsonify({
        "id": licencia.id,
        "nombre_licencia": licencia.nombre_licencia,
        "fecha_inicio": licencia.fecha_inicio.strftime("%Y-%m-%d"),
        "fecha_fin": licencia.fecha_fin.strftime("%Y-%m-%d"),
        "fecha_creacion": licencia.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
    }), 200


@main.route("/", methods=["GET"])
def obtener_licencias():
    licencias = Licencia.query.all()
    return jsonify([{
        "id": licencia.id,
        "nombre_licencia": licencia.nombre_licencia,
        "fecha_inicio": licencia.fecha_inicio.strftime("%Y-%m-%d"),
        "fecha_fin": licencia.fecha_fin.strftime("%Y-%m-%d"),
        "fecha_creacion": licencia.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
    } for licencia in licencias]), 200