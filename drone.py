# A class to generate random data from the sensors that will be on the real drone module
# Also, has functions to connect to the remote server and send the data
#
#   Written by Team CCC
#



## [imports]
import socketio                             # Used to connect to the servers websocket
import requests                             # Allows to send API requests to the server
from fakeGPS import GPS                     # Used to fake a GPS signal
from geiger import Geiger_Counter           # Used to interface with the Geiger Counter
from time import sleep                      # Used to add delays so the comm bus' are not overloaded
from smbus2 import SMBus                    # Used to access the I2C bus
from thermal_cam import thermal_camera      # Used to get image from the thermal camera
from Enviro import Enviro                   # Used to get data of the Enviro Sensor



# Main Class
#   Functions:
#       Constructor - Initialises the drone sets its name and server URL
#       Connect     - Registers with the remote server and tries to open a websocket
#       Disconnect  - Removes the drone from the server and closes the websocket
#       senddata    - Creates the data packet to be sent to the server
#       get *       - Generates the relevant data from the sensor
class drone:

    # Constructor class, sets drone up
    #   Takes in, the name/ID of the drone and the server URL
    def __init__(self, DNAME, URL):

        # Assigns the drone id to a internal variable
        self.dname = DNAME

        # Assigns the URL of the server to a internal variable
        self.url = URL

        # Initialising the I2C Bus
        self.BUS = SMBus(1)

        # Initiating the GPS sensor
        self.GPS = GPS()

        # Initiating the Geiger sensor
        self.geiger = Geiger_Counter(0x4d)

        # Initiating the Enviro
        self.enviro = Enviro()

        # Initiating the Thermal Camera Sensor
        ##self.tcam = thermal_camera()

        return
    
    # Allows the drone to register it self with the server and open a websocket
    #   Retruns either 1, if connection was a seccess or 0 if it failed
    def connect(self):
        try:

            # Attempts the registration with the drone id given - refer to API docs for more info
            registration = requests.post(self.url + "/drones/" + str(self.dname))

            # Opens the websocket once registration is done
            self.sock = socketio.Client(logger=False, engineio_logger=False)
            self.sock.connect(self.url, socketio_path="/ws/socket.io/")

            # If no errors are thrown then the function returns 1 to represent a success
            return 1
        
        except:
            
            # If errors are thrown then the function returns 0
            return 0

    # Allows the drone to remove it self from the server and close the websocket
    #   Retruns either 1, if connection was a seccess or 0 if it failed
    def disconnect(self):
        try:

            # Instructs the API to remove this drone
            deregistration = requests.post(self.url + "/removedrone/" + str(self.dname))
            
            # Checks if the websocket is alive
            if self.sock.connected == True:

                # Disconnects it if it is still open
                self.sock.disconnect()
            
            # If no errors are thrown then the function returns 1 to represent a success
            return 1
        
        except:

            # If errors are thrown then the function returns 0
            return 0

    # Allows to build the payload of data to be sent to the server via the websocket
    #   Takes in the frame from the webcam in Base64 format
    async def senddata(self, frame, person):

        # Creating a new payload to send and setting the droneID
        payload = {}

        # Adding the drone name to the payload
        payload["dname"] = self.dname

        # Generating data from sensors and adding to payload
        payload["temp"] = self.getTemp()
        payload["pressure"] = self.getPressure()
        payload["humidity"] = self.getHumidity()
        payload["lux"] = self.getLux()

        # Getting data from the Geiger Counter
        payload["geiger"]= self.getGeiger()

        payload["gas"] = self.getGas()
        payload["air"] = self.getAir()
        payload["gps"] = self.getGPS()

        # Adding the webcam frame to the payload
        payload["cam"] = frame

        # As there is no thermal camera, for testing the thermal camera shows the same frame
        payload["tcam"] = frame #self.tcam.get_image()

        payload["person"] = person

        # Attempts to send the payload over the websocket
        try:
            self.sock.emit("getdata", payload)
        except:
            print("error sending payload")
            return 0

        return 1
    
    # Generates a random temperature value
    def getTemp(self):
        return self.enviro.get_temperature()
        
    # Generates a random pressure value
    def getPressure(self):
        return self.enviro.get_pressure()

    # Generates a random humidity value
    def getHumidity(self):
        return self.enviro.get_humidity()
        
    # Generates a random lux value
    def getLux(self):
        return self.enviro.get_light()
        
    # Generates random gas sensor values
    def getGas(self):
        return self.enviro.get_gas()
    
    # Generates random air particle values
    def getAir(self):
        # Getting the Air data
        return self.enviro.get_air()

    # Generates a random radiation level
    def getGeiger(self):
        data, check = self.geiger.getData(self.BUS)
        sleep(0.01)
        
        # Checking if the I2C failed or not
        if(check == 1):
            print("Geiger Counter I2C Error")
        
        return data
        
    # Generates random lat and log values
    def getGPS(self):

        # Creating the gps data structure to be inside the payload
        gps = {}

        # Getting the GPS Values
        gps["lat"], gps["long"] = self.GPS.getPos()
        
        return gps


'''    
####################### [TESTING] #######################

d1 = drone(0, "http://localhost")

d1.connect()

for i in range(10):
    d1.senddata("hi")
    sleep(1)

d1.disconnect()

'''