import json
from src.utils.utils import retrival_fase,obtener_contexto_chunks_str,leer_txt,get_keywords,get_all_jurisprudencias
from string import Template
from dotenv import load_dotenv
import os
from openai import OpenAI
from flask import request
from db.db import Chat
import eventlet
from flask import current_app,copy_current_request_context

load_dotenv()
API_OPENIA =  os.getenv("OPENAI_API_KEY")
model_llm = os.getenv("MODEL_LLM")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_KEY")
GEMMA_KEY = os.getenv("GEMMA_KEY")
def init_socketio(socketio,app):
    @socketio.on('connect')
    def handle_connect():
        print('Cliente conectado')
        socketio.emit('message', 'Conexión establecida',to=request.sid)

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Cliente desconectado')

    @socketio.on('message')
    def handle_message(request_user):
        @copy_current_request_context
        def procesar_mensaje(data):
            with current_app.app_context():
                user_question = data['text']
                chat_id = data['chat_id']
                usuario_id = data['usuario_id']
                folder = data['folder']
                searchType = data['searchType']

                chat = Chat.query.get(chat_id)
                contexto_caso = chat.contexto if chat.contexto else ""

                client = OpenAI(api_key=GEMMA_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
                #client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")
                #client = OpenAI(api_key=API_OPENIA)
                if searchType == "documentos":
                    palabras_clave = get_keywords(user_question)["palabras"]
                    retrival = retrival_fase(palabras_clave, folder, 200)

                    context_string = obtener_contexto_chunks_str(retrival) if retrival else ""
                    print(context_string)
                    prompt_template = leer_txt('src/prompts/prompt_search_documents.txt')
                    template = Template(prompt_template)
                    prompt = template.substitute(
                        context_string=context_string,
                        user_question=user_question,
                    )
                elif searchType == "jurisprudencias":
                    jurisprudencias = get_all_jurisprudencias(user_question)
                    prompt_template = leer_txt('src/prompts/prompt_jurisprudencias.txt')
                    template = Template(prompt_template)
                    prompt = template.substitute(
                        context_caso=contexto_caso,
                        jurisprudencias=json.dumps(jurisprudencias),
                    )
                else:
                    prompt_template = leer_txt('src/prompts/prompt_general.txt')
                    template = Template(prompt_template)
                    prompt = template.substitute(
                        context_string="",
                        user_question=user_question,
                    )

                with open("prompt_generao.txt", "w", encoding="utf-8") as archivo:
                    archivo.write(prompt)

                completion = client.chat.completions.create(
                    model=model_llm,
                    messages=[{

                        "role": "system",
                        "content": "Eres un asistente juridico llamado Halach Contexto: " + contexto_caso
                    }, {
                        "role": "user",
                        "content": prompt
                    }],
                    stream=True
                )

                bot_response = ""
                for chunk in completion:
                    delta_content = chunk.choices[0].delta.content if chunk.choices[0].delta.content else ''
                    bot_response += delta_content
                    socketio.emit('response', delta_content, to=request.sid)
                    socketio.sleep(0)

                socketio.emit("response_end", to=request.sid)
                chat = Chat()
                chat.guardar_mensaje(chat_id, usuario_id, user_question, bot_response)

        data = json.loads(request_user)
        eventlet.spawn(procesar_mensaje, data)