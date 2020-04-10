import sys
sys.path.append('D:\\qpt') # adjust to path of qpt folder on the system
import unittest

from integer import *

class IntegerTestCase(unittest.TestCase):

    def test_is_valid(self):
        f = 'failed is_valid()'
        self.assertTrue(Integer(32767).is_valid(), f)
        self.assertTrue(Integer(-32768).is_valid(), f)
        self.assertTrue(Integer(0).is_valid(), f)
        self.assertFalse(Integer(65000).is_valid(), f)
        self.assertTrue(Integer(1800).is_valid(), f)
        self.assertTrue(Integer(-1800).is_valid(), f)
        self.assertFalse(Integer(3.2).is_valid(), f)
        self.assertFalse(Integer('hi').is_valid(), f)
        self.assertFalse(Integer(32768).is_valid(), f)
        self.assertFalse(Integer(-32769).is_valid(), f)

    def test_lower_byte(self):
        f = 'failed lower_byte()'
        self.assertEqual(Integer(32767).lower_byte(), b'\xff', f)
        self.assertEqual(Integer(-32768).lower_byte(), b'\x00', f)
        self.assertEqual(Integer(0).lower_byte(), b'\x00', f)
        self.assertEqual(Integer(65000).lower_byte(), -1, f)
        self.assertEqual(Integer(1800).lower_byte(), b'\x08', f)
        self.assertEqual(Integer(-1800).lower_byte(), b'\xf8', f)
        self.assertEqual(Integer(3.2).lower_byte(), -1, f)
        self.assertEqual(Integer('hi').lower_byte(), -1, f)
        self.assertEqual(Integer(32768).lower_byte(), -1, f)
        self.assertEqual(Integer(-32769).lower_byte(), -1, f)

    def test_upper_byte(self):
        f = 'failed upper_byte()'
        self.assertEqual(Integer(32767).upper_byte(), b'\x7f', f)
        self.assertEqual(Integer(-32768).upper_byte(), b'\x80', f)
        self.assertEqual(Integer(0).upper_byte(), b'\x00', f)
        self.assertEqual(Integer(65000).upper_byte(), -1, f)
        self.assertEqual(Integer(1800).upper_byte(), b'\x07', f)
        self.assertEqual(Integer(-1800).upper_byte(), b'\xf8', f)
        self.assertEqual(Integer(3.2).upper_byte(), -1, f)
        self.assertEqual(Integer('hi').upper_byte(), -1, f)
        self.assertEqual(Integer(32768).upper_byte(), -1, f)
        self.assertEqual(Integer(-32769).upper_byte(), -1, f)

    def test_to_int(self):
        f = 'failed to_int()'
        self.assertEqual(Integer(32767).to_int(), 32767, f)
        self.assertEqual(Integer(-32768).to_int(), -32768, f)
        self.assertEqual(Integer(0).to_int(), 0, f)
        self.assertEqual(Integer(65000).to_int(), -1, f)
        self.assertEqual(Integer(1800).to_int(), 1800, f)
        self.assertEqual(Integer(-1800).to_int(), -1800, f)
        self.assertEqual(Integer(3.2).to_int(), -1, f)
        self.assertEqual(Integer('hi').to_int(), -1, f)
        self.assertEqual(Integer(32768).to_int(), -1, f)
        self.assertEqual(Integer(-32769).to_int(), -1, f)

    def test_to_bytes(self):
        f = 'failed to_bytes()'
        self.assertEqual(Integer(32767).to_bytes(), bytes(b'\xff\x7f'), f)
        self.assertEqual(Integer(-32768).to_bytes(), bytes(b'\x00\x80'), f)
        self.assertEqual(Integer(0).to_bytes(), bytes(b'\x00\x00'), f)
        self.assertEqual(Integer(65000).to_bytes(), -1, f)
        self.assertEqual(Integer(1800).to_bytes(), bytes(b'\x08\x07'), f)
        self.assertEqual(Integer(-1800).to_bytes(), bytes(b'\xf8\xf8'), f)
        self.assertEqual(Integer(3.2).to_bytes(), -1, f)
        self.assertEqual(Integer('hi').to_bytes(), -1, f)
        self.assertEqual(Integer(32768).to_bytes(), -1, f)
        self.assertEqual(Integer(-32769).to_bytes(), -1, f)

    def test_to_hex(self):
        f = 'failed to_hex()'
        self.assertEqual(Integer(32767).to_hex(), bytes(b'\xff\x7f').hex('-'), f)
        self.assertEqual(Integer(-32768).to_hex(), bytes(b'\x00\x80').hex('-'), f)
        self.assertEqual(Integer(0).to_hex(), bytes(b'\x00\x00').hex('-'), f)
        self.assertEqual(Integer(65000).to_hex(), -1, f)
        self.assertEqual(Integer(1800).to_hex(), bytes(b'\x08\x07').hex('-'), f)
        self.assertEqual(Integer(-1800).to_hex(), bytes(b'\xf8\xf8').hex('-'), f)
        self.assertEqual(Integer(3.2).to_hex(), -1, f)
        self.assertEqual(Integer('hi').to_hex(), -1, f)
        self.assertEqual(Integer(32768).to_hex(), -1, f)
        self.assertEqual(Integer(-32769).to_hex(), -1, f)


