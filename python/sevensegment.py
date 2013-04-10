# -*- coding: utf-8 -*-
import time
import serial
from collections import deque


class SevenSegmentDisplay(object):
    """Control a 7 segment display.

    Segment numbering::

            7
          -----
       2 |     | 6
         |  1  |
          ------
       3 |     | 5
         |     |
          -----   . 8
            4
     
    To display one "1", you need to light up segments 2,5 => in binary: 0b01001000

    """
    CHAR_MAP = {  # Don't forget to convert those values to base-2 integers!
        '0': '00000000', '1': '00110000', '2': '01101101', '3': '01111001',
        '4': '00110011', '5': '01011011', '6': '01011111', '7': '01110000',
        '8': '01111111', '9': '01110011', 'a': '01110111', 'b': '00011111',
        'c': '00001101', 'C': '01001110', 'd': '00111101', 'e': '01001111',
        'f': '01000111', 'g': '01111011', 'h': '00010111', 'H': '00110111',
        'i': '00000100', 'I': '00000110', 'j': '00111000', 'l': '00001110',
        'm': '00000000', 'n': '00010101', 'o': '00011101', 'O': '01111110',
        'p': '01100111', 'q': '01110011', 'r': '00000101', 's': '01011011',
        't': '00001111', 'u': '00011100', 'U': '00111110', 'y': '00110011',
        'z': '01101101', ' ': '00000000', '.': '10000000',
    }

    def __init__(self, device='/dev/ttyUSB0', digits=8):
        """Initialize a new 7 segment display on a serial port.

        Args:
            device:
                Device path to serial device.
            digits:
                Number of digits in the display.

        """
        self.ser = serial.Serial(device, 9600, timeout=1)
        self.digits = digits
        time.sleep(2)  # Wait for serial device to become ready

    def write(self, frames):
        """Write frames to the display. If there are less frames than digits,
        "blank" digits will be appended on the right side."""

        print frames

        # Pad display with "blank digits" 
        if len(frames) < self.digits:
            frames.extend([0] * (self.digits - len(frames)))

        # Convert frames to ascii bytes
        ascii_frames = ''.join(chr(frame) for frame in frames)

        # Write to device
        self.ser.write(ascii_frames)
        self.ser.flush()

    def _convert_string(self, string):
        """Take a string as input, return frame."""
        assert len(string) <= self.digits, 'Max string length: {}'.format(self.digits)
        frame = []
        for char in string:
            frame.append(self.get_char(char))
        return frame

    def write_string(self, string):
        frame = self._convert_string(string)
        self.write(frame)

    def rotate_string(self, string, delay=0.2):
        frame = deque(self._convert_string(string))
        while 1:
            self.write(frame)
            frame.rotate(1)
            time.sleep(delay)

    @classmethod
    def get_char(cls, char):
        if char in cls.CHAR_MAP:
            pattern = cls.CHAR_MAP[char]
        elif char.lower() in cls.CHAR_MAP:
            pattern = cls.CHAR_MAP[char]
        else:
            raise RuntimeError('Character mapping for "{}" not found.'.format(char))
        return int(cls.CHAR_MAP[char], 2)
