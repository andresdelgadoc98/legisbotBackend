import requests
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

LOCAL_API_URL = "https://localhost:5002/api/documents/jurisprudencias"

def get_next_friday():
    today = datetime.now()
    days_until_friday = (4 - today.weekday()) % 7
    if days_until_friday == 0:
        days_until_friday = 7
    elif days_until_friday < 0 or (days_until_friday == 0 and today.weekday() == 4):
        days_until_friday += 7
    next_friday = today + timedelta(days=days_until_friday)
    return next_friday

def generate_year_week(date):
    year = date.strftime("%Y")
    week_number = date.strftime("%U")
    if len(week_number) == 1:
        week_number = f"0{week_number}"
    return f"{year}{week_number}"

def check_jurisprudencias(year_week):

    payload = {"yearWeek": year_week}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(LOCAL_API_URL, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()

        documents = data.get("documents", [])
        total = data.get("total", 0)
        if documents:
            return True,total
        else:
            logger.info(f"No se encontraron documentos para {year_week}. Reintentando...")
            return False,total

    except requests.exceptions.RequestException as e:
        logger.error(f"Error al realizar la solicitud: {str(e)}")
        return False,0

def run_check_until_success(year_week):
    max_attempts = 24
    attempt = 0

    while attempt < max_attempts:
        isDocuments, number_documents = check_jurisprudencias(year_week)
        if isDocuments:
            return isDocuments, number_documents
        else:
            return False, 0


next_friday = get_next_friday()
year_week = int(generate_year_week(next_friday)) + 0
result,total = run_check_until_success(year_week=year_week)

if result:
    from firebase_admin import credentials, messaging, initialize_app

    cred = credentials.Certificate('halachia-afd77-firebase-adminsdk-fbsvc-5a8b00edd7.json')
    initialize_app(cred)
    registration_token = "d6iFG7qkjebNAYM99JpCVn:APA91bHg-rF2nvq51Gq3CYFhhvTCJhrKPuuHY0IxW6_sdU19bRK_7zSCDcJ4OiVigjTgnp94FuUZCG92bKwRQsycXaivFkw9zz-J-6-A8bCsxCtTFfYeY-U"


    message = messaging.Message(
        notification=messaging.Notification(
            title='Jurisprudencias Nuevas',
            body=f'Se subieron {total} Jurisprudencias!',
        ),
        data={
            'url': 'https://localhost:3000/jurisprudencias?yearWeek=202511'
        },
        token=registration_token,
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)


