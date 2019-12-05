import click

from molegame.main import start_kubernetes


@click.command()
@click.option('--config_file', default='', help='config to the our .kube config file')
@click.option('--image_name', default='molerelayprod', help='the name of the image we should launch')
@click.option('--replication', default=1, help='number of containers')
def hello(config_file: str, image_name: str, replication: int) -> None:
    load_kubernetes_config(config_file)
    start_kubernetes(image_name, replication)
