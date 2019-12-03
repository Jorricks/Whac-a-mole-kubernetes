# Kubernetes based Whac-a-mole game
This is whac-a-mole game with Kubernetes running in the background. 

Each mole is a kubernetes pod. 
The goal is to kill the pods faster than kubernetes can deploy new ones.

# Explanation of the application
This repository is split into two applications.

### Molepod
This is a very basic flask application which is dockerized.\
The docker image is ran as a pod in Kubernetes.

### Molegame
The application that is run to start the whack-a-mole game.\
Once we start our application, several 

# How to start the molegame
@ToDo


# How to contribute
1. Fork the repository. 
2. Make your change.
3. Verify the changes are correct by running.

        cd src/
        mypy gitje/
        flake8 --max-line-length=100 gitje
4. Provide a pull request.