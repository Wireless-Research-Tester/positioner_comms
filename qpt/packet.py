import integer as qi

class Constants:
    # Control Chars
    ctrl = [
        b'\x02', # Start-of-Text Char
        b'\x03', # End-of-Text Char
        b'\x06', # Acknowledge Char
        b'\x15', # Not Acknowledge Char
    ]

    # Escape Char
    esc = [
        b'\x1b', 
    ]

    # Positioner Commands 
    cmd = [
        b'\x31', # Get Status/Jog
        b'\x33', # Move To Entered Coordinates
        b'\x34', # Move To Delta Coordinates
        b'\x35', # Move To Absolute 0/0
        b'\x70', # Get Pan & Tilt Angle Correction
        b'\x71', # Get Soft Limit
        b'\x80', # Set Pan & Tilt Angle Correction
        b'\x81', # Set Soft Limit to Current Possition
        b'\x82', # Align Angles to Center
        b'\x84', # Clear Angle Correction
        b'\x90', # Get Center Position in RU's'
        b'\x91', # Set Center Position
        b'\x92', # Get Minimum Speeds
        b'\x93', # Set Minimum Speeds
        b'\x95', # Get/Set Motor and Resolver Direction
        b'\x96', # Get/Set Communication Timeout
        b'\x97', # Get/Set Heater Power Sharing
        b'\x98', # Get Maximum Speeds
        b'\x99', # Set Maximum Speeds
    ]

    # used to set and clear bit 7 in command/data/LRC bytes that match control chars
    ESC_MASK = int.from_bytes(b'\x80', byteorder='little')

def generate_LRC(data):
    """Generates LRC Checksum for packet based on data.

    data -> Bytes representing the command number and packet data to be transmitted.
    returns -> Byte representation of the LRC checksum for the given data.
    """
    checksum = 0
    for item in data:
        checksum = checksum ^ item
    return (checksum).to_bytes(1, byteorder='little')

def valid_LRC(data):
    """Determines if the LRC Checksum of a packet is valid.

    data -> Bytes representing the command number, packet data, and LRC checksum of 
            a received packet.
    returns -> True if the transmitted LRC checksum matches the calculated LRC checksum
    """
    checksum = generate_LRC(data)
    if checksum == b'\x00':
        return True
    return False

def insert_esc(data):
    """Inserts escape char 0x1b before any data value, including the LRC,
    that matches a control char, then sets bit 7 of the byte matching a control char.

    data -> Bytes representing the complete packet, aside from the STX and ETX control chars.
    returns -> Packet that is ready to transmit once STX and ETX are added.
    """
    tx_packet = bytes()
    for i in data:
        val = i.to_bytes(1, byteorder='little')
        if val in Constants.ctrl or val in Constants.esc:
            tx_packet += b'\x1b'
            tx_packet += (i | Constants.ESC_MASK).to_bytes(1, byteorder='little')
        else:
            tx_packet += val
    return tx_packet

def strip_esc(data):
    """Strips escape char 0x1b from infront of data values, including the LRC,
    that match a control char, then clears bit 7 of the byte matching a control char.

    data -> Bytes representing the complete packet, including the STX and ETX control chars.
    returns -> Packet that is ready to be parsed.
    """
    rx = list(data)
    rx_packet = bytes()
    include_next = False
    for i in range(len(rx)):
        val = rx[i].to_bytes(1, byteorder='little')
        if val not in Constants.esc or include_next is True:
            rx_packet += val
            include_next = False
        else:
            rx[i+1] = (rx[i+1] & (~Constants.ESC_MASK))
            include_next = True
    return rx_packet

def get_status():
    """Command 0x31: "Get Status/Jog"
    Creates packet to query the status of the QPT Positioner.

    returns -> Packet that is ready to transmit.
    """
    return bytes.fromhex('02 31 00 00 00 00 00 31 03') 

def jog_positioner(
        pan_speed,
        pan_dir,
        tilt_speed,
        tilt_dir,
        override_soft_limit=0):
    """Command 0x31: "Get Status/Jog"

    returns -> Packet that is ready to transmit.
    """
    pass

def stop():
    """Command 0x31: "Get Status/Jog"
    Creates packet to STOP the QPT Positioner from continuing an automated move.

    returns -> Packet that is ready to transmit.
    """
    return bytes.fromhex('02 31 1b 82 00 00 00 00 33 03')

