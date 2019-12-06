import atexit
import time
from typing import Optional, List

from kubernetes import client, config
from kubernetes.client import CoreV1Api, AppsV1Api, V1Deployment, V1PodList, V1Pod, V1Container


def load_kubernetes_config(config_file: Optional[str]) -> None:
    """
    We load the kubernetes config and than the corresponding API into the global v1 variable.
    :param config_file: The path to the kubernetes config file.
    """
    if config_file is None or config_file == "":
        config.load_kube_config()
    else:
        config.load_kube_config(config_file=config_file)


def print_all_relevant_pods(core_instance: CoreV1Api, deployment_name: str) -> None:
    """
    We print all pods
    :param core_instance: Core API instance.
    :param deployment_name: The name of the deployment.
    """
    print('\n\n')
    print("Listing pods with their IPs:")
    ret: V1PodList = core_instance.list_pod_for_all_namespaces(watch=False)
    i: V1Pod
    for i in ret.items:
        if deployment_name not in str(i.metadata.name):
            continue
        # import pprint
        # pprint.pprint(i)
        # print(f"{}")
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


def create_container_object(deployment_image: str, port: int, external_port: bool) -> V1Container:
    """
    Create the container object
    :param deployment_image: The image name in the docker environment.
    :param port: port of the web_server.
    :param external_port: whether the port should be an external port.
    :return: The container object.
    """
    liveness_probe = client.V1Probe(
        http_get=client.V1HTTPGetAction(
            port=port,
            path='/health'
        ),
        initial_delay_seconds=5,
        failure_threshold=2,
        period_seconds=3,
    )

    readiness_probe = client.V1Probe(
        http_get=client.V1HTTPGetAction(
            port=port,
            path='/health'
        ),
        initial_delay_seconds=5,
        failure_threshold=2,
        period_seconds=3,
    )

    port = client.V1ContainerPort(
            container_port=port,
            host_ip='0.0.0.0',
            host_port=port,
            name='prt',
            protocol='TCP'
        ) if external_port else client.V1ContainerPort(
            container_port=port
        )

    return client.V1Container(
        name="molerelay",
        image=deployment_image,
        image_pull_policy="Never",
        ports=[port],
        liveness_probe=liveness_probe,
        readiness_probe=readiness_probe
    )


def create_deployment_object(
        no_replicas: int,
        deployment_images: str,
        deployment_name: str,
        port: int,
        external_port: bool,
) -> V1Deployment:
    """
    We create a deployment according to the specified arguments.
    :param no_replicas: Number of container in the pod.
    :param deployment_images: The image name in the docker environment for the moles.
    :param deployment_name: The name of the deployment.
    :param port: port of the web_server.
    :param external_port: whether the port should be an external port.
    :return: Deployment setup.
    """
    container = create_container_object(deployment_images, port, external_port)

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "molerelay"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=no_replicas,
        template=template,
        selector={'matchLabels': {'app': 'molerelay'}})
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=spec)

    return deployment


def create_deployment(api_instance: AppsV1Api, deployment: V1Deployment, namespace: str) -> None:
    """
    Instantiate the deployment.
    :param api_instance: The api instance.
    :param deployment: The deployment setup.
    :param namespace: The namespace in which the pods are deployed.
    """
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace=namespace)
    print("Deployment created.\n status=\n'%s'" % str(api_response.status))


# def update_deployment(
#         api_instance: AppsV1Api,
#         deployment: V1Deployment,
#         deployment_name: str,
#         namespace: str
# ) -> None:
#     """
#     Update our deployment
#     :param api_instance: The api instance.
#     :param deployment: The deployment setup.
#     :param deployment_name: The name of the deployment.
#     :param namespace: The namespace in which the pods are deployed.
#     """
#     # Update container image
#     deployment.spec.template.spec.containers[0].image = "nginx:1.16.0"
#     # Update the deployment
#     api_response = api_instance.patch_namespaced_deployment(
#         name=deployment_name,
#         namespace=namespace,
#         body=deployment)
#     print("Deployment updated.\n status=\n'%s'" % str(api_response.status))


def delete_deployment(api_instance: AppsV1Api, deployment_names: List[str], namespace: str) -> None:
    """
    Delete our deployment
    :param api_instance: The api instance
    :param deployment_names: The names of the deployments.
    :param namespace: The namespace in which the pods are deployed.
    """
    for deployment_name in deployment_names:
        api_response = api_instance.delete_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
        print("Deployment deleted. status='%s'" % str(api_response.status))


def change_image(deployment: V1Deployment, new_image_name: str) -> None:
    """
    Change the image of the deployment
    :param deployment: The deployment setup.
    :param new_image_name: New image name.
    """
    deployment.spec.template.spec.containers[0].image = new_image_name


def run_whac_a_mole(
        kubernetes_config: Optional[str],
        no_replicas: int,
        deployment_image_mole: str,
        deployment_image_relay: str,
        deployment_name: str,
        namespace: str,
        port: int) -> None:
    """
    Main routine.
    :param kubernetes_config: The path to the kubernetes config file.
    :param no_replicas: Number of container in the pod.
    :param deployment_image_mole: The image name in the docker environment for the mole image.
    :param deployment_image_relay: The image names in the docker environment for the relay image.
    :param deployment_name: The name of the deployment.
    :param namespace: The namespace in which the pods are deployed.
    :param port: port of the web_server.
    """
    load_kubernetes_config(kubernetes_config)

    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()

    deployment_name_mole = deployment_name + '-mole-prod'
    deployment_name_relay = deployment_name + '-relay-pod'

    deployment_relay = create_deployment_object(
        no_replicas=1,
        deployment_images=deployment_image_relay,
        deployment_name=deployment_name_relay,
        port=port,
        external_port=True)

    deployment_mole = create_deployment_object(
        no_replicas=no_replicas,
        deployment_images=deployment_image_mole,
        deployment_name=deployment_name_mole,
        port=port,
        external_port=False)

    create_deployment(api_instance=apps_v1, deployment=deployment_relay, namespace=namespace)
    create_deployment(api_instance=apps_v1, deployment=deployment_mole, namespace=namespace)

    # When we shut down our program, this is always ran!
    atexit.register(delete_deployment,
                    api_instance=apps_v1,
                    deployment_names=[deployment_name_relay, deployment_name_mole],
                    namespace=namespace)

    print_all_relevant_pods(core_instance=core_v1, deployment_name=deployment_name_relay)
    print_all_relevant_pods(core_instance=core_v1, deployment_name=deployment_name_mole)
    time.sleep(3)
    print_all_relevant_pods(core_instance=core_v1, deployment_name=deployment_name_relay)
    print_all_relevant_pods(core_instance=core_v1, deployment_name=deployment_name)
    time.sleep(3)
    print_all_relevant_pods(core_instance=core_v1, deployment_name=deployment_name)
    time.sleep(1000)
    print_all_relevant_pods(core_instance=core_v1, deployment_name=deployment_name)


def get_correct_config_folder(project_dir: str) -> str:
    """
    Finds the correct config folder by looking at the parents of the current working dir and
    comparing this to our project directory.
    :return:
    """
    from pathlib import Path
    d = Path().resolve()
    while d.as_posix().split('/')[-1] != project_dir:
        d = d.parent
    return d.as_posix() + '/.kube/config'


if __name__ == '__main__':
    run_whac_a_mole(
        kubernetes_config=get_correct_config_folder('whac-a-mole-kubernetes'),
        no_replicas=3,
        deployment_image_mole='molepodprod',
        deployment_image_relay='molerelayprod',
        deployment_name='mole',
        namespace='whac',
        port=8080)
