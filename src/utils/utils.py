from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from pdf2image import convert_from_path
embedding = OllamaEmbeddings(model='nomic-embed-text')
chunk_size = 450
from string import Template
from dotenv import load_dotenv
import os
from openai import OpenAI
import pytesseract

load_dotenv()
number_chunks = os.getenv('NUMBER_CHUNKS')
API_OPENIA   = os.getenv('OpenAI_KEY')

def pdf_to_txt(pdf_path, txt_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text()
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text_content)
        print(f"Conversión exitosa. Archivo guardado en: {txt_path}")
    except Exception as e:
        print(f"Error al convertir el PDF a TXT: {e}")


def txt_to_embeddings_2(name: str):
    db_path = "db/embeddings/"
    with open(name, 'r', encoding='utf-8') as file:
        text = file.read()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=int(chunk_size),chunk_overlap=25)
    chunks = text_splitter.split_text(text)
    documents = []
    for i,chunk in enumerate(chunks):
        metadata = {"article_number": i + 1}
        print(metadata)
        doc = Document(page_content=chunk, metadata=metadata)
        documents.append(doc)

    if not os.path.exists(db_path + 'ley federal'):
        print("guardando embeddings")
        chunks_vectorstore = FAISS.from_documents(documents, embedding=embedding)
        chunks_vectorstore.save_local("db/embeddings/" + 'ley federal')

    print("Se realizaron los chunks por artículo.")


def obtener_contexto_chunks_str(chunks):
    contexto_str = ""
    for doc in chunks:
        contenido = doc.page_content
        articulo = doc.metadata["article_number"]

        if isinstance(contenido, (list, tuple)):
            contenido = " ".join(map(str, contenido))
        else:
            contenido = str(contenido)
        contexto_str += f"\nArtículo {articulo}:\n{contenido}\n"

    return contexto_str.strip()

def retrival_fase(user_question: str,folder,k):

    directorio = "db/embeddings/" + str(folder)
    try:
        vectorstore = FAISS.load_local(directorio, embedding, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"Error cargando el vectorstore desde {directorio}: {e}")

    chunk_retriever = vectorstore.as_retriever(search_kwargs={"k": int(k)})
    resultados = chunk_retriever.invoke(user_question)
    return resultados

def leer_txt(nombre_archivo : str) -> str:
    with open(nombre_archivo, 'r', encoding='UTF-8') as archivo:
        contenido = archivo.read()
    return contenido

def get_chat_response_openia(content : str) -> str:
    client = OpenAI(api_key=API_OPENIA)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": str(content)
            }
        ]
    )

    return completion.choices[0].message.content


def extract_text_with_ocr(pdf_path,txt_path):
    text = ""
    pages = convert_from_path(pdf_path,first_page=0)
    for page_number, page_image in enumerate(pages):
        print("pagina numero: ",page_number)
        page_text = pytesseract.image_to_string(page_image)
        text += page_text + "\n"

    with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
    print(f"Conversión exitosa. Archivo guardado en: {txt_path}")
    return text


def dict_to_embeddings(articulos_dict, db_name="codigo_civil_procedimientos"):
    db_path = "db/embeddings/"
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=int(450),chunk_overlap=25)
    chunks_array = []
    for datos in articulos_dict.values():
        chunks = text_splitter.split_text(datos['content'])
        for chunk in chunks:
            metadata = {"article_number": datos['articulo']}
            doc = Document(page_content=chunk, metadata=metadata)
            chunks_array.append(doc)
        print(f"Artículo {datos['articulo']}")

    if not os.path.exists(db_path + db_name):
        print("Guardando embeddings...")
        chunks_vectorstore = FAISS.from_documents(chunks_array, embedding=embedding)
        chunks_vectorstore.save_local(db_path + db_name)
    else:
        print("Los embeddings ya existen. No se guardaron nuevos embeddings.")

    print("Se realizaron los embeddings por artículo.")

import json

def clean_json(response_text):
    cleaned_text = response_text.strip("```json").strip("```").strip()
    cleaned_text = cleaned_text.replace("'", '"')
    try:
        json_object = json.loads(cleaned_text)
        return json_object
    except json.JSONDecodeError as e:
        print(f"Error al convertir a JSON: {e}")
        return None

def get_keywords(user_question):
        prompt_template = leer_txt('src/prompts/key_word.txt')
        template = Template(prompt_template)
        prompt = template.substitute(
            user_question=user_question,
        )
        response = get_chat_response_openia(prompt)
        print(response)
        return ' '.join(clean_json(response))
