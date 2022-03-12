import socketio             # The socketIO server that will wait for images from camera
import uvicorn              # The ASGI that will run the service
from drone import drone     # The drone module
import sys                  # used to terminate if errors


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[], ping_interval = (7200,7200), ping_timeout = 7200, max_http_buffer_size = 10000000)
socket_app = socketio.ASGIApp(sio)

# Creating the Drone object that the sensors will attach to
DNAME = '10'
URL = "https://ajayvarghese.me"  # URL of the host server
Drone = drone(DNAME, URL)

try:
    Drone.connect()
except:
    print("Unable to reach cloud server")

'''
@sio.on("connect")
async def connect(sid, env):
    # Prints a connection message and their session ID
    print("New Client connected ", sid)

# SocketIO handler for when a client disconnects
@sio.on("disconnect")
async def disconnect(sid):
    # Prints a disconnection message and their session ID
    print("Client disconnected ", sid)
'''

# SocketIO handler for when a new image is sent
@sio.on("cam")
async def getdata(sid, mes):

    # Debug statement to print what device id gave what message
    # print(mes)
    Drone.senddata(mes["frame"], mes["person"])


if __name__ == "__main__":
    kwargs = {"host": "192.168.0.5", "port": 12345, "workers" : 1}
    kwargs.update({"debug": False, "reload": False})
    uvicorn.run("server:socket_app", **kwargs)