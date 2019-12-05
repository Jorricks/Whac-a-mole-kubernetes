import threading
from typing import Tuple, Optional

import requests
import pytest

from molerelay import start_app, stop_app


class APIServiceThread(threading.Thread):
	"""
	A helper to launch the Flask service.
	"""
	def __init__(self, port: int, *args, **kwargs):
		super(APIServiceThread, self).__init__(*args, **kwargs)
		self.port = port

	def run(self):
		start_app(self.port)

	@staticmethod
	def stop():
		stop_app()


@pytest.fixture
def launch_api_get_url() -> str:
	port = 12345
	api_service_thread = APIServiceThread(port)
	api_service_thread.run()
	yield f'http://localhost:{port}/'
	api_service_thread.stop()


def make_request(launch_api_get_url: str, endpoint: str) -> Tuple[int, Optional[str]]:
	try:
		request = requests.get(launch_api_get_url + endpoint)
		return request.status_code, request.text
	except requests.exceptions.ConnectionError:
		return 0, None


def test_relay(launch_api_get_url) -> None:
	assert 200, _ == make_request(launch_api_get_url, 'health')


def test_kill(launch_api_get_url) -> None:
	pass


def test_health_after_kill(launch_api_get_url) -> None:
	pass


def test_shutdown(launch_api_get_url) -> None:
	pass


def test_health_after_shutdown(launch_api_get_url) -> None:
	pass
