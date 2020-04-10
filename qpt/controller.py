import pyvisa as visa
import parser as par
import packet as pkt
import integer as qi

class CommsManager:
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
        while tries < self._LIMIT and rx == -1:
            rx = self.positioner_query(pkt.get_status())
        if rx == -1:
            return False
        else:
            return True

    def positioner_query(self, msg):
        self.comms.write_raw(msg)
        try:
            rx = self.comms.read_raw()
        except visa.errors.VisaIOError as err:
            rx = -1
        return rx


class QPT_Positioner:
    def __init__(self):
        self.cm = CommsManager()
        self.parser = par.Parser()

        self.executing = False
        self.curr_pos = qi.Coordinate(0, 0)
        self.dest_pos = qi.Coordinate(0, 0)
        self.pan_min_speed = 0
        self.pan_max_speed = 0
        self.pan_status = bytes()
        self.tilt_min_speed = 0
        self.tilt_max_speed = 0
        self.tilt_status = bytes()
        self.gen_status = bytes()
        self.center_pos = qi.Coordinate(0, 0)
        self.comms_timeout = 0
        self.cw_softlimit = 0
        self.ccw_softlimit = 0
        self.up_softlimit = 0
        self.down_softlimit = 0


    def move_to(self, pan, tilt, move_type='stop'):
        if move_type == 'abs':
            coord = qi.Coordinate(pan,tilt)
            rx = self.cm.positioner_query(pkt.move_to_entered_coords(coord))
        elif move_type == 'delta':
            coord = qi.Coordinate(pan,tilt)
            rx = self.cm.positioner_query(pkt.move_to_delta_coords(coord))
        elif move_type == 'zero':
            rx = self.cm.positioner_query(pkt.move_to_absolute_zero())
        else:
            rx = self.cm.positioner_query(pkt.stop())
        return rx


