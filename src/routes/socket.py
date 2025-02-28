import json
from src.utils.utils import retrival_fase,obtener_contexto_chunks_str,leer_txt,get_keywords
from string import Template
from dotenv import load_dotenv
import os
from openai import OpenAI
from flask import request
load_dotenv()
API_OPENIA =  os.getenv("OpenAI_KEY")
model_llm = os.getenv("MODEL_LLM")

def init_socketio(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Cliente conectado')
        socketio.emit('message', 'Conexión establecida',to=request.sid)

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Cliente desconectado')

    @socketio.on('message')
    def handle_message(request_user):
        data = json.loads(request_user)
        user_question = data['text']
        folder = data['folder']

        client = OpenAI(api_key=API_OPENIA)
        palabras_clave = get_keywords(user_question)
        retrival = retrival_fase(palabras_clave,folder,200)
        context_string = obtener_contexto_chunks_str(retrival)
        prompt_template = leer_txt('prompt.txt')
        template = Template(prompt_template)
        prompt = template.substitute(
            context_string=context_string,
            user_question=user_question,
        )

        with open("prompt_generao.txt", "w", encoding="utf-8") as archivo:
            archivo.write(prompt)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
           stream=True
        )

        for chunk in completion:
            delta_content = chunk.choices[0].delta.content if chunk.choices[0].delta.content else ''
            socketio.emit('response', delta_content,to=request.sid)
            socketio.sleep(0)

        socketio.emit("response_end",to=request.sid)
