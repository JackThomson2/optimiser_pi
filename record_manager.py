import threading
import time
from store_manager import store_manager
from reader import DataStore

class record_manager:
    def __init__(self):
        self.file_names = store_manager.get_files()
        self.reader_cache = []

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

        self.reader_cache.append(reader)
        store_manager.store_file(recording)

    # Send record from name
    def get_send_chunk(self, file_name, location):
        sender_object = None
        try:
            pos = self.reader_cache.index(file_name.name)
            sender_object = self.reader_cache[pos]
        except:
            sender_object = store_manager.get_reader_from_name(file_name.path)
            self.reader_cache.append(sender_object)

        return sender_object.get_chunk(location)