import unittest
from reader import DataStore
import numpy as np

class ReaderTestCase(unittest.TestCase):

    # Used to make sure object is initialised correctly
    def test_init(self):
        reader = DataStore()
        self.assertEqual(len(reader.data), 0)

    # Checking the shape of data returned from the accelerometers
    def test_read(self):
        reader = DataStore()
        result = reader.get_all_sensors()
        shape = np.shape(result)
        self.assertEqual((5,), shape)

if __name__ == "__main__":
    unittest.main()