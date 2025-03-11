from waitress import serve
from app import app

if __name__ == '__main__':
    # Configure Waitress server
    serve(
        app,
        host='0.0.0.0',  # Listen on all available network interfaces
        port=3000,       # Port to run the server on
        threads=4,       # Number of worker threads
        url_scheme='http'
    )
