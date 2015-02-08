
from protocol_legacy import SAE_J1850_PWM, \
                            SAE_J1850_VPW, \
                            ISO_9141_2, \
                            ISO_14230_4_5baud, \
                            ISO_14230_4_fast

from protocol_can import ISO_15765_4_11bit_500k, \
                         ISO_15765_4_29bit_500k, \
                         ISO_15765_4_11bit_250k, \
                         ISO_15765_4_29bit_250k, \
                         SAE_J1939


# allow each class to be access by ELM name (the result of an "AT DP\r")
protocols = {
    "SAE J1850 PWM"            : SAE_J1850_PWM,
    "SAE J1850 VPW"            : SAE_J1850_VPW,
    "ISO 9141-2"               : ISO_9141_2,
    "ISO 14230-4 (KWP 5BAUD)"  : ISO_14230_4_5baud,
    "ISO 14230-4 (KWP FAST)"   : ISO_14230_4_fast,
    "ISO 15765-4 (CAN 11/500)" : ISO_15765_4_11bit_500k,
    "ISO 15765-4 (CAN 29/500)" : ISO_15765_4_29bit_500k,
    "ISO 15765-4 (CAN 11/250)" : ISO_15765_4_11bit_250k,
    "ISO 15765-4 (CAN 29/250)" : ISO_15765_4_29bit_250k,
    "SAE J1939"                : SAE_J1939
}


def get(name):
    if name in protocols:
        return protocols[name]
    else:
        return None
