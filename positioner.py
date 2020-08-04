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
import pyvisa as visa
import packet_parser as par
import packet as pkt
import integer as qi
from constants import BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7
import time


class Comms:
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

        # Testing Properties
        self.on = False
        self.time_series = []

    def move_to(self, pan, tilt, move_type='stop'):
        if move_type == 'abs':
            coord = qi.Coordinate(pan,tilt)
            rx = self.comms.positioner_query(pkt.move_to_entered_coords(coord))
        elif move_type == 'delta':
            coord = qi.Coordinate(pan,tilt)
            rx = self.comms.positioner_query(pkt.move_to_delta_coords(coord))
        elif move_type == 'zero':
            rx = self.comms.positioner_query(pkt.move_to_absolute_zero())
        else:
            rx = self.comms.positioner_query(pkt.stop())
        return rx

    def get_position(self):
        rx = self.comms.positioner_query(pkt.get_status())

        if rx is not None:
            rx = pkt.strip_esc(rx)
            curr = qi.Coordinate(rx[2:4], rx[4:6], fromqpt=True)
            
            if len(rx) > 8:
                executing = (rx[8] & int.from_bytes(b'\x40', byteorder='little'))
                self.curr_position = curr
                if executing != 0:
                    self.executing = True
                else:
                    self.executing = False
                return curr
        return None

    def record_move(self, pan, tilt, sample_dt):
        i = 0
        self.time_series = []
        t = time.time()
        self.move_to(pan,tilt,'abs')
        curr = self.get_position()
        self.on = True
        while self.on is True:
            i += 1
            t = time.time()
            curr = self.get_position()
            if i > 3 and curr is not None:
                self.time_series.append([i, curr])
                print(self.executing, ' ', i, ' ', curr.pan_angle(), ' ', curr.tilt_angle())
                f = open('move.txt','a')
                f.write(str(curr.pan_angle()) + ',' + str(curr.tilt_angle()) + '\n')
                f.close()
            time.sleep(sample_dt)
            if i > 3:
                self.on = self.executing
        return self.time_series

    def jog_cw(self, pan_speed, target):
        p = par.Packet_Parser()
        rx = self.comms.positioner_query(pkt.get_status())
        p.parse(rx, self)
        self.print_curr()
        t_0 = time.time()
        phi_0 = self.curr_position.pan_angle()

        while self.curr_position.pan_angle() < target.pan_angle():
            rx = self.comms.positioner_query(pkt.jog_positioner(pan_speed, 1, 0, 0))
            p.parse(rx, self)
            time.sleep(.08)

        p.parse(self.comms.positioner_query(pkt.get_status()), self)
        t_f = time.time()
        phi_f = self.curr_position.pan_angle()
        self.print_curr()
        print('angular velocity: {:2.5f} degrees/sec, pan_speed: {:3}'.format(
            ((phi_f - phi_0) / (t_f - t_0)),
            pan_speed))

    def jog_ccw(self, pan_speed, target):
        p = par.Packet_Parser()
        rx = self.comms.positioner_query(pkt.get_status())
        p.parse(rx, self)
        self.print_curr()
        t_0 = time.time()
        phi_0 = self.curr_position.pan_angle()

        while self.curr_position.pan_angle() > target.pan_angle():
            rx = self.comms.positioner_query(pkt.jog_positioner(pan_speed, 0, 0, 0))
            p.parse(rx, self)
            time.sleep(.08)

        p.parse(self.comms.positioner_query(pkt.get_status()), self)
        t_f = time.time()
        phi_f = self.curr_position.pan_angle()
        self.print_curr()
        print('angular velocity: {:2.5f} degrees/sec, pan_speed: {:3}'.format(
            ((phi_0 - phi_f) / (t_f - t_0)),
            pan_speed))     

    def print_curr(self):
        print('Current Position => PAN: {:3.2f}, TILT: {:2.2f}, TIME: {:3.4f}'.format(
            self.curr_position.pan_angle(),
            self.curr_position.tilt_angle(),
            time.time()))

    def update_curr_position(self, rx):
        self.curr_position = qi.Coordinate(rx[2:4], rx[4:6], fromqpt=True)

    def update_pan_status(self, rx):
        self.sfault_cs_soft_limit = bool(rx[6] & BIT7)
        self.sfault_ccw_soft_limit = bool(rx[6] & BIT6)
        self.hfault_cw_hard_limit = bool(rx[6] & BIT5)
        self.hfault_ccw_hard_limit = bool(rx[6] & BIT4)
        self.hfault_pan_timeout = bool(rx[6] & BIT3)
        self.hfault_pan_direction_error = bool(rx[6] & BIT2)
        self.hfault_pan_current_overload = bool(rx[6] & BIT1)
        self.sfault_pan_resolver_fault = bool(rx[6] & BIT0)

    def update_tilt_status(self, rx):
        self.sfault_up_soft_limit = bool(rx[7] & BIT7)
        self.sfault_down_soft_limit = bool(rx[7] & BIT6)
        self.hfault_up_hard_limit = bool(rx[7] & BIT5)
        self.hfault_down_hard_limit = bool(rx[7] & BIT4)
        self.hfault_tilt_timeout = bool(rx[7] & BIT3)
        self.hfault_tilt_direction_error = bool(rx[7] & BIT2)
        self.hfault_tilt_current_overload = bool(rx[7] & BIT1)
        self.sfault_tilt_resolver_fault = bool(rx[7] & BIT0)

    def update_general_status(self, rx):
        self.status_high_res = bool(rx[8] & BIT7)
        self.status_executing = bool(rx[8] & BIT6)
        self.status_dest_coords = bool(rx[8] & BIT5)
        self.status_soft_limit_override = bool(rx[8] & BIT4)
        self.pan_status_cw_moving = bool(rx[8] & BIT3)
        self.pan_status_ccw_moving = bool(rx[8] & BIT2)
        self.tilt_status_up_moving = bool(rx[8] & BIT1)
        self.tilt_status_down_moving = bool(rx[8] & BIT0)

    def update_qpt_status(self, rx):
        self.update_curr_position(rx)
        self.update_pan_status(rx)
        self.update_tilt_status(rx)
        self.update_general_status(rx)

    def update_soft_limits(self, rx):
        if rx[2] == 0 or rx[2] == 1:
            limit = qi.Coordinate(rx[3:5], 0, fromqpt=True).pan_angle()
            if rx[2] == 0:
                self.pan_cw_soft_limit = limit
            elif rx[2] == 1:
                self.pan_ccw_soft_limit = limit
        elif rx[2] == 2 or rx[2] == 3:
            limit = qi.Coordinate(0, rx[3:5], fromqpt=True).tilt_angle()
            if rx[2] == 2:
                self.tilt_up_soft_limit = limit
            elif rx[2] == 3:
                self.tilt_down_soft_limit = limit

    def update_potentiometer_center(self, rx):
        self.pan_center_RU = int.from_bytes(rx[2:4], byteorder='little', signed=True)
        self.tilt_center_RU = int.from_bytes(rx[4:6], byteorder='little', signed=True)

    def update_min_speed(self, rx):
        self.pan_min_speed = rx[2]
        self.tilt_min_speed = rx[3]

    def update_max_speed(self, rx):
        self.pan_max_speed = rx[2]
        self.tilt_max_speed = rx[3]

    def update_angle_corrections(self, rx):
        self.angle_corrections = qi.Coordinate(rx[2:4], rx[4:6], fromqpt=True)

    def update_comm_timeout(self, rx):
        self.comms_timeout = rx[2]    
"""End QPT_Positioner Class"""

