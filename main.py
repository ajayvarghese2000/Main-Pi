## [imports]
import socketio             # The socketIO server that will wait for images from camera
import uvicorn              # The ASGI that will run the service
from drone import drone     # The drone module
from time import sleep      # Used for Simple delays

# Creating the sockets server
sio = socketio.AsyncServer(async_mode="asgi")
socket_app = socketio.ASGIApp(sio)

# Creating the Drone object that the sensors will attach to
DNAME = '10'
URL = "https://ajayvarghese.me"
Drone = drone(DNAME, URL)

# Checks if the drone should be sending data or not
########## REPLACE WITH TOGGLE SWITCH CODE #################
CONNECTION_SWITCH = True

# Connected Status
CONNECTED = False

if (CONNECTION_SWITCH == True):
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

    # Using the gloabl variables 
    global CONNECTED, CONNECTION_SWITCH

    # Checks if we're meant to send data
    if (CONNECTION_SWITCH == True):

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