class Integer:
    _MAX_INT = 32767
    _MIN_INT = -32768

    def __init__(self, val):
        if isinstance(val, int) and val <= self._MAX_INT and val >= self._MIN_INT:
            self._value = int(val).to_bytes(2, byteorder='little', signed=True)
            self._valid = True
        else:
            self._value = -1
            self._valid = False

    def is_valid(self):
        return self._valid

    def lower_byte(self):
        if self._valid:
            return self._value[0].to_bytes(1, byteorder='little')
        return -1

    def upper_byte(self):
        if self._valid:
            return self._value[1].to_bytes(1, byteorder='little')
        return -1

    def to_int(self):
        if self._valid:
            return int.from_bytes(self._value, byteorder='little', signed=True)
        return -1

    def to_bytes(self):
        if self._valid:
            return self._value
        return -1

    def to_hex(self):
        if self._valid:
            return self._value.hex('-')
        return -1


class Coordinate:
    _MAX_PHI = 180.00
    _MIN_PHI = -180.00
    _MAX_THETA = 90.00
    _MIN_THETA = -90.00

    def __init__(self, pan, tilt):
        if (isinstance(pan, int) or isinstance(pan, float)) \
            and (isinstance(tilt, int) or isinstance(tilt, float)) \
            and pan <= self._MAX_PHI and pan >= self._MIN_PHI \
            and tilt <= self._MAX_THETA and tilt >= self._MIN_THETA:
                self._phi = int(pan*100).to_bytes(2, byteorder='little', signed='True')
                self._theta = int(tilt*100).to_bytes(2, byteorder='little', signed='True')
                self._valid = True
        else:
            self._phi = -1
            self._theta = -1
            self._valid = False     

    def is_valid(self):
        return self._valid

    def pan_angle(self):
        if self._valid:
            return int.from_bytes(self._phi, byteorder='little', signed=True) / 100
        return -1

    def tilt_angle(self):
        if self._valid:
            return int.from_bytes(self._theta, byteorder='little', signed=True) / 100
        return -1

    def pan_bytes(self):
        if self._valid:
            return self._phi
        return -1

    def tilt_bytes(self):
        if self._valid:
            return self._theta
        return -1

    def pan_hex(self):
        if self._valid:
            return self._phi.hex('-')
        return -1

    def tilt_hex(self):
        if self._valid:
            return self._theta.hex('-')
        return -1

    def to_bytes(self):
        if self._valid:
            return self._phi + self._theta
        return -1

    def to_hex(self):
        if self._valid:
            return (self._phi + self._theta).hex('-')
        return -1


