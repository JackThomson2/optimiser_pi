import unittest
import numpy as np
import threading
import time
import random
from record_manager import record_manager
from store_manager import store_manager
from reader import RANGE
from multi import I2C_controller, PTR_ARR
from sensor import mpu6050

class RecordManagerTestCase(unittest.TestCase):

    # Instantiates a new recording and then checks its been stored
    def test_start_new_recording(self):
        manager = record_manager()

        start_count = manager.get_cache_size()

        stop = threading.Event()
        logging_thread = threading.Thread(target=manager.start_new_recording, args=(stop,))
        logging_thread.start()

        time.sleep(1)

        stop.set()
        logging_thread.join()

        self.assertEqual(manager.get_cache_size(), start_count + 1)

    def test_load_chunk(self):
        manager = record_manager()
        file_list = store_manager.get_files()
        record = random.choice(file_list)
        res = manager.get_send_chunk(record, 0)

        self.assertGreater(len(res),0)

    # Tests that the code is using the cached objects to save computation
    def test_load_cache(self):
        manager = record_manager()
        file_list = store_manager.get_files()
        record = random.choice(file_list)
        res = manager.get_send_chunk(record, 0)

        start = manager.get_cache_size()

        self.assertGreater(len(res),0)

        res = manager.get_send_chunk(record, 1)

        self.assertGreater(len(res),0)
        self.assertEqual(start, manager.get_cache_size())

    # Tests all sensors are configured to the correct range
    def test_init_sensors(self):
        manager = record_manager()
        multi = I2C_controller()
        sensor = mpu6050(0x68)

        manager.setup_sensors()

        for i in range(1,6):
            multi.I2C_setup(PTR_ARR[i])
            self.assertEqual(sensor.read_accel_range(raw=True), RANGE)
            
        
if __name__ == "__main__":
    unittest.main()