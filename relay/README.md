# Mole relay
Simple flask app that relays information to our moles. \
This piece is required to relay outside information to a specific container.

# End points
1. / - Relays a message to a mole. Given the ip, the port and the message the mole should receive,
this call actually makes the request and forwards the response.
2. /health - Returns a http code of 200.

# Setup
    pip install .
For during development use
    
    pip install -e ".[dev]"
    
# Dockerfile
The docker file uses a multi-stage build process which means slower building but much smaller 
images of only 170MB. \

# Building the docker image for minikube
First start up minikube!

    eval $(minikube docker-env)
    docker build -t molerelayprod . 
    docker run --name molerelayprod -P molerelayprod 