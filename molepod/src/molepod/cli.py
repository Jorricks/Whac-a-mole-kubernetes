"""
Command line interface for the Molepod
"""

import logging
import click

from molepod.flask_service import start_app
from molepod.util import get_hostname

logger = logging.getLogger(__name__)


@click.group()
def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('Starting application')


@main.command("get-hostname")
def cli_get_hostname() -> None:
    """
    Gets our hostname
    """
    print(get_hostname())


@main.command("start")
@click.option("--port", default="8080", show_default=True)
def start_flask_app(port: int) -> None:
    """
    Start the flask app
    """
    logging.info('Starting flask app')
    start_app(port=port)


if __name__ == "__main__":
    main()
