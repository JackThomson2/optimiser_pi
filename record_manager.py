import threading
import time
from store_manager import store_manager
from reader import DataStore

class record_manager:
    def __init__(self):
        self.files = store_manager.get_files()

    # Used to instantiate a new recording and store it post recording
    def start_new_recording(self, stop_event):
        reader = DataStore()

        logging_thread = threading.Thread(target=reader.log_data,args=(stop_event,))
        logging_thread.start()
        while not stop_event.is_set():
            time.sleep(1)
        
        logging_thread.join()

        recording = reader.get_storage()

        self.files.append(recording)
        store_manager.store_file(recording)