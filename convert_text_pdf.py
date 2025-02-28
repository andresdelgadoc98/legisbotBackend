from src.utils.utils import leer_txt,dict_to_embeddings,extract_text_with_ocr
import re

#extract_text_with_ocr("db/pdfs/Codigo_Proced_Civil.pdf", "db/pdfs/Codigo_Proced_Civil.txt")


def convertir_a_diccionario(articulos):
    diccionario_articulos = {}

    for articulo in articulos:
       #pattern_trabajo = r'Articulo\s+(\d+)\.-?'

        pattern = r'ARTICULO\s+(\d+)\.-'
        match = re.search(pattern, articulo)
        if match:
            numero = int(match.group(1))
            contenido = articulo.strip()
            tamaño = len(contenido)
            diccionario_articulos[numero] = {
                'content': contenido,
                'tamaño': tamaño
            }

    return diccionario_articulos

def extraer_numero_articulo(contenido):
    pattern_trabajo =r'Articulo (\d+)\.-'
    pattern = r'ARTICULO\s+(\d+)\.-'
    match = re.search(pattern, contenido)
    if match:
        return int(match.group(1))
    return None

def agregar_numero_articulo(diccionario):
    for key, articulo in diccionario.items():
        contenido = articulo['content']
        numero_articulo = extraer_numero_articulo(contenido)
        articulo['articulo'] = numero_articulo  # Agrega el número de artículo
    return diccionario

def superan_umbral(tamaños, umbral):
    resultados = []

    for indice, tamaño in enumerate(tamaños):
        if tamaño > umbral:
            resultados.append((indice - 1, tamaño))

    return resultados

texto = leer_txt("db/texts/Codigo_Proced_Civil.txt")
tamaño_texto = len(texto)
#pattern = r'(Articulo\s+\d+\.-?.*?)(?=\s*Articulo\s+\d+\.-?|$)'
pattern = r'(ARTICULO\s+\d+\.-.*?)(?=\s*ARTICULO\s+\d+\.-|$)'
articulos = re.findall(pattern, texto, flags=re.DOTALL)
articulos_limpios = [articulo.strip().replace('\n', ' ') for articulo in articulos]
diccionario = convertir_a_diccionario(articulos_limpios)
diccionario_actualizado = agregar_numero_articulo(diccionario)
dict_to_embeddings(diccionario_actualizado)
