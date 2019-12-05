# Mole game


# Minikube setttings
    export MINIKUBE_HOME=/Users/jorricks/PycharmProjects/whac-a-mole-kubernetes;
    export PATH=$MINIKUBE_HOME/bin:$PATH
    export KUBECONFIG=$MINIKUBE_HOME/.kube/config
    export KUBE_EDITOR="code -w"

    minikube --profile whac config set memory 6144
    minikube --profile whac config set cpus 2
    minikube --profile whac config set vm-driver hyperkit
    minikube --profile whac config set kubernetes-version v1.15.6
    minikube start --profile whac
    minikube profile whac