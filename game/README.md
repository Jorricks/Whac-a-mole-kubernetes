# Mole game
This application contains most of the logic.\
Based on the configuration given by the command line arguments, it starts the two pods(mole pod
 and mole relay). \
Once the pods are deployed, the front end flask app is launched. \
Here we can access our whac a mole interface. \
When we press a mole, a kill or shutdown command is send through the server, to the relay, 
to finally end up at the specific container in the mole pod. \
Once the mole pod is down, kubernetes will take care to relaunch it.

# Setup
    pip install .
For during development use
    
    pip install -e ".[dev]"

# Running
You can either run this by pip installing our game as shown above, or by simply running 
game/src/molegame/main.py. \
In the case you kept the default ports, the interface of whac-a-mole is accessible at 
http://localhost:80. \