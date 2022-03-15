<p align="center">
	<a href="https://github.com/lboroWMEME-TeamProject/CCC-ProjectDocs"><img src="https://i.imgur.com/VwT4NrJ.png" width=650></a>
	<p align="center"> This repository is part of  a collection for the 21WSD001 Team Project. 
	All other repositories can be access below using the buttons</p>
</p>

<p align="center">
	<a href="https://github.com/lboroWMEME-TeamProject/CCC-ProjectDocs"><img src="https://i.imgur.com/rBaZyub.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Dashboard"><img src="https://i.imgur.com/fz7rgd9.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Cloud-Server"><img src="https://i.imgur.com/bsimXcV.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Drone-Firmware"><img src="https://i.imgur.com/yKFokIL.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Simulated-Drone"><img src="https://i.imgur.com/WMOZbrf.png" alt="drawing" height = 33/></a>
</p>

------------

# Main-Pi

This repo contains code that will be run on the Main Pi. The Main Pi is responsible for interfacing with each of the individual subsystems attached to it, getting the relevant data from them and sending that to the cloud server.

------------

## Table of Contents

- [Subsystem Overview](#Subsystem-Overview)
- [Code Overview](#Code-Overview)
    - [Event Loop](#Event-Loop)
- [Wiring Diagram](#Wiring-Diagram)
- [Installation](#Installation)
- [Deployment](#Deployment)

------------

## Subsystem Overview

There are 5 major subsystems attached to the Main Pi as well as the Main Pi system itself.

<p align="center">
	<img src="https://i.imgur.com/8I0nU0g.jpg" alt="drawing"/>
</p>

The vase majority of these are connected via I2C however the AI-Cam is connected using TCP Socket due to the larger amount of data that it sends and the limitations of the speed of the I2C bus.

*For a more detailed look at the other indavidual subsystems please visit its respective repository they can all be found within the [Drone Firmware](https://github.com/lboroWMEME-TeamProject/Drone-Firmware) repo.*

------------

## Code Overview

The Code is split into 2 major components,

`main.py` - The main program that is run, starts us the sockets server that allows for the camera to connect and send data. Also contains the drone object.

`drone.py` - Contains the drone class that handles getting the data from the I2C connected subsystems, packing that data into the schema the server is expecting and sending that data to the server.

There are also some minor components,

`fakeGPS.py` - Contains a object definition for a fake GPS module that emulates a GPS signal starting in Loughborough and emulates movement. 

### Event Loop
The Main-Pi runs a sockets server and runs on a simple event loop.

<p align="center">
	<img src="https://i.imgur.com/7Zk6h83.jpg" alt="drawing"/>
</p>

The socket server will wait for the AI-Cam to send a frame to it, then if sending is enabled via the toggle switch, it will get the data from the I2C devices and send it to the remote server. 

If sending is not enabled it will discard the frame. A new frame comes in about 7-10 times per second when using the Raspberry Pi 4 to run the neural detection.


------------

## Wiring Diagram

*Will be added when wiring is finalised*

------------

## Installation

**Step 0** : Setup a Raspberry Pi with linux.

**Step 1** : Clone the repo to the target device, If you have git installed you can do so by running the following.

```
git clone https://github.com/lboroWMEME-TeamProject/Main-Pi.git
```

**Step 3** : Install the Python dependencies using pip.

```
pip install -r requirements.txt
```

**Step 4** : Edit the configuration variables in `main.py` to match your setup.

`main.py` :
```
# Creating the Drone object that the sensors will attach to
DNAME = <SET THIS To THE ID/SERIAL OF THE DRONE>
URL = <URL TO THE REMOTE SERVER>
```

**Step 5** : Run `main.py` and you will see a sockets server spin up and wait for connections.

------------

## Deployment

Once you have the code installed and setup, you can deploy the package as a systemd service that auto starts up at boot. An example `.service` file is included in the project repo, you can use that or tweak the values to match your specific setup.

`mainpi.service` :

```
[Unit]
Description=Auto Start Main Pi Server
After=network.target

[Service]
User=<User To Run App>
Group=<User Group>
WorkingDirectory=<Path to Working Directory>
ExecStart=python3 main.py

[Install]
WantedBy=multi-user.target
```

Once you have setup your `.service` file you need to enable it on the system by first copying the file to the systemd service location.

You can do so by executing the following command

```
sudo cp mainpi.service /etc/systemd/system
```

Then you need to activate the service,

```
sudo systemctl enable mainpi.service
```

Then you can start the service

```
sudo systemctl start mainpi.service
```

Now on boot after the device has an internet connection the detection will automatically start.

------------