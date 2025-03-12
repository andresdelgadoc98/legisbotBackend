from flask import request, jsonify, Blueprint
from db.db import Licencia,db
from flask_cors import cross_origin
from datetime import datetime
from uuid import UUID

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


@main.route('<string:id>', methods=['PUT'])
def editar_licencia(id):
    try:
        id_licencia = UUID(id)
    except ValueError:
        return jsonify({"error": "ID de licencia no válido"}), 400

    licencia = Licencia.query.get(id_licencia)
    if not licencia:
        return jsonify({"error": "Licencia no encontrada"}), 404

    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400

    if "nombreLicencia" in datos:
        licencia.nombre_licencia = datos["nombreLicencia"]
    if "fechaInicio" in datos:
        licencia.fecha_inicio = datetime.strptime(datos["fechaInicio"], "%Y-%m-%d").date()
    if "fechaFin" in datos:
        licencia.fecha_fin = datetime.strptime(datos["fechaFin"], "%Y-%m-%d").date()
    if "estado" in datos:
        licencia.estado = datos["estado"]

    db.session.commit()

    return jsonify({
        "id": licencia.id,
        "estado":  licencia.estado,
        "nombre_licencia": licencia.nombre_licencia,
        "fecha_inicio": licencia.fecha_inicio.isoformat(),
        "fecha_fin": licencia.fecha_fin.isoformat(),
        "fecha_creacion": licencia.fecha_creacion.isoformat()
    }), 200
