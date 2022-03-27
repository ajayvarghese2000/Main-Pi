# A class to interface with the i2C Geiger Counter
#
#   Written by Team CCC
#

## [imports]
from smbus2 import SMBus    # Used to communicate with the i2c bus on pi

# Main Class
#   Functions:
#     Constructor   - Sets up up the Geiger Counter
#     getData       - Returns the CPM
class Geiger_Counter:
    
    # Constructor class, sets drone up
    #   Takes in, the Address the geiger counter is at
    def __init__(self, ADDRESS):

        # Address of the i2c device
        self.ADDRESS = ADDRESS

        # The Number of Blocks of 8 bits to read from the device
        self.BLOCKSIZE = 2   # [WARNING] If set incorrectly the i2c bus will block out

        # Default value of the geiger counter
        self.combine = 0

        return

    def getData(self, BUS):
        # Attempt read from bus
        try:
            # Attempt read from device
            dat = BUS.read_i2c_block_data(self.ADDRESS, 1, self.BLOCKSIZE)

            # Combine the Values
            self.combine = dat[1] << 8 | dat[0]

            # Retrun the Value
            return self.combine, 0
        # Returns 1 on failure
        except:
            return self.combine, 1

'''
# Testing
geiger = Geiger_Counter(0x4d)

print(geiger.getData())
'''