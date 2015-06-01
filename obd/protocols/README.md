Notes
-----

Each protocol object is callable, and accepts a list of raw input strings, and returns a list of parsed `Message` objects. The `data_bytes` field will contain a list of integers, corresponding to all relevant data returned by the command.

*Note: `Message.data_bytes` does not refer to the full data field of a message, but rather a subset of this field. Things like Mode/PID/PCI bytes are removed. However, `Frame.data_bytes` DOES include the full data field (per-spec), for each frame.*

For example, these are the resultant `Message.data_bytes` fields for some single frame messages:

```
A CAN Message:
7E8 06 41 00 BE 7F B8 13
             [  data   ]

A J1850 Message:
48 6B 10 41 00 BE 7F B8 13 FF
               [  data   ]
``` 

Subclassing `Protocol`
---------------------

All protocol objects must implement two functions:

----------------------------------------

#### create_frame(self, raw)

Recieves a single frame (in string form), and is responsible for parsing and returning a new `Frame` object. If the frame is invalid, or the parse fails, this function should return `None`, and the frame will be dropped.

----------------------------------------

#### create_message(self, frames, tx_id)

Recieves a list of `Frame`s, and is responsible for assembling them into a finished `Message` object. This is where multi-line responses are assembled, and the final `Message.data_bytes` field is filled. If the message is found to be invalid, this function should return `None`, and the entire message will be dropped.


Inheritance structure
---------------------

```
Protocol
    UnknownProtocol
    LegacyProtocol
        SAE_J1850_PWM
        SAE_J1850_VPM
        ISO_9141_2
        ISO_14230_4_5baud
        ISO_14230_4_fast
    CANProtocol
        ISO_15765_4_11bit_500k
        ISO_15765_4_29bit_500k
        ISO_15765_4_11bit_250k
        ISO_15765_4_29bit_250k
        SAE_J1939
```
