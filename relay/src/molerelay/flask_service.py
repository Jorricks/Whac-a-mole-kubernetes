"""
Flask app for the MoleRelay
"""
import atexit
import logging
from typing import Optional

import requests
from gevent.pywsgi import WSGIServer
from flask import Flask, make_response, request
from requests import Timeout

server: Optional[WSGIServer] = None


def start_app(port: int = 8080) -> None:
    global server
    server = WSGIServer(('0.0.0.0', int(port)), get_flask_app())
    logging.info(f'Starting webserver at port {port}')
    server.serve_forever()


def stop_app() -> None:
    if server is not None:
        logging.info('Stopping webserver')
        server.stop()


def get_flask_app() -> Flask:
    app = Flask(__name__)

    def log_make_response(message, code) -> str:
        logging.info(f'Code: {code}, Message: {message}')
        return make_response(message, code)

    @app.route('/')
    def relay_message() -> str:
        """
        Relay a message
        :return: The message we got from the other cluster.
        """

        ip = request.args.get('ip', default='')
        port = request.args.get('port', default='')
        link = request.args.get('link', default='')
        if ip == '' or port == '' or link == '':
            return log_make_response(f"Invalid request: ip:{ip}, port:{port}, link:{link}", 400)

        try:
            a_request = requests.get(f"http://{ip}:{port}/{link}", timeout=1)
            return log_make_response(a_request.text, a_request.status_code)

        except Timeout:
            return log_make_response(f'Timeout for http://{ip}:{port}/{link}', 500)

    return app


@atexit.register
def goodbye() -> None:
    """
    This routine is placed to prevent gevent from taking a long time to shutdown.
    """
    stop_app()
    logging.info('Killed server. Bye bye!')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_app(port=12345)
