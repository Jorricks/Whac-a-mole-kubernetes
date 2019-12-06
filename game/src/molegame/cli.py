from typing import Optional

import click

from molegame.main import run_whac_a_mole


@click.command()
@click.option('--config_file', default=None, help='The path to our kubernetes .kube config file.')
@click.option('--replication', default=1, help='Number of replicas of the mole container.')
@click.option('--image_name_mole', default='molepodprod', help='The name of the mole pod image.')
@click.option('--image_name_relay', default='molerelayprod', help='The name of the relay image.')
@click.option('--deployment_name', default=1, help='Number of replicas of the mole container.')
@click.option('--namespace_prefix', default='whac', help='Prefix for the deployments namespace.')
@click.option('--port', default='8080', help='The port.')
def start_kubernetes(
        config_file: Optional[str],
        replication: int,
        image_name_mole: str,
        image_name_relay: str,
        deployment_name: str,
        namespace_prefix: str,
        port: int,
) -> None:
    run_whac_a_mole(
        kubernetes_config=config_file,
        no_replicas=int(replication),
        deployment_image_mole=str(image_name_mole),
        deployment_image_relay=str(image_name_relay),
        deployment_name=str(deployment_name),
        namespace=str(namespace_prefix),
        port=int(port)
    )
