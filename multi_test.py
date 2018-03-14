import unittest
from multi import I2C_controller, PTR_ARR

class MultiTestClass(unittest.TestCase):

    # When initalized the I2C should be reset to 1
    def test_init(self):
        tester = I2C_controller()
        self.assertEqual(255, tester.I2C_reader())

    # Testing the update of all the pins and checking the Board returns correct values
    def test_set_id(self):
        tester = I2C_controller()
        for i in range(1,6):
            tester.I2C_setup(PTR_ARR[i])
            self.assertEqual(PTR_ARR[i], tester.I2C_reader())

    
if __name__ == "__main__":
    unittest.main()