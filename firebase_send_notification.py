from firebase_admin import credentials, messaging, initialize_app

cred = credentials.Certificate('halachia-afd77-firebase-adminsdk-fbsvc-5a8b00edd7.json')
initialize_app(cred)

registration_token = "d6iFG7qkjebNAYM99JpCVn:APA91bHg-rF2nvq51Gq3CYFhhvTCJhrKPuuHY0IxW6_sdU19bRK_7zSCDcJ4OiVigjTgnp94FuUZCG92bKwRQsycXaivFkw9zz-J-6-A8bCsxCtTFfYeY-U"

message = messaging.Message(
    notification=messaging.Notification(
        title='Título de la Notificación',
        body='Este es el cuerpo de la notificación.',
    ),
    token=registration_token,
)

response = messaging.send(message)
print('Successfully sent message:', response)
