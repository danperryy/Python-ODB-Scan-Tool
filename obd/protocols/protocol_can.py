

from protocol import Protocol
from obd.utils import ascii_to_bytes
from obd.debug import debug


class CANProtocol(Protocol):

    def __init__(self, baud, id_bits):
        Protocol.__init__(self, baud)
        self.id_bits = id_bits

    def parse_frame(self, frame):

        # pad 11-bit CAN headers out to 32 bits for consistency,
        # since ELM already does this for 29-bit CAN headers
        if self.id_bits == 11:
            frame.raw = "00000" + frame.raw

        raw_bytes = ascii_to_bytes(frame.raw)

        # read header information
        if self.id_bits == 11:
            frame.priority = raw_bytes[2] & 0x0F  # always 7
            frame.addr_mode = raw_bytes[3] & 0xF0  # 0xD0 = functional, 0xE0 = physical

            if frame.addr_mode == 0xD0:
                #untested("11-bit functional request from tester")
                frame.rx_id = raw_bytes[3] & 0x0F  # usually (always?) 0x0F for broadcast
                frame.tx_id = 0xF1  # made-up to mimic all other protocols
            elif raw_bytes[3] & 0x08:
                frame.rx_id = 0xF1  # made-up to mimic all other protocols
                frame.tx_id = raw_bytes[3] & 0x07
            else:
                #untested("11-bit message header from tester (functional or physical)")
                frame.tx_id = 0xF1  # made-up to mimic all other protocols
                frame.rx_id = raw_bytes[3] & 0x07

        else: # self.id_bits == 29:
            frame.priority  = raw_bytes[0]  # usually (always?) 0x18
            frame.addr_mode = raw_bytes[1]  # DB = functional, DA = physical
            frame.rx_id     = raw_bytes[2]  # 0x33 = broadcast (functional)
            frame.tx_id     = raw_bytes[3]  # 0xF1 = tester ID

        frame.data_bytes = raw_bytes[5:]


    def parse_message(self, message):
        if len(message.frames) == 1:
            message.data_bytes = message.frames[0].data_bytes
        else:
            debug("Recieved multi-frame response. Can't parse those yet")


##############################################
#                                            #
# Here lie the class stubs for each protocol #
#                                            #
##############################################



class ISO_15765_4_11bit_500k(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=500000, id_bits=11)


class ISO_15765_4_29bit_500k(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=500000, id_bits=29)


class ISO_15765_4_11bit_250k(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=250000, id_bits=11)


class ISO_15765_4_29bit_250k(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=250000, id_bits=29)


class SAE_J1939(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=250000, id_bits=29)
