import smbus2 as smbus
import time
import sys
from sensor import mpu6050

I2C_address = 0x70
I2C_bus_number = 1
I2C_ch_0 = 0x02
I2C_ch_1 = 0x03
I2C_ch_2 = 0x04
I2C_ch_3 = 0x05
I2C_ch_4 = 0x06
I2C_ch_5 = 0x07
I2C_ch_6 = 0x08
I2C_ch_7 = 0x09

PTR_ARR = [
    I2C_ch_0,
    I2C_ch_1,
    I2C_ch_2,
    I2C_ch_3,
    I2C_ch_4,
    I2C_ch_5,
    I2C_ch_6,
    I2C_ch_7
]

class I2C_controller():

    def __init__(self):
        self.bus = smbus.SMBus(I2C_bus_number)
        self.I2C_setup(0xff)

    def I2C_setup(self, i2c_channel_setup):
        self.bus.write_byte(I2C_address, i2c_channel_setup)

    def I2C_reader(self):
        return self.bus.read_byte(I2C_address)
