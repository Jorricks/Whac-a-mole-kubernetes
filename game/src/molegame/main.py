""" Our main file """
import atexit
import os
import subprocess
import time
from typing import Tuple
from kubernetes import client

from molegame.flask_service import start_front_end
from molegame.pod_control import load_kubernetes_config, create_deployment_object, \
    create_deployment, delete_deployment, print_all_containers_in_pod
from molegame.whac_config import WhacConfig


def deploy_pods(
        whac_config: WhacConfig,
        apps_v1: client.AppsV1Api,
        no_replicas: int) -> None:
    """
    Starts our pods followed by starting our flask service.
    :param whac_config: All the static configurations required to run are in this instance.
    :param apps_v1: instance of client.AppsV1Api.
    :param no_replicas: Number of container in the pod.
    """
    deployment_relay = create_deployment_object(
        no_replicas=1,
        deployment_images=whac_config.deployment_image_relay,
        deployment_name=whac_config.deployment_name_relay,
        container_port=whac_config.containers_port,
        external_port=True)
    deployment_mole = create_deployment_object(
        no_replicas=no_replicas,
        deployment_images=whac_config.deployment_image_mole,
        deployment_name=whac_config.deployment_name_mole,
        container_port=whac_config.containers_port,
        external_port=False)

    create_deployment(
        api_instance=apps_v1, deployment=deployment_relay, namespace=whac_config.namespace)
    create_deployment(
        api_instance=apps_v1, deployment=deployment_mole, namespace=whac_config.namespace)


def run_whac_a_mole(
        whac_config: WhacConfig,
        no_replicas: int,
) -> None:
    """
    Starts our pods, creates an exit handler to delete them at exit and starts our flask service.
    :param whac_config: All the static configurations required to run are in this instance.
    :param no_replicas: Number of container in the pod.
    """
    load_kubernetes_config(whac_config.kubernetes_config)

    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()

    deploy_pods(
        whac_config=whac_config,
        apps_v1=apps_v1,
        no_replicas=no_replicas,
    )

    # When we shut down our program, this is always ran!
    atexit.register(delete_deployment,
                    api_instance=apps_v1,
                    deployment_names=whac_config.deployment_names,
                    namespace=whac_config.namespace)

    time.sleep(5)

    print_all_containers_in_pod(
        core_instance=core_v1, deployment_name=whac_config.deployment_name_mole)

    start_front_end(whac_config=whac_config, core_v1=core_v1, apps_v1=apps_v1)


def get_deployment_names(deployment_name: str) -> Tuple[str, str]:
    return deployment_name + '-mole-prod', deployment_name + '-relay-prod'


def get_project_folder(project_dir: str) -> str:
    """
    Finds the project folder by looking at the parents of the current working dir and
    comparing this to our project directory name.
    :param project_dir: the project directory name
    """
    from pathlib import Path
    d = Path().resolve()
    while d.as_posix().split('/')[-1] != project_dir:
        d = d.parent
    return d.as_posix()


def get_correct_config_folder(project_dir: str) -> str:
    """
    Finds the correct config folder by looking at the parents of the current working dir and
    comparing this to our project directory.
    :param project_dir: the project directory name
    """
    return get_project_folder(project_dir=project_dir) + '/.kube/config'


def get_minikube_ip(project_dir: str) -> str:
    """
    Finds the minikube ip with the help of our project directory name
    :param project_dir: the project directory name
    """
    p = get_project_folder(project_dir=project_dir)

    d = dict(os.environ)  # Copy current dir after which we add our required records.
    d['MINIKUBE_HOME'] = p
    d['KUBECONFIG'] = p + '/.kube/config'
    output = subprocess.check_output(['minikube', 'ip'], env=d)
    return str(output.decode()).replace('\n', '')


if __name__ == '__main__':
    project_dir_name = 'whac-a-mole-kubernetes'

    our_whac_config = WhacConfig(
        kubernetes_config=get_correct_config_folder(project_dir_name),
        deployment_image_mole='molepodprod',
        deployment_image_relay='molerelayprod',
        deployment_name='mole',
        namespace='whac',
        minikube_ip=get_minikube_ip(project_dir_name),
        containers_port=8080,
        host_port=80
    )

    run_whac_a_mole(whac_config=our_whac_config, no_replicas=3)
