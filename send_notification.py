import requests
import time

from datetime import datetime


API_URL = "https://saturnodelgado.com:5002/api/notification/send_notifications"

def check_api():
    while True:
        try:
            response = requests.post(API_URL, timeout=10, verify=False)
            status_code = response.status_code

            # Si el código es 200, salir del bucle
            if status_code == 200:
                print(f"[{datetime.now()}] Éxito: Código 200 recibido.")
                break
            else:

                print(f"[{datetime.now()}] Código {status_code}. Reintentando en 30 minutos...")

        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now()}] Error: {str(e)}. Reintentando en 30 minutos...")

        time.sleep(1800)

if __name__ == "__main__":
    print(f"[{datetime.now()}] Iniciando script de reintentos a {API_URL}")
    check_api()