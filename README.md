# Kubernetes based Whac-a-mole game
This is whac-a-mole game with Kubernetes running in the background. 

Each mole is a kubernetes pod. 
The goal is to kill the pods faster than kubernetes can deploy new ones.

# Explanation of the application
This repository is split into three applications.

### Mole pod
This is a very basic flask application which is dockerized.\
It contains three endpoints: /health, /kill and /shutdown. \
This application is than build as a docker image and ran as a pod in Kubernetes. \
In the final web interface, a mole is molepod container.

### Mole relay
Again a very basic flask application which is dockerized.\
It contains two endpoints: / and /health. \
The purpose of this application is to be the bridge between the host and the minikube environment. \
Meaning that when we want to access a mole pod, we actually make the request through a container \
with the docker image of this mole relay program.

### Mole game
This application contains most of the logic.\
Based on the configuration given by the command line arguments, it starts the two pods(mole pod
 and mole relay). \
Once the pods are deployed, the front end flask app is launched. \
Here we can access our whac a mole interface. \
When we press a mole, a kill or shutdown command is send through the server, to the relay, 
to finally end up at the specific container in the mole pod. \
Once the mole pod is down, kubernetes will take care to relaunch it.

# Requirements
1. Python3.7
2. Docker
3. Minikube
4. Google Chrome

# General instructions
### Terminal commands to get a working Minikube
Note that the application expects the application to be launched from within a folder of the project
root "whac-a-mole-kubernetes". If you change the project folders name, you do not only have to 
change the upcoming commands but also part of the project. \
You can store the 'whac-a-mole-kubernetes' directory anywhere you like, as long as you set the
correct MINIKUBE_HOME location for each terminal session
    
    export MINIKUBE_HOME=~/PycharmProjects/whac-a-mole-kubernetes;
    export PATH=$MINIKUBE_HOME/bin:$PATH
    export KUBECONFIG=$MINIKUBE_HOME/.kube/config
    export KUBE_EDITOR="code -w"
    
### To create a new minikube profile
In our application we use the profile 'whac'. This profile can be created in the following way:

    minikube --profile whac config set memory 6144
    minikube --profile whac config set cpus 2
    minikube --profile whac config set vm-driver hyperkit
    minikube --profile whac config set kubernetes-version v1.15.6
    minikube start --profile whac
    minikube profile whac

# How to start the molegame
After you set the terminal commands to get a working minikube setup and started the 'whac' profile, 
we can build the pod and relay. The assumption is made that we start from the project directory.

    eval $(minikube docker-env)
    cd relay
    docker build -t molerelayprod . 
    cd ../pod
    docker build -t molepodprod . 

Once the docker images are build, we can already start out application. \
This can either be done by pip installing our game, or by simply running 
game/src/molegame/main.py. \
In the case you kept the default ports, the interface of whac-a-mole is accessible at 
http://localhost:80. \

# How to contribute
1. Fork the repository. 
2. Make your change.
3. Verify the changes are correct by running.

        mypy --ignore-missing-imports pod/src/molepod/ game/src/molegame/ relay/src/molerelay/
        flake8 --max-line-length=100 pod/src/molepod game/src/molegame relay/src/molerelay
        
4. Provide a pull request.

# Special thanks to
- [Burr Sutter for his excelent explanation of Kubernetes.](https://www.youtube.com/watch?v=ZpbXSdzp_vo)
- [The designer of this image of which I borrowed my design.](https://www.skincancer.org/wp-content/uploads/whackamole-900px.jpg)