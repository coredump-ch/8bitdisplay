# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import time
import logging
from collections import deque
from itertools import islice

import serial


class Segments(object):
    MID = 1
    NW = 2
    SW = 4
    S = 8
    SE = 16
    NE = 32
    N = 64
    DOT = 128


class Shapes(object):
    TOP_CIRCLE = Segments.MID | Segments.NW | Segments.N | Segments.NE
    BOTTOM_CIRCLE = Segments.MID | Segments.SW | Segments.S | Segments.SE
    LEFT_BAR = Segments.NW | Segments.SW
    RIGHT_BAR = Segments.NE | Segments.SE


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

    To display one "7", you need to light up segments 5,6,7 => in binary: 0b01110000

    """
    CHAR_MAP = {  # Don't forget to convert those values to base-2 integers!
        '0': '00000000', '1': '00110000', '2': '01101101', '3': '01111001',
        '4': '00110011', '5': '01011011', '6': '01011111', '7': '01110000',
        '8': '01111111', '9': '01110011', 'a': '01110111', 'b': '00011111',
        'c': '00001101', 'C': '01001110', 'd': '00111101', 'e': '01001111',
        'f': '01000111', 'g': '01111011', 'h': '00010111', 'H': '00110111',
        'i': '00000100', 'I': '00000110', 'j': '00111000', 'k': '00001101',
        'l': '00001110', 'm': '00000000', 'n': '00010101', 'o': '00011101',
        'O': '01111110', 'ö': '01011101', 'p': '01100111', 'q': '01110011',
        'r': '00000101', 's': '01011011', 't': '00001111', 'u': '00011100',
        'U': '00111110', 'y': '00110011', 'z': '01101101', ' ': '00000000',
        '.': '10000000', '-': '00000001', '_': '00001000', '=': '00001001',
        '!': '10100000',
    }

    def __init__(self, device='/dev/ttyUSB0', digits=8, timeout=1):
        """Initialize a new 7 segment display on a serial port.

        Args:
            device:
                Device path to serial device.
            digits:
                Number of digits in the display.
            timeout:
                The writeTimeout. See pyserial docs for more information. (Default: 1).

        """
        self.ser = serial.Serial(device, 9600, timeout=timeout, writeTimeout=timeout)
        self.digits = digits
        time.sleep(2)  # Wait for serial device to become ready

    def write(self, frames):
        """Write frames to the display. If there are less frames than digits,
        "blank" digits will be appended on the right side."""

        logging.debug('Writing {}'.format(frames))

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
        frame = []
        for char in string:
            frame.append(self.get_char(char))
        return frame

    def write_string(self, string):
        """Write a string with max length ``self.digits`` to the display."""
        assert len(string) <= self.digits, 'Max string length: {}'.format(self.digits)
        frame = self._convert_string(string)
        self.write(frame)

    def rotate_string(self, string, delay=0.2, repeat=-1):
        """Write a scrolling/rotating string to the display.

        Args:
            string:
                The string to write to the display.
            delay:
                Delay time between a shift (Default: 0.2).
            repeat:
                How many times to repeat the string. Use ``-1`` for infinite
                scrolling. (Default: -1).
        """
        frame = deque(self._convert_string(string))
        shifts = repeat * len(string) + 1 if repeat > 0 else 1
        while shifts > 0:
            length = min(8, len(frame))
            self.write(list(islice(frame, 0, length)))
            frame.rotate(-1)
            time.sleep(delay)
            if repeat > 0:
                shifts -= 1

    @classmethod
    def get_char(cls, char):
        if char in cls.CHAR_MAP:
            pattern = cls.CHAR_MAP[char]
        elif char.lower() in cls.CHAR_MAP:
            pattern = cls.CHAR_MAP[char.lower()]
        else:
            raise RuntimeError('Character mapping for "{}" not found.'.format(char))
        return int(pattern, 2)
