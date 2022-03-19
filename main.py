## [imports]
import socketio             # The socketIO server that will wait for images from camera
import uvicorn              # The ASGI that will run the service
from drone import drone     # The drone module
from time import sleep      # Used for Simple delays
import RPi.GPIO as GPIO     # Used to Access RPi GPIO Pins

# Setting the Pin naming method
GPIO.setmode(GPIO.BCM)

# Creating the sockets server
sio = socketio.AsyncServer(async_mode="asgi")
socket_app = socketio.ASGIApp(sio)

# Creating the Drone object that the sensors will attach to
DNAME = '10'
URL = "https://ajayvarghese.me"
Drone = drone(DNAME, URL)

# Pin the Connection Toggle is connected to
CONNECTION_TOGGLE_PIN = 23

# Mapping up the connection toggle to the pin its connected to
GPIO.setup(CONNECTION_TOGGLE_PIN, GPIO.IN)

# Function to check if the drone should be sending data or not
# Returns True or False
def CONNECTION_SWITCH(): 
    if GPIO.input(CONNECTION_TOGGLE_PIN):
        return True
    
    return False

# Connected Status
CONNECTED = False

if (CONNECTION_SWITCH() == True):
    # Connect the drone to the server list
    while(CONNECTED == False):
        CONNECTED = True
        try:
            Drone.connect()
        except:
            CONNECTED = False
            sleep(5)

# SocketIO handler for when a new image is sent
@sio.on("cam")
async def getdata(sid, mes):

    # Using the global variables 
    global CONNECTED

    # Checks if we're meant to send data
    if (CONNECTION_SWITCH() == True):

        # Checks if the drone is connected
        if(CONNECTED == True):

            # Sends the data to the server checks if it fails
            if(Drone.senddata(mes["frame"], mes["person"]) == 0):

                # If it does fail disconnect
                await sio.disconnect(sid)
                Drone.disconnect()
                CONNECTED = False
        # If not already connected attempt a connection
        else:

            # tries to connect and set the appropriate falgs
            CONNECTED = True
            try:
                Drone.connect()
            except:
                CONNECTED = False
    # If we're not meant to send data, attempt to disconnect if connected
    else:
        if(CONNECTED == True):
            Drone.disconnect()
            CONNECTED = False

    return


if __name__ == "__main__":
    kwargs = {"host": "192.168.0.5", "port": 12345, "workers" : 1}
    kwargs.update({"debug": False, "reload": False})
    uvicorn.run("main:socket_app", **kwargs)