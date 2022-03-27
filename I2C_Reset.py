import RPi.GPIO as GPIO     # Used to Access RPi GPIO Pins
from time import sleep

class I2C_Watchdog:

    def __init__(self, PIN):

        # Setting the Pin naming method
        GPIO.setmode(GPIO.BCM)

        # Pin the Relay Toggle is connected to
        self.PIN = PIN

        # Mapping up the connection toggle to the pin its connected to
        GPIO.setup(self.PIN, GPIO.OUT)

        # Enabling the Voltage to the I2C devices
        GPIO.output(self.PIN, GPIO.LOW)

        return

    def reset(self):

        # Disabling the I2C devices
        GPIO.output(self.PIN, GPIO.HIGH)

        # Waiting for a reset
        sleep(1)

        # Enabling the I2C devices
        GPIO.output(self.PIN, GPIO.LOW)

I2C = I2C_Watchdog(23)

I2C.reset()