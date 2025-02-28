from src.utils.utils import retrival_fase,obtener_contexto_chunks_str,leer_txt,get_chat_response_openia
from string import Template

user_question = "¿quienes son las personas física?"




retrival = retrival_fase(user_question,200)
context_string = obtener_contexto_chunks_str(retrival)
prompt_template = leer_txt('prompt.txt')
template = Template(prompt_template)
prompt = template.substitute(
    context_string=context_string,
    user_question=user_question,
)

response = get_chat_response_openia(prompt)
