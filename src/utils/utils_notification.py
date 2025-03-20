import requests
from datetime import datetime, timedelta
from firebase_admin import credentials, messaging, initialize_app
import requests


def get_next_friday():
    today = datetime.now()
    days_until_friday = (4 - today.weekday()) % 7
    if days_until_friday == 0:
        days_until_friday = 7
    elif days_until_friday < 0 or (days_until_friday == 0 and today.weekday() == 4):
        days_until_friday += 7
    next_friday = today + timedelta(days=days_until_friday)
    return next_friday


def generate_year_week(date):
    year = date.strftime("%Y")
    week_number = date.strftime("%U")
    if len(week_number) == 1:
        week_number = f"0{week_number}"
    return f"{year}{week_number}"


def check_jurisprudencias(year_week):
    external_url = "https://sjfsemanal.scjn.gob.mx/services/sjftesismicroservice/api/public/tesis?page=0&size=20&isSJFSemanal=true"

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

    return transformed_response
