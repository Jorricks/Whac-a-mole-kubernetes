"""
Command line interface for the MoleRelay
"""

import logging
import click

from molerelay.flask_service import start_app

logger = logging.getLogger(__name__)


@click.group()
def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('Starting application')


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
