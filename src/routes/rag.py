from flask import request, jsonify,Blueprint
from flask_cors import cross_origin
from dotenv import load_dotenv
import os
from langchain_ollama import OllamaEmbeddings
from string import Template
from src.utils.utils import retrival_fase,obtener_contexto_chunks_str,leer_txt,get_chat_response_openia

load_dotenv()
main = Blueprint('response', __name__)
embedding_model = os.getenv("EMBEDDING_MODEL")
embedding = OllamaEmbeddings(model=embedding_model)

@main.route('generate', methods=['POST'])
@cross_origin(origin='*')
def response():
    data = request.json
    user_question = data.get('user_question', 'No user_question provided')
    #palabras_clave = extract_keywords(user_question)
    #print(palabras_clave)
    #retrival = retrival_fase(' '.join(palabras_clave))
    retrival = retrival_fase(user_question,50)
    context_string = obtener_contexto_chunks_str(retrival)
    prompt_template = leer_txt('prompt.txt')
    template = Template(prompt_template)
    prompt = template.substitute(
        context=context_string,
        user_question=user_question,
    )

    with open("prompt_generado.txt", "w") as file:
        file.write(prompt)

    return jsonify({"result": get_chat_response_openia(prompt)}),200
