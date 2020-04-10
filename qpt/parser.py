import packet as pkt
import integer as qi

class Parser:
    def __init__(self):
        self.busy = False
        self.packet = bytes()
        self.data = {}