def move_to_entered_coords(coord):
    """Command 0x33: "Move To Entered Coordinates"
    Creates packet to move the QPT Positioner to the entered coordinate.

    coord -> qpt.integer.Coordinate to move the positioner to.
    returns -> Packet that is ready to transmit.
    """
    tx_data = bytes(b'\x33' + coord.to_bytes())
    LRC = generate_LRC(tx_data)
    return bytes(b'\x02' + insert_esc(tx_data + LRC) + b'\x03')

def move_to_delta_coords(coord):
    """Command 0x34: "Move To Delta Coordinates"
    Creates a packet to move the QPT Positioner to the delta provided.

    coord -> qpt.integer.Coordinate representing the delta to move the positioner to.
    returns -> Packet that is ready to transmit.
    """
    tx_data = bytes(b'\x34' + coord.to_bytes())
    LRC = generate_LRC(tx_data)
    return bytes(b'\x02' + insert_esc(tx_data + LRC) + b'\x03')

def move_to_absolute_zero():
    """Command 0x35: "Move To Absolute 0/0"
    Creates packet to move the QPT Positioner to absolute 0/0.

    returns -> Packet that is ready to transmit.
    """
    return bytes.fromhex('02 35 35 03')

def get_angle_correction():
    """Command 0x70: "Get Pan & Tilt Angle Correction"
    Creates packet to query the QPT Positioner for the current angle correction.

    returns -> Packet that is ready to transmit.
    """
    return bytes.fromhex('02 70 70 03')

# TODO: Implement
def get_soft_limit(axis):
    """Command 0x71: "Get Soft Limit"

    """
    pass

# TODO: Implement
def set_angle_correction(coord):
    """Command 0x80: "Set Pan & Tilt Angle Correction"

    """
    pass

# TODO: Implement
def set_soft_limit_to_current_position(axis):
    """Command 0x81: "Set Soft Limit To Current Position"

    """
    pass

def align_angles_to_center():
    """Command 0x82: "Align Angles To Center"
    Creates packet to set the QPT Positioner's angle corrections so that the 
    current position is considered a center position displaying a pan and tilt
    angle of 0 degrees.

    returns -> Packet that is ready to transmit.
    """
    return bytes.fromhex('02 82 82 03')

def clear_angle_correction():
    """Command 0x84: "Clear Angle Correction"
    Creates packet to reset any angular corrections to zero, realigning the platform
    angular display to the true 0/0 position.

    returns -> Packet that is ready to transmit.
    """
    return bytes.fromhex('02 84 84 03')

def get_center_position_in_RUs():
    """Command 0x90: "Get Center Position in RU's"
    Creates packet to get the center position in resolver units (RU's)

    returns -> Packet that is ready to transmit.
    """
    return bytes.fromhex('02 90 90 03')

def set_center_position():
    """Command 0x91: "Set Center Position"

    returns -> Packet that is ready to transmist.
    """
    return bytes.fromhex('02 91 91 03')

def get_minimum_speeds():
    """Command 0x92: "Get Minimum Speeds"

    returns -> Packet that is ready to transmit.
    """
    return bytes.fromhex('02 92 92 03')

# TODO: Implement
def set_minimum_speeds(pan_speed, tilt_speed):
    """Command 0x93: "Set Minimum Speeds"

    returns -> Packet that is ready to transmit.
    """
    pass

# TODO: Implement
def get_set_motor_and_RU_direction(
        query, 
        tilt_RU_dir, 
        tilt_motor_dir, 
        pan_RU_dir, 
        pan_motor_dir):
    """Command 0x95: "Get/Set Motor and Resolver Direction"

    returns -> Packet that is ready to transmit.
    """
    pass

# TODO: Implement
def get_set_communication_timeout(query, timeout):
    """Command 0x96: "Get/Set Communication Timeout"

    returns -> Packet that is ready to transmit.
    """
    pass

def get_maximum_speeds():
    """Command 0x98: "Get Maximum Speeds"

    returns -> Packet that is ready to transmit.
    """
    return bytes.fromhex('02 98 98 03')

# TODO: Implement
def set_maximum_speeds(pan_speed, tilt_speed):
    """Command 0x99: "Set Maximum Speeds"

    returns -> Packet that is ready to transmit.
    """
    pass


