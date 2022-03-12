# A class to simulate some GPS positions within a perscribed area
#
#   Written by Team CCC
#

## [imports]
from random import randint    # Used to generate random data values

# Main Class
#   Functions:
#     Constructor   - Sets up up the fakeGPS with limits and defaults
#     getPos        - Returns the long and lat
#     genLAT        - Generates a lat post based on info from previous pos
#     getLONG       - Generates a long post based on info from previous pos
class GPS:
    def __init__(self):

        ## [Default Values] (centred around Loughborough)
        self.MAXLONG = -1.187
        self.MINLONG = -1.265
        self.MAXLAT= 52.779
        self.MINLAT = 52.761
        self.LAT = 52.77
        self.LONG = -1.226

        ## Scale values to move the possitions about by
        self.LAT_SCALER  = 0.00055
        self.LONG_SCALER = 0.0024
        return

    def getPos(self):
        self.genLAT()
        self.genLONG()
        # print(self.LAT, " ", self.LONG)
        return self.LAT, self.LONG
    
    def genLAT(self):

        # 0 is down and 1 is up on a map
        direction = randint(0,1)

        if(direction == 1):

            # Create a random movement
            self.LAT = self.LAT + (self.LAT_SCALER)

            # Check if we've gone past the max
            if (self.LAT >= self.MAXLAT):
                self.LAT = self.MAXLAT
        
            return
        
        self.LAT = self.LAT - (self.LAT_SCALER)

        # Check if we've gone past the max
        if (self.LAT <= self.MINLAT):
            self.LAT = self.MINLAT
    
        return
    
    def genLONG(self):
        
        # 0 is left and 1 is right on a map
        direction = randint(0,1)

        if(direction == 1):

            # Create a random movement
            self.LONG = self.LONG + (self.LONG_SCALER)

            # Check if we've gone past the max
            if (self.LONG >= self.MAXLONG):
                self.LONG = self.MAXLONG
        
            return

        # Create a random movement
        self.LONG = self.LONG - (self.LONG_SCALER)

        # Check if we've gone past the max
        if (self.LONG <= self.MINLONG):
            self.LONG = self.MINLONG
    
        return
