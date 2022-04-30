try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    light = LTR559()
except ImportError:
    import ltr559
from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas
from time import sleep


class Enviro:
    def __init__(self):
        # BME280 temperature/pressure/humidity sensor
        self.bme280 = BME280()

        # PMS5003 particulate sensor
        self.pms5003 = PMS5003()
        
        return

    def get_cpu_temperature(self):
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
            temp = int(temp) / 1000.0
        return temp

    def get_temperature(self):
        factor = 2.25
#        cpu_temp = self.get_cpu_temperature()
        raw_temp = self.bme280.get_temperature()
        data = raw_temp - ((raw_temp) / factor)
        return round(data, 2)

    def get_gas(self):
        gas_data={}
        data = gas.read_all()
        gas_data["co"] = data.oxidising/1000
        gas_data["no2"] = data.reducing/1000
        gas_data["nh3"] = data.nh3/1000
        return gas_data

    def get_air(self):
        air={}
        data = self.pms5003.read()
        air["pm1"] = data.pm_ug_per_m3(1.0)
        air["pm2_5"] = data.pm_ug_per_m3(2.5)
        air["pm10"] = data.pm_ug_per_m3(10)
        return air

    def get_pressure(self):
        return round(self.bme280.get_pressure(),0)

    def get_humidity(self):
        return round(self.bme280.get_humidity(),0)

    def get_light(self):
        return round(light.get_lux(),0)

'''
# Testing
enviro = Enviro()

while True:
    print(str(enviro.get_light())+"\n")
    sleep(0.1)
'''