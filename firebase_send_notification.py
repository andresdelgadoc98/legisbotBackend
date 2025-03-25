from firebase_admin import credentials, messaging, initialize_app

cred = credentials.Certificate('firebase.json')
initialize_app(cred)

registration_token = "fmD6HYTf9XlpETB7RPtkor:APA91bHbv89BZhhWP_x_Mt6wiTCnQYeGeoj5kgs4kMGM3c2BJfcoSxnAz2P8yC-w1-BNG3XpbtdNNVJ_oBVfShkXCHLymMsHTiphlUNQAoRWUjjydzFrQ1Q"
total = "10"
year_week = 202511
message = messaging.Message(
    notification=messaging.Notification(
        title="Jurisprudencias",
        body=f'Se Actualizaron {total} Jurisprudencias',
    ),
    data={
        'url': 'https://www.saturnodelgado.com/jurisprudencias?yearWeek=' + str(year_week)
    },
    token=registration_token,
)
response = messaging.send(message)
print('Successfully sent message:', response)
