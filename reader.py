import time
import threading
import json
import math
from bluetooth import *
from sensor import mpu6050
from multi import I2C_controller, PTR_ARR

CHUNK_SIZE = 30

class DataStore:
    def __init__(self):
        self.data = []
        self.send_buffer = 0
        self.cntr = 0
        self.controller = I2C_controller()
        self.sensor = mpu6050(0x68)
        self.sensor.set_accel_range(int(mpu6050.ACCEL_SCALE_MODIFIER_2G))
    
    # This method is used to start the recording of the data from the sensors
    def log_data(self, stop_event):
        while not stop_event.is_set():
            self.data.append(self.get_all_sensors())
            self.cntr += 1
            time.sleep(0.05)

    # This method will call the multiplexer to switch between all the accelerometers
    # data is returned as an array of objects
    def get_all_sensors(self):
        self.controller.I2C_setup(1)
        return_arr = []
        for i in range(1,6):
            self.controller.I2C_setup(i)
            try:
                data = self.sensor.get_accel_data()
                returnX =  {'x': self.cntr, 'y': data['x']}
                returnY =  {'x': self.cntr, 'y': data['y']}
                returnZ =  {'x': self.cntr, 'y': data['z']}
                return_arr.append({'x': returnX, 'y': returnY, 'z': returnZ})
            except:
                print(f"Error with {i}")
        return return_arr

    # Dumps all the data into JSON
    def get_dump(self):
        return json.dumps(self.data).encode()

    # Used for the initating the sending of the data to the mobile app
    def init_send(self):
        self.send_buffer = 0
        return str(int(math.ceil(len(self.data) / CHUNK_SIZE))).encode()

    # Used to break the data into smaller chunks so at to not break bluetooth
    def get_chunk(self, start=None):
        start_loc = (self.send_buffer if start is None else start) * CHUNK_SIZE
        end_loc = CHUNK_SIZE *( self.send_buffer + 1)
        print(f"Start location {start_loc} end location {end_loc}")
        send_data = self.data[start_loc:end_loc]
        self.send_buffer += 1
        return json.dumps(send_data).encode()