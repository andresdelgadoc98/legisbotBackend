import requests
import json

def getJurisprudenciasInitial(key_words, page):
    url = "https://sjf2.scjn.gob.mx/services/sjftesismicroservice/api/public/tesis?page=" + str(page) + "&size=20"
    body = {
        "classifiers": [
            {"name": "idEpoca", "value": ["200", "100", "5"], "allSelected": False, "visible": False,"isMatrix": False},
            {"name": "numInstancia", "value": ["6", "1", "2", "60", "50", "7"], "allSelected": False, "visible": False,"isMatrix": False},
            {"name": "idTipoTesis", "value": ["1"], "allSelected": False, "visible": False, "isMatrix": False},
            {"name": "tipoDocumento", "value": ["1"], "allSelected": False, "visible": False, "isMatrix": False}
        ],
        "searchTerms": [
            {
                "expression": key_words,
                "fields": ["localizacionBusqueda", "rubro", "texto"],
                "fieldsUser": "Localización: \nRubro (título y subtítulo): \nTexto: \n",
                "fieldsText": "Localización, Rubro (título y subtítulo), Texto",
                "operator": 0,
                "operatorUser": "Y",
                "operatorText": "Y",
                "lsFields": [],
                "esInicial": True,
                "esNRD": False
            }
        ],
        "bFacet": True,
        "ius": [],
        "idApp": "SJFAPP2020",
        "lbSearch": [
            "11a. Época - Todas las Instancias",
            "10a. Época - Todas las Instancias",
            "9a. Época - Todas las Instancias"
        ],
        "filterExpression": ""
    }

    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(body), headers=headers)
    totalPage = 0
    documents = []
    if response.status_code == 200:
        data = response.json()
        totalPage = data['totalPage']

        for document in data['documents']:

            documents.append({"ius": document['ius'], "rubro": document['rubro']})
    return {"total_page": totalPage, "documents": documents}

def get_all_jurisprudencias(key_words):
    page = 0
    all_documents = []
    while True:
        result = getJurisprudenciasInitial(key_words, page)
        all_documents.extend(result['documents'])
        if page >= result['total_page']:
            break
        page += 1
    return all_documents[:100]

key_words = "INTERES SUPERIOR DEL MENOR"
all_documents = get_all_jurisprudencias(key_words)
print(f"Total de documentos obtenidos: {len(all_documents)}")