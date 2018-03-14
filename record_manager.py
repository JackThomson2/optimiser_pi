import threading
import time
import json
from multi import I2C_controller, PTR_ARR
from store_manager import store_manager
from reader import DataStore, RANGE
from sensor import mpu6050

class record_manager:
    
    def __init__(self):
        self.file_names = store_manager.get_files()
        self.reader_cache = []
        self.last_record = None
    
    # Ensures all the accelerometers are correctly configured
    def setup_sensors(self):
        controller = I2C_controller()
        sensor = mpu6050(0x68)

        for i in range(1,6):
            controller.I2C_setup(PTR_ARR[i])
            time.sleep(1)
            sensor.set_accel_range(RANGE)

    # Used to fisplay all the recordings saved to the device
    def get_all_data(self):
        names = [entry.name for entry in self.file_names]
        return json.dumps(names).encode()

    # Used for debugging and testing
    def get_cache_size(self):
        return len(self.reader_cache)

    # Used to instantiate a new recording and store it post recording
    def start_new_recording(self, stop_event):
        reader = DataStore()

        logging_thread = threading.Thread(target=reader.log_data,args=(stop_event,))
        logging_thread.start()
        while not stop_event.is_set():
            time.sleep(1)
        
        logging_thread.join()

        recording = reader.get_storage()

        self.last_record = reader
        self.reader_cache.append(reader)
        store_manager.store_file(recording)

    # Used for a handshake with device after finishing
    def get_last_data(self):
        return_data = {'done': True, 'duration': self.last_record.recording_time}

        return json.dumps(return_data).encode()

    # Private function for getting a safe object from cache
    def get_my_object(self, file_name):
        sender_object = None
        try:
            pos = self.reader_cache.index(file_name.name)
            sender_object = self.reader_cache[pos]
        except:
            sender_object = store_manager.get_reader_from_name(file_name.path)
            self.reader_cache.append(sender_object)

        return sender_object

    # Used for instantiating a request
    def get_initial_request(self, file_name):
        found = self.get_my_object(file_name)
        return found.init_send()

    # Send record from name
    def get_send_chunk(self, file_name, location):
        found = self.get_my_object(file_name)
        return found.get_chunk(location)