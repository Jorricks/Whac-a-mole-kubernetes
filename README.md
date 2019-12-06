# Kubernetes based Whac-a-mole game
This is whac-a-mole game with Kubernetes running in the background. 

Each mole is a kubernetes pod. 
The goal is to kill the pods faster than kubernetes can deploy new ones.

# Explanation of the application
This repository is split into two applications.

### Molepod
This is a very basic flask application which is dockerized.\
The docker image is ran as a pod in Kubernetes.

### Molerelay


### Molegame
The application that is run to start the whack-a-mole game.\
Once we start our application, several 

# Requirements
1. Python3.7
2. Docker
3. Minikube

# General instructions
### Get your terminal configured to get minikube working correctly
    
    export MINIKUBE_HOME=/Users/jorricks/PycharmProjects/whac-a-mole-kubernetes;
    export PATH=$MINIKUBE_HOME/bin:$PATH
    export KUBECONFIG=$MINIKUBE_HOME/.kube/config
    export KUBE_EDITOR="code -w"
    
### To create a new minikube profile
    minikube --profile whac config set memory 6144
    minikube --profile whac config set cpus 2
    minikube --profile whac config set vm-driver hyperkit
    minikube --profile whac config set kubernetes-version v1.15.6
    minikube start --profile whac
    minikube profile whac

# How to start the molegame
@ToDo


# How to contribute
1. Fork the repository. 
2. Make your change.
3. Verify the changes are correct by running.

        mypy --ignore-missing-imports pod/src/molepod/ game/src/molegame/ relay/src/molerelay/
        flake8 --max-line-length=100 pod/src/molepod game/src/molegame relay/src/molerelay
        
4. Provide a pull request.

# Special thanks to
- https://media.istockphoto.com/illustrations/game-to-hit-the-mole-illustration-id1153033854
- https://www.skincancer.org/wp-content/uploads/whackamole-900px.jpg