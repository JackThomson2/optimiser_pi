import smbus2 as smbus
import time
import sys
from sensor import mpu6050

I2C_address = 0x70
I2C_bus_number = 1
I2C_ch_0 = 0b00000001
I2C_ch_1 = 0b00000010
I2C_ch_2 = 0b00000100
I2C_ch_3 = 0b00001000
I2C_ch_4 = 0b00010000
I2C_ch_5 = 0b00100000
I2C_ch_6 = 0b01000000
I2C_ch_7 = 0b10000000

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
        self.I2C_setup(1)

    def I2C_setup(self, i2c_channel_setup):
        self.bus.write_byte(I2C_address,i2c_channel_setup)

    def I2C_reader(self):
        return self.bus.read_byte(I2C_address)
