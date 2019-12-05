"""
Flask app for the Molepod
"""
import atexit
import logging
from typing import Optional, Callable

from gevent.pywsgi import WSGIServer
from flask import Flask, make_response

from molepod.util import get_hostname

server: Optional[WSGIServer] = None


def start_app(port: int = 8080) -> None:
    global server
    server = WSGIServer(('0.0.0.0', int(port)), get_flask_app(stop_app))
    logging.info(f'Starting webserver at port {port}')
    server.serve_forever()


def stop_app() -> None:
    if server is not None:
        logging.info('Stopping webserver')
        server.stop()


def get_flask_app(shutdown_routine: Callable[[], None]) -> Flask:
    app = Flask(__name__)
    killed = False
    request = 0
    hostname = get_hostname()

    def log_make_response(message, code) -> str:
        logging.info(f'Code: {code}, Message: {message}')
        return make_response(message, code)

    @app.route('/health')
    def health_check() -> str:
        """
        How is our health doing
        :return:
        """
        nonlocal request

        if killed:
            return log_make_response(f'I am dead {hostname} :(!', 503)

        request += 1
        return log_make_response(f'Hello {request} from {hostname}!', 200)

    @app.route('/kill')
    def kill() -> str:
        """
        We kill part of our web server functionality but don't kill our full web app yet.
        """
        nonlocal killed

        killed = True
        return log_make_response(f'Killed {hostname}', 200)

    @app.route('/shutdown')
    def shutdown() -> str:
        """
        Complete shutdown of our web server
        """
        shutdown_routine()
        return log_make_response(f'Received shutdown request for {hostname}', 200)

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
    start_app(port=12340)
