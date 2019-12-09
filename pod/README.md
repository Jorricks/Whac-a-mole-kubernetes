# Mole pod
Simple flask app that is supposed to be run inside a docker container.

# End points
1. /health - Returns a http code of 200 if everything is running according to specification and no
 kill request has been made yet. Otherwise it returns a http code of 503.
2. /kill - Returns 200 and kills part of the webserver, meaning it will only return 503's now on 
the health call.
3. /shutdown - This shuts down the whole webserver. After this, the webserver can not reply to any
requests anymore.

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
    docker build -t molepodprod . 
    docker run --name molepodprod -P molepodprod 