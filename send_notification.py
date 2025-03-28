import os
import requests
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

API_URL_NOTIFICATION = os.getenv("API_URL_NOTIFICATION")

if not API_URL_NOTIFICATION:
    print(f"[{datetime.now()}] ERROR: No se encontró 'API_URL' en el archivo .env.")
    exit(1)

def check_api():
    try:
        response = requests.post(API_URL_NOTIFICATION, timeout=10, verify=False)
        status_code = response.status_code

        if status_code == 200:
            print(f"[{datetime.now()}] Éxito: Código 200 recibido. No se volverá a ejecutar.")
            # Crear un archivo de bloqueo para evitar futuras ejecuciones
            with open("/tmp/api_info_detected.lock", "w") as lock_file:
                lock_file.write("success")
        else:
            print(f"[{datetime.now()}] Código {status_code}. Se ejecutará en el próximo intento.")

    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Error: {str(e)}. Se ejecutará en el próximo intento.")

if __name__ == "__main__":
    if os.path.exists("/tmp/api_info_detected.lock"):
        print(f"[{datetime.now()}] Información ya detectada. No se ejecutará nuevamente.")
        exit(0)
    print(f"[{datetime.now()}] Iniciando script de verificación en {API_URL_NOTIFICATION}")
    check_api()
