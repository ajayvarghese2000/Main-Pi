## [Imports]
from time import sleep
from smbus2 import SMBus    # Used to communicate with the i2c bus on pi

# Initialising the I2C Bus
BUS = SMBus(1)

# Address of the i2c device
ADDRESS = 0x2d ## 0x2d for the Pm and 0x4d for the geiger

# The Number of Blocks of 8 bits to read from the device
BLOCKSIZE = 2   # [WARNING] If set incorrectly the i2c bus will block out

# Simple Function to read from a registar and combine two blocks of data and retrun as a HEX
def read_test(registar_address):
    # Use the Global Variables
    global BLOCKSIZE, ADDRESS, BUS

    # Attempt read from bus
    try:
        # Attempt read from device
        dat = BUS.read_i2c_block_data(ADDRESS, registar_address, BLOCKSIZE)

        # Combine the Values
        combine = dat[1] << 8 | dat[0]

        # Retrun the Hex
        return combine
    # Returns 1 on failure
    except:
        return "err"

# Try reading from registar 1
#print(read_test(1))


while True:
    PM1= read_test(1)
    sleep(0.1)
    PM2_5 = read_test(2)
    sleep(0.1)
    PM10 = read_test(3)
    sleep(0.1)
    print("PM1 = ", PM1, " PM2.5 = ", PM2_5 , " PM10 = ", PM10)
    sleep(1)


## for the geiger
# while True:
#     print(read_test(1))
#     sleep(1)

