################################################################################
#
#  Description:
#
#
#  Status:
#
#
#  Dependencies:
#      PyVISA Version: 1.10.1
#
#  Author: Thomas Hoover
#  Date: 20200417
#  Built with Python Version: 3.8.2
#
################################################################################
import time
from threading import Lock
import pyvisa as visa
import qpt_ints as qi
import packet as pkt
from constants import BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7
from packet_parser import Parser

class Comms:
    # _COMMS_PORT = 'ASRL1::INSTR'
    # _COMMS_PORT = 'ASRL3::INSTR'
    _COMMS_PORT = 'ASRL8::INSTR'
    _LIMIT = 25

    def __init__(self):
        self.rm = visa.ResourceManager()
        self.comms = self.rm.open_resource(self._COMMS_PORT)
        self.comms.read_termination = b'\x03'
        self.comms.write_termination = b'\x03'
        self.comms.timeout = 30
        self.comms.baud_rate = 9600
        self.comms.stop_bites = visa.constants.StopBits.one
        self.comms.parity = visa.constants.Parity.none
        self.comms.data_bits = 8
        self.connected = self.init_comms_link()

    def init_comms_link(self):
        tries = 0
        rx = self.positioner_query(pkt.get_status())
        while tries < self._LIMIT and rx == None:
            rx = self.positioner_query(pkt.get_status())
        if rx == None:
            return False
        else:
            return True

    def positioner_query(self, msg):
        self.comms.write_raw(msg)
        try:
            time.sleep(.02)
            rx = self.comms.read_raw()
        except visa.errors.VisaIOError as err:
            return None
        return rx

    def clear_rx_buffer(self):
        clear = False
        while clear is False:
            try:
                rx = self.comms.read_raw()
            except visa.errors.VisaIOError as err:
                clear = True
"""End CommsManager Class"""


class Positioner:
    def __init__(self):
        self.comms = Comms()
        self.p = Parser()
        self.curr_lock = Lock()

        # General Properties
        self.executing = False
        self.comms_timeout = False
        self.curr_position = qi.Coordinate(0,0)
        self.dest_position = qi.Coordinate(0,0)
        self.pan_center_RU = 0
        self.tilt_center_RU = 0
        self.status_high_res = True
        self.status_executing = False
        self.status_dest_coords = False
        self.status_soft_limit_override = False
        self.angle_corrections = qi.Coordinate(0,0)

        # Pan Properties
        self.pan_min_speed = 0
        self.pan_max_speed = 0
        self.pan_cw_soft_limit = 0
        self.pan_ccw_soft_limit = 0
        self.pan_status_cw_moving = False
        self.pan_status_ccw_moving = False

        # Pan Status
        self.sfault_cw_soft_limit = False
        self.sfault_ccw_soft_limit = False
        self.hfault_cw_hard_limit = False
        self.hfault_ccw_hard_limit = False
        self.hfault_pan_timeout = False
        self.hfault_pan_direction_error = False
        self.hfault_pan_current_overload = False
        self.sfault_pan_resolver_fault = False

        # Tilt Properties
        self.tilt_min_speed = 0
        self.tilt_max_speed = 0
        self.tilt_up_soft_limit = 0
        self.tilt_down_soft_limit = 0
        self.tilt_status_up_moving = False
        self.tilt_status_down_moving = False

        # Tilt Status
        self.sfault_up_soft_limit = False
        self.sfault_down_soft_limit = False
        self.hfault_up_hard_limit = False
        self.hfault_down_hard_limit = False
        self.hfault_tilt_timeout = False
        self.hfault_tilt_direction_error = False
        self.hfault_tilt_current_overload = False
        self.sfault_tilt_resolver_fault = False

        # Initialize positioner properties and status
        self.update_positioner_stats()
        self.print_curr()

    def move_to(self, pan, tilt, move_type='stop'):
        self.p.parse(self.comms.positioner_query(pkt.set_minimum_speeds(40,40)),self)

        if move_type == 'abs':
            coord = qi.Coordinate(pan,tilt)
            self.p.parse(self.comms.positioner_query(pkt.move_to_entered_coords(coord)),self)
        elif move_type == 'delta':
            coord = qi.Coordinate(pan,tilt)
            self.p.parse(self.comms.positioner_query(pkt.move_to_delta_coords(coord)),self)
        elif move_type == 'zero':
            self.p.parse(self.comms.positioner_query(pkt.move_to_absolute_zero()),self)
        else:
            self.p.parse(self.comms.positioner_query(pkt.stop()),self)

        time.sleep(.08)
        self.p.parse(self.comms.positioner_query(pkt.get_status()),self)

        while self.status_executing is True:
            self.p.parse(self.comms.positioner_query(pkt.get_status()),self)
            time.sleep(.08)

        self.p.parse(self.comms.positioner_query(pkt.set_minimum_speeds(8,17)),self)

    def get_position(self):
        with self.curr_lock:
            curr = self.curr_position
        return curr

    def jog_cw(self, pan_speed, target):
        if self.curr_position.pan_angle() < target.pan_angle():
            rx = self.comms.positioner_query(pkt.jog_positioner(pan_speed, 1, 0, 0))
            self.p.parse(rx, self)

    def jog_ccw(self, pan_speed, target):
        p = Parser()
        rx = self.comms.positioner_query(pkt.get_status())
        p.parse(rx, self)

        while self.curr_position.pan_angle() > target.pan_angle():
            rx = self.comms.positioner_query(pkt.jog_positioner(pan_speed, 0, 0, 0))
            p.parse(rx, self)
            time.sleep(.08)

        p.parse(self.comms.positioner_query(pkt.get_status()), self)

    def jog_up(self, tilt_speed, target):
        if self.curr_position.tilt_angle() < target.tilt_angle():
            rx = self.comms.positioner_query(pkt.jog_positioner(0, 0, tilt_speed, 1))
            self.p.parse(rx, self)

    def jog_down(self, tilt_speed, target):
        p = Parser()
        rx = self.comms.positioner_query(pkt.get_status())
        p.parse(rx, self)
        
        while self.curr_position.tilt_angle() > target.tilt_angle():
            rx = self.comms.positioner_query(pkt.jog_positioner(0, 0, tilt_speed, 0))
            p.parse(rx, self)
            time.sleep(.08)

        p.parse(self.comms.positioner_query(pkt.get_status()), self)

    def print_curr(self):
        with self.curr_lock:
            print('Current Position => PAN: {:3.2f}, TILT: {:2.2f}, TIME: {:3.4f}'.format(
                self.curr_position.pan_angle(),
                self.curr_position.tilt_angle(),
                time.time()))

    def update_positioner_stats(self):
        self.p.parse(self.comms.positioner_query(pkt.get_status()), self)
        self.p.parse(self.comms.positioner_query(pkt.get_angle_correction()), self)
        self.p.parse(self.comms.positioner_query(pkt.get_soft_limit(0)), self)
        self.p.parse(self.comms.positioner_query(pkt.get_soft_limit(1)), self)
        self.p.parse(self.comms.positioner_query(pkt.get_soft_limit(2)), self)
        self.p.parse(self.comms.positioner_query(pkt.get_soft_limit(3)), self)
        self.p.parse(self.comms.positioner_query(pkt.get_minimum_speeds()), self)
        self.p.parse(self.comms.positioner_query(pkt.get_set_communication_timeout(True,0)), self)
        self.p.parse(self.comms.positioner_query(pkt.get_maximum_speeds()), self)

    def print_positioner_stats(self):
        print('General Properties:\n')
                
"""End QPT_Positioner Class"""

