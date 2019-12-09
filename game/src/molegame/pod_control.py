from typing import Optional, List

from kubernetes import client, config
from kubernetes.client import CoreV1Api, AppsV1Api, V1Deployment, V1PodList, V1Pod, V1Container, \
    V1PodStatus

from molegame.whac_config import WhacConfig


def load_kubernetes_config(config_file: Optional[str]) -> None:
    """
    We load the kubernetes config and than the corresponding API into the global v1 variable.
    :param config_file: The path to the kubernetes config file.
    """
    if config_file is None or config_file == "":
        config.load_kube_config()
    else:
        config.load_kube_config(config_file=config_file)


def get_containers_in_pod(core_instance: CoreV1Api, deployment_name: str) -> List[V1Pod]:
    containers = []
    ret: V1PodList = core_instance.list_pod_for_all_namespaces(watch=False)
    i: V1Pod
    for i in ret.items:
        if deployment_name in str(i.metadata.name):
            containers.append(i)
    return containers


def get_relevant_pods_status(core_instance: CoreV1Api, deployment_name: str) -> List[V1PodStatus]:
    return [container.status for container in
            get_containers_in_pod(core_instance=core_instance, deployment_name=deployment_name)]


def print_all_containers_in_pod(core_instance: CoreV1Api, deployment_name: str) -> None:
    """
    We print all pods
    :param core_instance: Core API instance.
    :param deployment_name: The name of the deployment.
    """
    print('\n\n')
    print("Listing pods with their IPs:")
    pod = get_containers_in_pod(core_instance=core_instance, deployment_name=deployment_name)
    for container in pod:
        print("%s\t%s\t%s" %
              (container.status.pod_ip, container.metadata.namespace, container.metadata.name))


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
        container_port: int,
        external_port: bool,
) -> V1Deployment:
    """
    We create a deployment according to the specified arguments.
    :param no_replicas: Number of container in the pod.
    :param deployment_images: The image name in the docker environment for the moles.
    :param deployment_name: The name of the deployment.
    :param container_port: port of the web_server.
    :param external_port: whether the port should be an external port.
    :return: Deployment setup.
    """
    container = create_container_object(deployment_images, container_port, external_port)

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


def update_no_replicas_in_deployment(
        whac_config: WhacConfig,
        apps_v1: AppsV1Api,
        new_no_replicas: int,
) -> None:
    """
    Update our deployment
    :param whac_config: All the static configurations required to run are in this instance.
    :param apps_v1: The api instance.
    :param new_no_replicas: the new number of replicas
    """
    the_mole_deployment: Optional[client.V1Deployment] = None
    a_deployment: client.V1Deployment
    for a_deployment in apps_v1.list_deployment_for_all_namespaces():
        if whac_config.deployment_name_mole in a_deployment.metadata.name:
            the_mole_deployment = a_deployment

    if the_mole_deployment is None:
        return

    # Update no replicas image
    the_mole_deployment.spec.replicas = new_no_replicas
    # Update the deployment
    api_response = apps_v1.patch_namespaced_deployment(
        name=whac_config.deployment_name_mole,
        namespace=whac_config.namespace,
        body=the_mole_deployment)
    print("Deployment updated.\n status=\n'%s'" % str(api_response.status))


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
