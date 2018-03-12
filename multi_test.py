import unittest
from multi import I2C_controller

class MultiTestClass(unittest.TestCase):

    # When initalized the I2C should be reset to 1
    def test_init(self):
        tester = I2C_controller()
        self.assertEqual(1, tester.I2C_reader())

    # Testing the update of all the pins and checking the Board returns correct values
    def test_set_id(self):
        tester = I2C_controller()
        for i in range(8):
            tester.I2C_setup(i)
            self.assertEqual(i, tester.I2C_reader())

    
if __name__ == "__main__":
    unittest.main()