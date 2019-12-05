import atexit
import time
from typing import Optional, Tuple, List

from kubernetes import client, config
from kubernetes.client import CoreV1Api, AppsV1Api, V1Deployment, V1PodList, V1Pod, V1Container, \
    V1Endpoints, V1Service

v1_core: Optional[CoreV1Api] = None
v1_apps: Optional[AppsV1Api] = None


def load_kubernetes_config(config_file: Optional[str]) -> None:
    """
    We load the kubernetes config and than the corresponding API into the global v1 variable.
    :param config_file: the path to the kubernetes config file
    """
    global v1_core, v1_apps
    if config_file is None or config_file == "":
        config.load_kube_config(
            config_file='/Users/jorricks/PycharmProjects/whac-a-mole-kubernetes/.kube/config')
    else:
        config.load_kube_config()


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


def create_container_object(deployment_image: str, port: int) -> V1Container:
    """
    Create the container object
    :param deployment_image: The image name in the docker environment.
    :param port: port of the web_server.
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

    return client.V1Container(
        name="molerelay",
        image=deployment_image,
        image_pull_policy="Never",
        ports=[client.V1ContainerPort(
            container_port=port,
            # host_ip='0.0.0.0',
            # host_port=8080,
            # name='prt',
            # protocol='TCP'
        )],
        liveness_probe=liveness_probe,
        readiness_probe=readiness_probe
    )


def create_deployment_object(
        no_replicas: int,
        deployment_image: str,
        deployment_name: str,
        port: int,
) -> V1Deployment:
    """
    We create a deployment according to the specified arguments.
    :param no_replicas: Number of container in the pod.
    :param deployment_image: The image name in the docker environment.
    :param deployment_name: The name of the deployment.
    :param port: port of the web_server.
    :return: Deployment setup.
    """
    container = create_container_object(deployment_image, port)

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


def update_deployment(
        api_instance: AppsV1Api,
        deployment: V1Deployment,
        deployment_name: str,
        namespace: str
) -> None:
    """
    Update our deployment
    :param api_instance: The api instance.
    :param deployment: The deployment setup.
    :param deployment_name: The name of the deployment.
    :param namespace: The namespace in which the pods are deployed.
    """
    # Update container image
    deployment.spec.template.spec.containers[0].image = "nginx:1.16.0"
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=deployment_name,
        namespace=namespace,
        body=deployment)
    print("Deployment updated.\n status=\n'%s'" % str(api_response.status))


def delete_deployment(api_instance: AppsV1Api, deployment_name: str, namespace: str) -> None:
    """
    Delete our deployment
    :param api_instance: The api instance
    :param deployment_name: The name of the deployment.
    :param namespace: The namespace in which the pods are deployed.
    """
    api_response = api_instance.delete_namespaced_deployment(
        name=deployment_name,
        namespace=namespace,
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))


def create_service_objects(
        deployment_name: str,
        client_ports: List[int],
        host_ports: List[int],
) -> V1Service:
    """
    We create the service object
    :param deployment_name: The deployment name.
    :param client_ports: A list of all client ports (all the ports of the pods).
    :param host_ports:
    :return:
    """
    assert len(client_ports) == len(host_ports)
    ports = []

    for i in range(len(client_ports)):
        ports.append(
            client.V1ServicePort(
                protocol='TCP',
                port=host_ports[i],
                target_port=client_ports[i]
            )
        )

    return client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=client.V1ServiceSpec(
            ports=ports
        )
    )


def create_endpoint_object(
        deployment_name: str,
        client_ip: int,
        client_port: int,
        host_port: int,
) -> Tuple[V1Service, V1Endpoints]:
    """
    :param deployment_name: The name of the deployment.
    :param client_ip: The clients ip.
    :param client_port: The clients port.
    :param host_port: THe hosts port.
    :return All unlocked ports.
    """

    endpoint = client.V1Endpoints(
        api_version="v1",
        kind="Endpoints",
        metadata=client.V1ObjectMeta(name=deployment_name),
        subsets=client.V1EndpointSubset(
            addresses=[
                client.V1EndpointAddress(
                    ip=client_ip
                )
            ],
            ports=[
                client.V1EndpointPort(
                    port=client_port
                )
            ]
        ))

    return service, endpoint


def change_image(deployment: V1Deployment, new_image_name: str) -> None:
    """
    Change the image of the deployment
    :param deployment: The deployment setup.
    :param new_image_name: New image name.
    """
    deployment.spec.template.spec.containers[0].image = new_image_name


def main(
        no_replicas: int,
        deployment_image: str,
        deployment_name: str,
        namespace: str,
        port: int,
) -> None:
    """
    Main routine.
    :param no_replicas: Number of container in the pod.
    :param deployment_image: The image name in the docker environment.
    :param deployment_name: The name of the deployment.
    :param namespace: The namespace in which the pods are deployed.
    :param port: port of the web_server.
    """
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    load_kubernetes_config(None)
    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()

    # Create a deployment object with client-python API. The deployment we
    # created is same as the `nginx-deployment.yaml` in the /examples folder.

    deployment = create_deployment_object(
        no_replicas=no_replicas,
        deployment_image=deployment_image,
        deployment_name=deployment_name,
        port=port
    )

    # time.sleep(5)
    # print_all_pods(core_v1)

    create_deployment(api_instance=apps_v1, deployment=deployment, namespace=namespace)

    atexit.register(delete_deployment,
                    api_instance=apps_v1,
                    deployment_name=deployment_name,
                    namespace=namespace)
    # delete_deployment(api_instance=apps_v1, deployment_name=deployment_name, namespace=namespace)

    print_all_relevant_pods(core_instance=core_v1, deployment_name=deployment_name)
    time.sleep(3)
    print_all_relevant_pods(core_instance=core_v1, deployment_name=deployment_name)
    time.sleep(100)

    # update_deployment(
    #     api_instance=apps_v1,
    #     deployment=deployment,
    #     deployment_name=deployment_name,
    #     namespace=namespace
    # )

    print_all_relevant_pods(core_instance=core_v1, deployment_name=deployment_name)
    time.sleep(15)


if __name__ == '__main__':
    main(
        no_replicas=3,
        deployment_image='molepodprod',
        deployment_name='molerelay-prod',
        namespace='whac',
        port=8080
    )
