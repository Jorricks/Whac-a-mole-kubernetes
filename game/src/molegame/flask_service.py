"""
Flask app for the MoleRelay
This contains the interface which our front-end is built on.
"""
import requests
from kubernetes.client import CoreV1Api, AppsV1Api
from requests import Timeout

from molegame.pod_control import update_no_replicas_in_deployment, \
    get_containers_in_pod
import atexit
import logging
from typing import Optional

from gevent.pywsgi import WSGIServer
from flask import Flask, send_from_directory, jsonify, request, make_response

from molegame.whac_config import WhacConfig

server: Optional[WSGIServer] = None


def start_front_end(whac_config: WhacConfig, core_v1: CoreV1Api, apps_v1: AppsV1Api) -> None:
    global server
    server = WSGIServer(('0.0.0.0', int(whac_config.host_port)), get_flask_app(
        whac_config=whac_config, core_v1=core_v1, apps_v1=apps_v1
    ))

    logging.info(f'Starting webserver at port {whac_config.host_port}')
    server.serve_forever()


def stop_front_end() -> None:
    if server is not None:
        logging.info('Stopping webserver')
        server.stop()


def get_flask_app(whac_config: WhacConfig, core_v1: CoreV1Api, apps_v1: AppsV1Api) -> Flask:
    app = Flask(__name__)

    @app.route('/')
    def index():
        return send_from_directory('../resources/', 'index.html')

    @app.route('/favicon.ico')
    def get_favicon():
        return send_from_directory('../resources/', 'favicon.ico')

    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory('../resources/js', path)

    @app.route('/css/<path:path>')
    def send_css(path):
        return send_from_directory('../resources/css', path)

    @app.route('/fonts/<path:path>')
    def send_fonts(path):
        return send_from_directory('../resources/fonts', path)

    @app.route('/img/<path:path>')
    def send_img(path):
        return send_from_directory('../resources/img', path)

    @app.route('/get_pod_info')
    def get_pods():
        return jsonify(
            [container_status.to_dict() for container_status in
             get_containers_in_pod(
                 core_instance=core_v1,
                 deployment_name=whac_config.deployment_name_mole)]
        )

    @app.route('/get_relay_info')
    def get_relay_info():
        return jsonify(
            {'url': 'http://' + str(whac_config.minikube_ip)
                    + ':' + str(whac_config.containers_port)}
        )

    @app.route('/update_no_replicas')
    def update_replicas():
        new_no_replicas = int(request.args.get('no_replicas'))

        update_no_replicas_in_deployment(
            whac_config=whac_config, apps_v1=apps_v1, new_no_replicas=new_no_replicas)
        return jsonify({'Done': f'Changed no_replicas to {str(new_no_replicas)}'})

    @app.route('/relay')
    def relay_message() -> str:
        """
        Relay a message
        :return: The message we got from the container at ip:port/link.
        """
        url = 'http://' + str(whac_config.minikube_ip) + ':' + str(whac_config.containers_port)

        payload = {
            'ip': request.args.get('ip', default=''),
            'port': request.args.get('port', default=''),
            'link': request.args.get('link', default=''),
        }
        if payload['ip'] == '' or payload['port'] == '' or payload['link'] == '':
            return make_response(f"Invalid request: {str(payload)}", 400)

        try:
            a_request = requests.get(url, params=payload, timeout=1.2)
            return make_response(a_request.text, a_request.status_code)
        except Timeout:
            return make_response(f'Timeout for relay message with payload: {str(payload)}', 500)

    return app


@atexit.register
def goodbye() -> None:
    """
    This routine is placed to prevent gevent from taking a long time to shutdown.
    """
    stop_front_end()
    logging.info('Killed server. Bye bye!')
