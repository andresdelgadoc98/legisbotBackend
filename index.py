import eventlet
eventlet.monkey_patch()
from src import create_app
from dotenv import load_dotenv
import os
import ssl

load_dotenv()
PORT = os.getenv("PORT")
mode = os.getenv('MODE', 'development')
app = create_app()

if __name__ == '__main__':
    if mode == 'production':
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile="src/certificates/certificate.crt", keyfile="src/certificates/private.key")

        eventlet.wsgi.server(
            eventlet.wrap_ssl(eventlet.listen(('0.0.0.0', int(PORT))),
                              #certfile="src/certificates/certificate.crt",
                              #keyfile="src/certificates/private.key",
                              certfile="src/certificates/server.crt",
                              keyfile="src/certificates/server.key",
                              server_side=True),
            app
        )
    else:
        eventlet.wsgi.server(
            eventlet.listen(('0.0.0.0', int(PORT))),
            app
        )