class CoordinateTestCase(unittest.TestCase):

    def test_is_valid(self):
        f = 'failed is_valid()'
        self.assertTrue(Coordinate(180.00, 90.00).is_valid(), f)
        self.assertFalse(Coordinate(181.00, 90.00).is_valid(), f)
        self.assertFalse(Coordinate(180.00, 91.00).is_valid(), f)
        self.assertTrue(Coordinate(-180.00, -90.00).is_valid(), f)
        self.assertFalse(Coordinate(-181.00, -90.00).is_valid(), f)
        self.assertFalse(Coordinate(-180.00, -91.00).is_valid(), f)
        self.assertTrue(Coordinate(180, 90).is_valid(), f)
        self.assertFalse(Coordinate(181, 90).is_valid(), f)
        self.assertFalse(Coordinate(180, 91).is_valid(), f)
        self.assertTrue(Coordinate(-180, -90).is_valid(), f)
        self.assertFalse(Coordinate(-181, -90).is_valid(), f)
        self.assertFalse(Coordinate(-180, -91).is_valid(), f)
        self.assertFalse(Coordinate(-1000, -1000).is_valid(), f)
        self.assertFalse(Coordinate(1000, 1000).is_valid(), f)
        self.assertFalse(Coordinate('hi', 'bye').is_valid(), f)
        self.assertTrue(Coordinate(59.02, -18.34).is_valid(), f)
        self.assertTrue(Coordinate(-142.32, 87.2).is_valid(), f)
        self.assertTrue(Coordinate(59, -18).is_valid(), f)
        self.assertTrue(Coordinate(-142, 87).is_valid(), f)
        self.assertFalse(Coordinate(50.0, 'hi').is_valid(), f)
        self.assertFalse(Coordinate('bye', 30.0).is_valid(), f)

    def test_pan_angle(self):
        f = 'failed pan_angle()'
        self.assertEqual(Coordinate(180.00, 90.00).pan_angle(), 180.00, f)
        self.assertEqual(Coordinate(181.00, 90.00).pan_angle(), -1, f)
        self.assertEqual(Coordinate(180.00, 91.00).pan_angle(), -1, f)
        self.assertEqual(Coordinate(-180.00, -90.00).pan_angle(), -180.00, f)
        self.assertEqual(Coordinate(-181.00, -90.00).pan_angle(), -1, f)
        self.assertEqual(Coordinate(-180.00, -91.00).pan_angle(), -1, f)
        self.assertEqual(Coordinate(180, 90).pan_angle(), 180.00, f)
        self.assertEqual(Coordinate(181, 90).pan_angle(), -1, f)
        self.assertEqual(Coordinate(180, 91).pan_angle(), -1, f)
        self.assertEqual(Coordinate(-180, -90).pan_angle(), -180.00, f)
        self.assertEqual(Coordinate(-181, -90).pan_angle(), -1, f)
        self.assertEqual(Coordinate(-180, -91).pan_angle(), -1, f)
        self.assertEqual(Coordinate(-1000, -1000).pan_angle(), -1, f)
        self.assertEqual(Coordinate(1000, 1000).pan_angle(), -1, f)
        self.assertEqual(Coordinate('hi', 'bye').pan_angle(), -1, f)
        self.assertEqual(Coordinate(59.02, -18.34).pan_angle(), 59.02, f)
        self.assertEqual(Coordinate(-142.32, 87.2).pan_angle(), -142.32, f)
        self.assertEqual(Coordinate(59, -18).pan_angle(), 59.00, f)
        self.assertEqual(Coordinate(-142, 87).pan_angle(), -142.00, f)
        self.assertEqual(Coordinate(50.0, 'hi').pan_angle(), -1, f)
        self.assertEqual(Coordinate('bye', 30.0).pan_angle(), -1, f)

    def test_tilt_angle(self):
        f = 'failed tilt_angle()'
        self.assertEqual(Coordinate(180.00, 90.00).tilt_angle(), 90.00, f)
        self.assertEqual(Coordinate(181.00, 90.00).tilt_angle(), -1, f)
        self.assertEqual(Coordinate(180.00, 91.00).tilt_angle(), -1, f)
        self.assertEqual(Coordinate(-180.00, -90.00).tilt_angle(), -90.00, f)
        self.assertEqual(Coordinate(-181.00, -90.00).tilt_angle(), -1, f)
        self.assertEqual(Coordinate(-180.00, -91.00).tilt_angle(), -1, f)
        self.assertEqual(Coordinate(180, 90).tilt_angle(), 90.00, f)
        self.assertEqual(Coordinate(181, 90).tilt_angle(), -1, f)
        self.assertEqual(Coordinate(180, 91).tilt_angle(), -1, f)
        self.assertEqual(Coordinate(-180, -90).tilt_angle(), -90.00, f)
        self.assertEqual(Coordinate(-181, -90).tilt_angle(), -1, f)
        self.assertEqual(Coordinate(-180, -91).tilt_angle(), -1, f)
        self.assertEqual(Coordinate(-1000, -1000).tilt_angle(), -1, f)
        self.assertEqual(Coordinate(1000, 1000).tilt_angle(), -1, f)
        self.assertEqual(Coordinate('hi', 'bye').tilt_angle(), -1, f)
        self.assertEqual(Coordinate(59.02, -18.34).tilt_angle(), -18.34, f)
        self.assertEqual(Coordinate(-142.32, 87.2).tilt_angle(), 87.20, f)
        self.assertEqual(Coordinate(59, -18).tilt_angle(), -18.00, f)
        self.assertEqual(Coordinate(-142, 87).tilt_angle(), 87, f)
        self.assertEqual(Coordinate(50.0, 'hi').tilt_angle(), -1, f)
        self.assertEqual(Coordinate('bye', 30.0).tilt_angle(), -1, f)

    def test_pan_bytes(self):
        f = 'failed pan_bytes()'
        self.assertEqual(Coordinate(180.00, 90.00).pan_bytes(), bytes(b'\x50\x46'), f)
        self.assertEqual(Coordinate(181.00, 90.00).pan_bytes(), -1, f)
        self.assertEqual(Coordinate(180.00, 91.00).pan_bytes(), -1, f)
        self.assertEqual(Coordinate(-180.00, -90.00).pan_bytes(), bytes(b'\xb0\xb9'), f)
        self.assertEqual(Coordinate(-181.00, -90.00).pan_bytes(), -1, f)
        self.assertEqual(Coordinate(-180.00, -91.00).pan_bytes(), -1, f)
        self.assertEqual(Coordinate(180, 90).pan_bytes(), bytes(b'\x50\x46'), f)
        self.assertEqual(Coordinate(181, 90).pan_bytes(), -1, f)
        self.assertEqual(Coordinate(180, 91).pan_bytes(), -1, f)
        self.assertEqual(Coordinate(-180, -90).pan_bytes(), bytes(b'\xb0\xb9'), f)
        self.assertEqual(Coordinate(-181, -90).pan_bytes(), -1, f)
        self.assertEqual(Coordinate(-180, -91).pan_bytes(), -1, f)
        self.assertEqual(Coordinate(-1000, -1000).pan_bytes(), -1, f)
        self.assertEqual(Coordinate(1000, 1000).pan_bytes(), -1, f)
        self.assertEqual(Coordinate('hi', 'bye').pan_bytes(), -1, f)
        self.assertEqual(Coordinate(59.02, -18.34).pan_bytes(), bytes(b'\x0e\x17'), f)
        self.assertEqual(Coordinate(-142.32, 87.2).pan_bytes(), bytes(b'\x68\xc8'), f)
        self.assertEqual(Coordinate(59, -18).pan_bytes(), bytes(b'\x0c\x17'), f)
        self.assertEqual(Coordinate(-142, 87).pan_bytes(), bytes(b'\x88\xc8'), f)
        self.assertEqual(Coordinate(50.0, 'hi').pan_bytes(), -1, f)
        self.assertEqual(Coordinate('bye', 30.0).pan_bytes(), -1, f)

    def test_tilt_bytes(self):
        f = 'failed tilt_bytes()'
        self.assertEqual(Coordinate(180.00, 90.00).tilt_bytes(), b'\x28\x23', f)
        self.assertEqual(Coordinate(181.00, 90.00).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(180.00, 91.00).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(-180.00, -90.00).tilt_bytes(), b'\xd8\xdc', f)
        self.assertEqual(Coordinate(-181.00, -90.00).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(-180.00, -91.00).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(180, 90).tilt_bytes(), b'\x28\x23', f)
        self.assertEqual(Coordinate(181, 90).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(180, 91).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(-180, -90).tilt_bytes(), b'\xd8\xdc', f)
        self.assertEqual(Coordinate(-181, -90).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(-180, -91).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(-1000, -1000).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(1000, 1000).tilt_bytes(), -1, f)
        self.assertEqual(Coordinate('hi', 'bye').tilt_bytes(), -1, f)
        self.assertEqual(Coordinate(59.02, -18.34).tilt_bytes(), b'\xd6\xf8', f)
        self.assertEqual(Coordinate(-142.32, 87.2).tilt_bytes(), b'\x10\x22', f)
        self.assertEqual(Coordinate(59, -18).tilt_bytes(), b'\xf8\xf8', f)
        self.assertEqual(Coordinate(-142, 87).tilt_bytes(), b'\xfc\x21', f)
        self.assertEqual(Coordinate(50.0, 'hi').tilt_bytes(), -1, f)
        self.assertEqual(Coordinate('bye', 30.0).tilt_bytes(), -1, f)

    def test_pan_hex(self):
        f = 'failed pan_hex()'
        self.assertEqual(Coordinate(180.00, 90.00).pan_hex(), bytes(b'\x50\x46').hex('-'), f)
        self.assertEqual(Coordinate(181.00, 90.00).pan_hex(), -1, f)
        self.assertEqual(Coordinate(180.00, 91.00).pan_hex(), -1, f)
        self.assertEqual(Coordinate(-180.00, -90.00).pan_hex(), bytes(b'\xb0\xb9').hex('-'), f)
        self.assertEqual(Coordinate(-181.00, -90.00).pan_hex(), -1, f)
        self.assertEqual(Coordinate(-180.00, -91.00).pan_hex(), -1, f)
        self.assertEqual(Coordinate(180, 90).pan_hex(), bytes(b'\x50\x46').hex('-'), f)
        self.assertEqual(Coordinate(181, 90).pan_hex(), -1, f)
        self.assertEqual(Coordinate(180, 91).pan_hex(), -1, f)
        self.assertEqual(Coordinate(-180, -90).pan_hex(), bytes(b'\xb0\xb9').hex('-'), f)
        self.assertEqual(Coordinate(-181, -90).pan_hex(), -1, f)
        self.assertEqual(Coordinate(-180, -91).pan_hex(), -1, f)
        self.assertEqual(Coordinate(-1000, -1000).pan_hex(), -1, f)
        self.assertEqual(Coordinate(1000, 1000).pan_hex(), -1, f)
        self.assertEqual(Coordinate('hi', 'bye').pan_hex(), -1, f)
        self.assertEqual(Coordinate(59.02, -18.34).pan_hex(), bytes(b'\x0e\x17').hex('-'), f)
        self.assertEqual(Coordinate(-142.32, 87.2).pan_hex(), bytes(b'\x68\xc8').hex('-'), f)
        self.assertEqual(Coordinate(59, -18).pan_hex(), bytes(b'\x0c\x17').hex('-'), f)
        self.assertEqual(Coordinate(-142, 87).pan_hex(), bytes(b'\x88\xc8').hex('-'), f)
        self.assertEqual(Coordinate(50.0, 'hi').pan_hex(), -1, f)
        self.assertEqual(Coordinate('bye', 30.0).pan_hex(), -1, f)            

    def test_tilt_hex(self):
        f = 'failed tilt_hex()' 
        self.assertEqual(Coordinate(180.00, 90.00).tilt_hex(), b'\x28\x23'.hex('-'), f)
        self.assertEqual(Coordinate(181.00, 90.00).tilt_hex(), -1, f)
        self.assertEqual(Coordinate(180.00, 91.00).tilt_hex(), -1, f)
        self.assertEqual(Coordinate(-180.00, -90.00).tilt_hex(), b'\xd8\xdc'.hex('-'), f)
        self.assertEqual(Coordinate(-181.00, -90.00).tilt_hex(), -1, f)
        self.assertEqual(Coordinate(-180.00, -91.00).tilt_hex(), -1, f)
        self.assertEqual(Coordinate(180, 90).tilt_hex(), b'\x28\x23'.hex('-'), f)
        self.assertEqual(Coordinate(181, 90).tilt_hex(), -1, f)
        self.assertEqual(Coordinate(180, 91).tilt_hex(), -1, f)
        self.assertEqual(Coordinate(-180, -90).tilt_hex(), b'\xd8\xdc'.hex('-'), f)
        self.assertEqual(Coordinate(-181, -90).tilt_hex(), -1, f)
        self.assertEqual(Coordinate(-180, -91).tilt_hex(), -1, f)
        self.assertEqual(Coordinate(-1000, -1000).tilt_hex(), -1, f)
        self.assertEqual(Coordinate(1000, 1000).tilt_hex(), -1, f)
        self.assertEqual(Coordinate('hi', 'bye').tilt_hex(), -1, f)
        self.assertEqual(Coordinate(59.02, -18.34).tilt_hex(), b'\xd6\xf8'.hex('-'), f)
        self.assertEqual(Coordinate(-142.32, 87.2).tilt_hex(), b'\x10\x22'.hex('-'), f)
        self.assertEqual(Coordinate(59, -18).tilt_hex(), b'\xf8\xf8'.hex('-'), f)
        self.assertEqual(Coordinate(-142, 87).tilt_hex(), b'\xfc\x21'.hex('-'), f)
        self.assertEqual(Coordinate(50.0, 'hi').tilt_hex(), -1, f)
        self.assertEqual(Coordinate('bye', 30.0).tilt_hex(), -1, f)


    def test_to_bytes(self):
        f = 'failed to_bytes()'
        self.assertEqual(Coordinate(180.00, 90.00).to_bytes(), bytes(b'\x50\x46\x28\x23'), f)
        self.assertEqual(Coordinate(181.00, 90.00).to_bytes(), -1, f)
        self.assertEqual(Coordinate(180.00, 91.00).to_bytes(), -1, f)
        self.assertEqual(Coordinate(-180.00, -90.00).to_bytes(), bytes(b'\xb0\xb9\xd8\xdc'), f)
        self.assertEqual(Coordinate(-181.00, -90.00).to_bytes(), -1, f)
        self.assertEqual(Coordinate(-180.00, -91.00).to_bytes(), -1, f)
        self.assertEqual(Coordinate(180, 90).to_bytes(), bytes(b'\x50\x46\x28\x23'), f)
        self.assertEqual(Coordinate(181, 90).to_bytes(), -1, f)
        self.assertEqual(Coordinate(180, 91).to_bytes(), -1, f)
        self.assertEqual(Coordinate(-180, -90).to_bytes(), bytes(b'\xb0\xb9\xd8\xdc'), f)
        self.assertEqual(Coordinate(-181, -90).to_bytes(), -1, f)
        self.assertEqual(Coordinate(-180, -91).to_bytes(), -1, f)
        self.assertEqual(Coordinate(-1000, -1000).to_bytes(), -1, f)
        self.assertEqual(Coordinate(1000, 1000).to_bytes(), -1, f)
        self.assertEqual(Coordinate('hi', 'bye').to_bytes(), -1, f)
        self.assertEqual(Coordinate(59.02, -18.34).to_bytes(), bytes(b'\x0e\x17\xd6\xf8'), f)
        self.assertEqual(Coordinate(-142.32, 87.2).to_bytes(), bytes(b'\x68\xc8\x10\x22'), f)
        self.assertEqual(Coordinate(59, -18).to_bytes(), bytes(b'\x0c\x17\xf8\xf8'), f)
        self.assertEqual(Coordinate(-142, 87).to_bytes(), bytes(b'\x88\xc8\xfc\x21'), f)
        self.assertEqual(Coordinate(50.0, 'hi').to_bytes(), -1, f)
        self.assertEqual(Coordinate('bye', 30.0).to_bytes(), -1, f)

    def test_to_hex(self):
        f = 'failed to_hex()'
        self.assertEqual(Coordinate(180.00, 90.00).to_hex(), bytes(b'\x50\x46\x28\x23').hex('-'), f)
        self.assertEqual(Coordinate(181.00, 90.00).to_hex(), -1, f)
        self.assertEqual(Coordinate(180.00, 91.00).to_hex(), -1, f)
        self.assertEqual(Coordinate(-180.00, -90.00).to_hex(), bytes(b'\xb0\xb9\xd8\xdc').hex('-'), f)
        self.assertEqual(Coordinate(-181.00, -90.00).to_hex(), -1, f)
        self.assertEqual(Coordinate(-180.00, -91.00).to_hex(), -1, f)
        self.assertEqual(Coordinate(180, 90).to_hex(), bytes(b'\x50\x46\x28\x23').hex('-'), f)
        self.assertEqual(Coordinate(181, 90).to_hex(), -1, f)
        self.assertEqual(Coordinate(180, 91).to_hex(), -1, f)
        self.assertEqual(Coordinate(-180, -90).to_hex(), bytes(b'\xb0\xb9\xd8\xdc').hex('-'), f)
        self.assertEqual(Coordinate(-181, -90).to_hex(), -1, f)
        self.assertEqual(Coordinate(-180, -91).to_hex(), -1, f)
        self.assertEqual(Coordinate(-1000, -1000).to_hex(), -1, f)
        self.assertEqual(Coordinate(1000, 1000).to_hex(), -1, f)
        self.assertEqual(Coordinate('hi', 'bye').to_hex(), -1, f)
        self.assertEqual(Coordinate(59.02, -18.34).to_hex(), bytes(b'\x0e\x17\xd6\xf8').hex('-'), f)
        self.assertEqual(Coordinate(-142.32, 87.2).to_hex(), bytes(b'\x68\xc8\x10\x22').hex('-'), f)
        self.assertEqual(Coordinate(59, -18).to_hex(), bytes(b'\x0c\x17\xf8\xf8').hex('-'), f)
        self.assertEqual(Coordinate(-142, 87).to_hex(), bytes(b'\x88\xc8\xfc\x21').hex('-'), f)
        self.assertEqual(Coordinate(50.0, 'hi').to_hex(), -1, f)
        self.assertEqual(Coordinate('bye', 30.0).to_hex(), -1, f)    

# command to run tests in windows powershell from qpt folder
# python -m unittest -v tests/test_integer.py
if __name__=='__main__':
    unittest.main()


