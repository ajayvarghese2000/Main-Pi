import socketio             # The socketIO server that will wait for images from camera
import uvicorn              # The ASGI that will run the service
from drone import drone     # The drone module


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[], ping_interval = (7200,7200), ping_timeout = 7200, max_http_buffer_size = 10000000)
socket_app = socketio.ASGIApp(sio)

# Creating the Drone object that the sensors will attach to
DNAME = '10'
URL = "https://ajayvarghese.me"  # URL of the host server
Drone = drone(DNAME, URL)

# Connect the drone to the server list
Drone.connect()

# SocketIO handler for when a new image is sent
@sio.on("cam")
async def getdata(sid, mes):

    if(Drone.senddata(mes["frame"], mes["person"]) == 0):
        Drone.disconnect()
        Drone.connect()

    return


if __name__ == "__main__":
    kwargs = {"host": "192.168.0.5", "port": 12345, "workers" : 1}
    kwargs.update({"debug": False, "reload": False})
    uvicorn.run("main:socket_app", **kwargs)