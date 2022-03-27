# A class to generate random data from the sensors that will be on the real drone module
# Also, has functions to connect to the remote server and send the data
#
#   Written by Team CCC
#



## [imports]
from random import random, seed, randint    # Used to generate random data values
import socketio                             # Used to connect to the servers websocket
import requests                             # Allows to send API requests to the server
from fakeGPS import GPS                     # Used to fake a GPS signal
from geiger import Geiger_Counter           # Used to interface with the Geiger Counter
from PMS5003 import PMS5003_Sensor          # Used to interface with the PMS5003 Sensor
from time import sleep                      # Used to add delays so the comm bus' are not overloaded
from I2C_Reset import I2C_Watchdog          # Used to reset I2C devices in case of errors
from smbus2 import SMBus



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

        # Initialising the I2C Bus
        self.BUS = SMBus(1)

        # Initiating the GPS sensor
        self.GPS = GPS()

        # Initiating the Geiger sensor
        self.geiger = Geiger_Counter(0x4d)

        # Initiating the PMS5003 Sensor
        self.PMS5003 = PMS5003_Sensor(0x2d)

        # I2C Error Counter
        self.ERROR_COUNTER = 0

        # Creating the I2C Watchdog connected on pin 23
        self.I2C_WATCHDOG = I2C_Watchdog(23)

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

        # Getting data from the Geiger Counter
        payload["geiger"]= self.getGeiger()

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
            return 0

        return 1
    
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
        
        air["pm1"], check = self.PMS5003.getData(1, self.BUS)
        #print("PM1 ", air["pm1"], " Check ", check)
        sleep(0.01)

        # Checking if the I2C failed or not
        if(check == 1):
            self.ERROR_COUNTER = self.ERROR_COUNTER + 1
            print("PMS5003 PM1 I2C Error")

        air["pm2_5"], check = self.PMS5003.getData(2, self.BUS)
        #print("PM2.5 ", air["pm2_5"], " Check ", check)
        sleep(0.01)

        # Checking if the I2C failed or not
        if(check == 1):
            self.ERROR_COUNTER = self.ERROR_COUNTER + 1
            print("PMS5003 PM2.5 I2C Error")

        air["pm10"], check = self.PMS5003.getData(3, self.BUS)
        #print("PM10 ", air["pm10"], " Check ", check)
        sleep(0.01)

        # Checking if the I2C failed or not
        if(check == 1):
            self.ERROR_COUNTER = self.ERROR_COUNTER + 1
            print("PMS5003 PM10 I2C Error")

        
        # Checking if the I2C bus has errored multiple times
        if(self.ERROR_COUNTER > 3):
            
            # Reset the I2C bus
            #self.I2C_WATCHDOG.reset()

            # Reset the error counter
            self.ERROR_COUNTER = 0

        return air

    # Generates a random radiation level
    def getGeiger(self):
        data, check = self.geiger.getData(self.BUS)
        #print("CPM ", data, " Check ", check)
        sleep(0.01)
        
        # Checking if the I2C failed or not
        if(check == 1):
            self.ERROR_COUNTER = self.ERROR_COUNTER + 1
            print("Geiger Counter I2C Error")
        
        # Checking if the I2C bus has errored multiple times
        if(self.ERROR_COUNTER > 3):
            
            # Reset the I2C bus
            self.I2C_WATCHDOG.reset()

            # Reset the error counter
            self.ERROR_COUNTER = 0

        return data
        
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