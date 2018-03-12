import unittest
from record_manager import record_manager
import numpy as np
import threading
import time

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
        
if __name__ == "__main__":
    unittest.main()