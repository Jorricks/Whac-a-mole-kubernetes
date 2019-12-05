# Mole pod
Simple flask app that is run inside a docker container.

# Setup
    pip install .
For during development use
    
    pip install -e ".[dev]"
    
# Dockerfile
The docker files contain two different approaches. \
The first approach uses multi-stage build and is slow but creates a small image(170MB). \
The second approach (Dockerfile2) uses stretch to build quicker but is larger(352MB)