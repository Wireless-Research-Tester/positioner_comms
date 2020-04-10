import sys
sys.path.append('D:\\qpt') # adjust to path of qpt folder on system
import integer as qi
import unittest

from packet import *

class PacketTestCase(unittest.TestCase):
    
    def test_generate_checksum(self):
        self.assertEqual(
            generate_LRC(bytes.fromhex('33 33 0a 00 00')), 
            b'\x0a')
        self.assertEqual(
            generate_LRC(bytes.fromhex('31 35 0a 00 00 00 00 80')), 
            b'\x8e')
        self.assertEqual(
            generate_LRC(bytes.fromhex('33 33 0a d9 07')),
            b'\xd4')
        self.assertEqual(
            generate_LRC(bytes.fromhex('33 33 0a d9 07 00 00 a0')), 
            b'\x74')
        self.assertEqual(
            generate_LRC(bytes.fromhex('31 33 0a da 07 00 00 80')), 
            b'\x55')        
        self.assertEqual(
            generate_LRC(bytes.fromhex('35 00 00 a0')), 
            b'\x95')        

    def test_validate_checksum(self):
        self.assertTrue(valid_LRC(bytes.fromhex('33 33 0a 00 00 0a')))
        self.assertFalse(valid_LRC(bytes.fromhex('33 33 0a 00 00 0b')))

    def test_insert_esc(self):
        self.assertEqual(
            insert_esc(bytes.fromhex('31 02 03 00 02 03')), 
            b'\x31\x1b\x82\x1b\x83\x00\x1b\x82\x1b\x83')
        self.assertEqual(
            insert_esc(bytes.fromhex('33 06 15 1b 02 45')), 
            b'\x33\x1b\x86\x1b\x95\x1b\x9b\x1b\x82\x45')

    def test_strip_esc(self):
        self.assertEqual(
            strip_esc(bytes.fromhex('02 31 1b 82 1b 83 00 1b 82 1b 83 03')), 
            b'\x02\x31\x02\x03\x00\x02\x03\x03')
        self.assertEqual(
            strip_esc(bytes.fromhex('06 33 1b 86 1b 95 1b 9b 1b 82 45 03')), 
            b'\x06\x33\x06\x15\x1b\x02\x45\x03')

    def test_get_status(self):
        self.assertEqual(get_status(), b'\x02\x31\x00\x00\x00\x00\x00\x31\x03')

    def test_stop(self):
        self.assertEqual(stop(), b'\x02\x31\x1b\x82\x00\x00\x00\x00\x33\x03')

    def test_move_to_absolute_zero(self):
        self.assertEqual(move_to_absolute_zero(), b'\x02\x35\x35\x03')

    def test_get_angle_correction(self):
        self.assertEqual(get_angle_correction(), b'\x02\x70\x70\x03')

    def test_align_angles_to_center(self):
        self.assertEqual(align_angles_to_center(), b'\x02\x82\x82\x03')

    def test_clear_angle_correction(self):
        self.assertEqual(clear_angle_correction(), b'\x02\x84\x84\x03')

    def test_get_center_position_in_RUs(self):
        self.assertEqual(get_center_position_in_RUs(), b'\x02\x90\x90\x03')

    def test_set_center_position(self):
        self.assertEqual(set_center_position(), b'\x02\x91\x91\x03')

    def test_get_minimum_speeds(self):
        self.assertEqual(get_minimum_speeds(), b'\x02\x92\x92\x03')

    def test_get_maximum_speeds(self):
        self.assertEqual(get_maximum_speeds(), b'\x02\x98\x98\x03')

    def test_move_to_entered_coords(self):
        self.assertEqual(
            move_to_entered_coords(qi.Coordinate(10.00,0.00)), 
            b'\x02\x33\xe8\x1b\x83\x00\x00\xd8\x03')
        self.assertEqual(
            move_to_entered_coords(qi.Coordinate(10.00,10.00)), 
            b'\x02\x33\xe8\x1b\x83\xe8\x1b\x83\x33\x03')

    def test_move_to_delta_coords(self):
        self.assertEqual(
            move_to_delta_coords(qi.Coordinate(10.00,0.00)), 
            b'\x02\x34\xe8\x1b\x83\x00\x00\xdf\x03')
        self.assertEqual(
            move_to_delta_coords(qi.Coordinate(10.00,10.00)), 
            b'\x02\x34\xe8\x1b\x83\xe8\x1b\x83\x34\x03')

# command to run tests in windows powershell from qpt folder
# python -m unittest -v tests/test_packet.py
if __name__=='__main__':
    unittest.main()


