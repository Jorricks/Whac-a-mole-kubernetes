# Mole relay
Simple flask app that relays information to our moles.

# Setup
    pip install .
For during development use
    
    pip install -e ".[dev]"
    
# Dockerfile
The docker files contain two different approaches. \
The first approach uses multi-stage build and is slow but creates a small image(170MB). \
The second approach (Dockerfile2) uses stretch to build quicker but is larger(352MB)

# Building the docker image for minikube
First start up minikube!

    eval $(minikube docker-env)
    docker build -t molerelayprod . 
    docker run --name molerelayprod -P molerelayprod 