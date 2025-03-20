import requests
import time
import logging
from datetime import datetime

# Configurar logging para registrar los intentos
logging.basicConfig(
    filename='/var/log/api_retry.log',  # Ruta del log en el servidor
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# URL de la API (ajústala según tu endpoint)
API_URL = "https://www.saturnodelgado.com:5002/api/notification/send_notifications"

def check_api():
    while True:
        try:

            response = requests.get(API_URL, timeout=10)  # Timeout de 10 segundos
            status_code = response.status_code
            logging.info(f"Intento a {API_URL} - Código de estado: {status_code}")

            # Si el código es 200, salir del bucle
            if status_code == 200:
                logging.info(f"Éxito: Respuesta 200 recibida. Contenido: {response.json()}")
                print(f"[{datetime.now()}] Éxito: Código 200 recibido.")
                break
            else:
                logging.warning(f"Respuesta no exitosa: {status_code}. Reintentando en 30 minutos...")
                print(f"[{datetime.now()}] Código {status_code}. Reintentando en 30 minutos...")

        except requests.exceptions.RequestException as e:
            # Manejar errores de conexión u otros problemas
            logging.error(f"Error en la petición: {str(e)}. Reintentando en 30 minutos...")
            print(f"[{datetime.now()}] Error: {str(e)}. Reintentando en 30 minutos...")

        # Esperar 30 minutos (1800 segundos)
        time.sleep(1800)

if __name__ == "__main__":
    print(f"[{datetime.now()}] Iniciando script de reintentos a {API_URL}")
    check_api()