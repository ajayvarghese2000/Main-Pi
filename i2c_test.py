from smbus import SMBus
from time import sleep

bus = SMBus(1)
address = 0x4c

def read_test():
    try:
        dat = bus.read_byte_data(address, 1)
        return dat
    except:
        return "error"
    


while True:
    data_recieved = read_test()
    print(data_recieved)
    sleep(1)

