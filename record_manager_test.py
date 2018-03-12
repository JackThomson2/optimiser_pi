import unittest
import numpy as np
import threading
import time
import random
from record_manager import record_manager
from store_manager import store_manager

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
        
if __name__ == "__main__":
    unittest.main()