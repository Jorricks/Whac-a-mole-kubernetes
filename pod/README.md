# Mole pod
Simple flask app that is run inside a docker container.

# Setup
    pip install .
For during development use
    
    pip install -e ".[dev]"
    
# Dockerfile
The docker files use multi-stage builds which slow the building down but create 
a very small image(170MB). \

# Building the docker image for minikube
First start up minikube!

    eval $(minikube docker-env)
    docker build -t molepodprod . 
    docker run --name molepodprod -P molepodprod 