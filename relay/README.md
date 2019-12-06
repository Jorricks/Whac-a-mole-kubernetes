# Mole relay
Simple flask app that relays information to our moles.

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
    docker build -t molerelayprod . 
    docker run --name molerelayprod -P molerelayprod 