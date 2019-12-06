"""
Flask app for the MoleGame
This contains the interface which we deal with
"""

"""
Flask app for the MoleRelay
"""
import atexit
import logging
from typing import Optional

import requests
from gevent.pywsgi import WSGIServer
from flask import Flask, make_response, request, send_from_directory
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

    @app.route('/')
    def index():
        password = request.cookies.get('password')
        if password == self.config.get_config_global('web_password'):
            return send_from_directory('web-config/config/', 'index.html')
        else:
            return redirect(url_for('login'))

    @app.route('/favicon.ico')
    def get_favicon():
        return send_from_directory('', 'favicon.ico')

    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory('web-config/config/js', path)

    @app.route('/css/<path:path>')
    def send_css(path):
        return send_from_directory('web-config/config/css', path)

    @app.route('/img/<path:path>')
    def send_img(path):
        return send_from_directory('web-config/config/img', path)

    return app


@atexit.register
def goodbye() -> None:
    """
    This routine is placed to prevent gevent from taking a long time to shutdown.
    """
    stop_app()
    logging.info('Killed server. Bye bye!')
