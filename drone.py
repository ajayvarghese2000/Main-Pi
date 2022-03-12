# A class to generate random data from the sensors that will be on the real drone module
# Also, has functions to connect to the remote server and send the data
#
#   Written by Team CCC
#

## [imports]
from random import random, seed, randint    # Used to generate random data values
import socketio                             # Used to connect to the servers websocket
import requests                             # Allows to send API requests to the server
from fakeGPS import GPS

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

        # Sets the seed to generate data with
        seed(1)

        # Initiating the GPS sensor
        self.GPS = GPS()

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
    def senddata(self, frame, person):

        # Changing the seed to get random values
        seed(randint(0,1000000))

        # Creating a new payload to send and setting the droneID
        payload = {}

        # Adding the drone name to the payload
        payload["dname"] = self.dname

        # Generating data from sensors and adding to payload
        payload["temp"] = self.getTemp()
        payload["pressure"] = self.getPressure()
        payload["humidity"] = self.getHumidity()
        payload["lux"] = self.getLux()
        payload["geiger"] = self.getGeiger()
        payload["gas"] = self.getGas()
        payload["air"] = self.getAir()
        payload["gps"] = self.getGPS()

        # Adding the webcam frame to the payload
        payload["cam"] = frame

        # As there is no thermal camera, for testing the thermal camera shows the same frame
        payload["tcam"] = frame

        payload["person"] = person

        # Attempts to send the payload over the websocket
        try:
            self.sock.emit("getdata", payload)
        except:
            print("error sending payload")

        return
    
    # Generates a random temperature value
    def getTemp(self):
        return round(randint(-10,100) + random(), 2)
        
    # Generates a random pressure value
    def getPressure(self):
        return round(randint(900,1500) + random(), 2)

    # Generates a random humidity value
    def getHumidity(self):
        return round(randint(0,100) + random(), 2)
        
    # Generates a random lux value
    def getLux(self):
        return round(randint(0,100) + random(), 2)
        
    # Generates random gas sensor values
    def getGas(self):

        # Creating the gas data structure to be inside the payload
        gas = {}

        gas["co"] = round(random(),2)
        gas["no2"] = round(random(),2)
        gas["nh3"] = round(random(),2)
        
        return gas
    
    # Generates random air particle values
    def getAir(self):
        
        # Creating the Air data structure to be inside the payload
        air = {}
        
        air["pm1"] = round(random(),2)
        air["pm2_5"] = round(random(),2)
        air["pm10"] = round(random(),2)

        return air

    # Generates a random radiation level
    def getGeiger(self):
        return randint(0,2500)
        
    # Generates random lat and log values
    def getGPS(self):

        # Creating the gps data structure to be inside the payload
        gps = {}

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