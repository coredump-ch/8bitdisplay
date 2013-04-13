# -*- coding: utf-8 -*-
"""
7 segment display main loop.

Usage:
    loop.py [--dev=<device>]

Options:
    --dev=<device>  The USB device [default: /dev/ttyUSB0].

"""
from __future__ import print_function, division, absolute_import
import sys
from docopt import docopt
from sevensegment import SevenSegmentDisplay, Segments, Shapes


class SimpleAnimations(object):
    """Animations using a single digit."""
    circle = [
        Segments.N,
        Segments.NE,
        Segments.SE,
        Segments.S,
        Segments.SW,
        Segments.NW,
    ]
    eight = [
        Segments.MID,
        Segments.NW,
        Segments.N,
        Segments.NE,
        Segments.MID,
        Segments.SW,
        Segments.S,
        Segments.SE,
    ]
    doublecircle = [
        Segments.N | Segments.S,
        Segments.NE | Segments.SW,
        Segments.SE | Segments.NW,
    ]


if __name__ == '__main__':

    args = docopt(__doc__, version='v0.0.1')

    disp = SevenSegmentDisplay(device=args['--dev'], digits=8)
    disp.rotate_string('8bit bar ')
