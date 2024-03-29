from typing import Optional
import click

from molegame.main import run_whac_a_mole, get_minikube_ip
from molegame.whac_config import WhacConfig


@click.command()
@click.option('--config_file', default=None, help='The path to our kubernetes .kube config file.')
@click.option('--replication', default=1, help='Number of replicas of the mole container.')
@click.option('--image_name_mole', default='molepodprod', help='The name of the mole pod image.')
@click.option('--image_name_relay', default='molerelayprod', help='The name of the relay image.')
@click.option('--deployment_name', default=1, help='Number of replicas of the mole container.')
@click.option('--namespace_prefix', default='whac', help='Prefix for the deployments namespace.')
@click.option('--minikube_ip', default=None, help='The ip of minikube.')
@click.option('--containers_port', default='8080', help='The port of the containers.')
@click.option('--host_port', default='80', help='The port of the host computer (recommended = 80).')
@click.option('--keep_containers_alive', is_flag=True, help='Containers stay alive after shutdown.')
@click.option('--open_web_browser', is_flag=True, help='Open the web browser to the front-end.')
def start_kubernetes(
        config_file: Optional[str],
        replication: int,
        image_name_mole: str,
        image_name_relay: str,
        deployment_name: str,
        namespace_prefix: str,
        minikube_ip: Optional[str],
        containers_port: int,
        host_port: int,
        keep_containers_alive: bool,
        open_web_browser: bool,
) -> None:
    if minikube_ip is None:
        project_dir_name = 'whac-a-mole-kubernetes'
        minikube_ip = get_minikube_ip(project_dir=project_dir_name)

    our_whac_config = WhacConfig(
        kubernetes_config=config_file,
        deployment_image_mole=str(image_name_mole),
        deployment_image_relay=str(image_name_relay),
        deployment_name=str(deployment_name),
        namespace=str(namespace_prefix),
        minikube_ip=minikube_ip,
        containers_port=int(containers_port),
        host_port=int(host_port),
        keep_deployment_alive=bool(keep_containers_alive),
        open_web_browser=bool(open_web_browser)
    )

    run_whac_a_mole(whac_config=our_whac_config, no_replicas=replication)
