## [imports]
from bme280 import BME280       # Needed for the Temperature, Pressure and Humidity Sensors
from pms5003 import PMS5003     # Needed for the Particulates sensor
from enviroplus import gas      # Needed for the Gas sensor
try:
    from ltr559 import LTR559   # Needed for the Light Sensor
    light = LTR559()
except ImportError:
    import ltr559


# Main Class
#   Functions:
#       Constructor - Initialises the sensors and gets them ready to send data
#       get *       - Gets the relevant data from the required sensor
class Enviro:

    # Initialises the sensors and gets them ready to send data
    def __init__(self):
        # BME280 temperature/pressure/humidity sensor
        self.bme280 = BME280()

        # PMS5003 particulate sensor
        self.pms5003 = PMS5003()
        
        return

    # Gets the CPU temp
    def get_cpu_temperature(self):

        # Accessing the CPU temprature
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
            temp = int(temp) / 1000.0

        # Returning the CPU temp
        return temp

    # Gets the compensated Temprature from the Enviro sensor
    def get_temperature(self):

        # Scale factor to correct raw read
        factor = 2.25

        # Getting a raw temp read
        raw_temp = self.bme280.get_temperature()

        # Compensating the Temprature sensor
        data = raw_temp - ((raw_temp) / factor)

        # Sending the data
        return round(data, 2)

    # Gets the Gas data
    def get_gas(self):
        
        # Creating the empty dictionary
        gas_data={}

        # Getting all the gas data
        data = gas.read_all()

        # Formatting the data
        gas_data["co"] = data.oxidising/1000
        gas_data["no2"] = data.reducing/1000
        gas_data["nh3"] = data.nh3/1000

        # Sending the data
        return gas_data

    # Gets the Particulates data
    def get_air(self):

        # Creating the empty dictionary
        air={}

        # Getting al the air data
        data = self.pms5003.read()

        # Formatting the data
        air["pm1"] = data.pm_ug_per_m3(1.0)
        air["pm2_5"] = data.pm_ug_per_m3(2.5)
        air["pm10"] = data.pm_ug_per_m3(10)

        # Sending the data
        return air

    # Gets the Pressure data
    def get_pressure(self):

        # Sending the Pressure data rounded to 0 DP
        return round(self.bme280.get_pressure(),0)

    # Gets the Humidity data
    def get_humidity(self):

        # Sending the Humidity data rounded to 0 DP
        return round(self.bme280.get_humidity(),0)

    # Gets the Light level
    def get_light(self):

        # Sending the Light data rounded to 0 DP
        return round(light.get_lux(),0)

'''
# Testing
enviro = Enviro()

while True:
    print(str(enviro.get_light())+"\n")
    sleep(0.1)
'''