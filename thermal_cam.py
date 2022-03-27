# A class to interface with the I2C MLX90640 Thermal Sensor
#   Written by Team CCC
#


## [imports]
import board                    # Used to interface with the i2c bus on the raspberry pi
import busio                    # Used to interface with the i2c bus on the raspberry pi
import adafruit_mlx90640        # Used to control the MLX90640
import matplotlib.pyplot as plt # Used to interpolate the data frame from the MLX90640
import numpy as np              # Used to interpolate the data frame from the MLX90640
import io                       # Used to hold interplated bytes data
import base64                   # Used to encode the image


# Main Class
#   Functions:
#     Constructor   - Sets up up the MLX90640 Sensor
#     getData       - Returns the current image
class thermal_camera:
    # Constructor class, sets camera up
    def __init__(self):

        # Creating the I2C instance
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency= 800000)

        # Creating the MLX90640 Object
        self.mlx = adafruit_mlx90640.MLX90640(self.i2c)

        # Setting the refresh rate of the camera
        self.mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
        return

    # Gets the image from the camera and encodes it to be useful to the GUI
    def get_image(self):

        # Creating the array to hold the raw camera data
        frame = [0] * 768

        # Getting teh raw camera data and dumping it in the array
        self.mlx.getFrame(frame)

        # Resizing the array to a 24x32 image
        frame = np.reshape(frame, (24, 32))

        # Creating the bytes object to hold the image data
        my_stringIObytes = io.BytesIO() 

        # Turing visual plotting off
        plt.ioff()

        # Creating a new figure
        fig = plt.figure(frameon=False)

        # Reamoving axis
        ax = plt.Axes(fig, [0, 0, 1, 1])
        ax.set_axis_off()
        fig.add_axes(ax)

        # Plotting the interpolated frame
        plt.imshow(frame, interpolation='bilinear', aspect='auto')

        # Saving the image to the bytes object
        plt.savefig(my_stringIObytes, format='jpeg')

        # Encoding the raw binary data to base64
        my_stringIObytes.seek(0)
        my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
        my_base64_jpgData = my_base64_jpgData.decode("utf-8")

        # Closing old plot to not cause memory issues
        plt.close(fig)

        # Returning the frame
        return my_base64_jpgData

# Testing
'''
cam = thermal_camera()
print(cam.get_image())
'''

