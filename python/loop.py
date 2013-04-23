#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
7 segment display main loop.

Usage:
    loop.py [--verbosity=<level>] [--dev=<device>]

Options:
    --dev=<device>       The USB device [default: /dev/ttyUSB0].
    --verbosity=<level>  The log level (1=debug, 2=info, 3=warning, 4=error) [default: 2]

"""
from __future__ import print_function, division, absolute_import

import os
import sys
import logging
from time import sleep
from itertools import tee, cycle

from docopt import docopt
from sevensegment import SevenSegmentDisplay, SevenSegmentController, Segments, Shapes


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


def run_animation(disp, frames, repeat=1, delay=0.1, digits=8):
    """Run an animation on all ``digits`` at the same time with the specified
    ``delay``."""
    for _ in xrange(repeat):
        for frame in frames:
            disp.write([frame]*digits)
            sleep(delay)


def run_shifted_animation(disp, frames, repeat=1, delay=0.1, digits=8):
    """Run an animation on all ``digits`` with the specified ``delay``. On each
    digit, the animation is shifted by 1 frame."""

    # Get multiple independent generators
    generators = tee(cycle(frames), digits)

    # Shift frames
    init = digits
    while init > 0:
        for frame in generators[:-init]:
            frame.next()
        init -= 1

    # Write to display and move each generator to next frame
    iterations = len(frames) * repeat
    while iterations > 0:
        disp.write([generator.next() for generator in generators])
        sleep(delay)
        iterations -= 1


def mainloop(disp, args):
    logging.info('Entered main loop!')

    ctrl = SevenSegmentController(disp)

    while 1:
        ctrl.write_string('8bit bar', 1)
        ctrl.write_string('bier', 1)
        ctrl.write_string('shots', 1)
        ctrl.write_string('bits', 1)
        ctrl.write_string('affen', 0.3)
        ctrl.write_string('titten', 0.3)
        ctrl.write_string('geil!', 1)

        run_animation(disp, SimpleAnimations.circle, 3)
        run_animation(disp, SimpleAnimations.eight, 3)
        run_animation(disp, SimpleAnimations.doublecircle, 6)

        ctrl.write_string('', 0.5)
        ctrl.rotate_string('8bit bar ', repeat=2)
        ctrl.write_string('', 0.5)
        ctrl.rotate_string('Affentittengeil! ', repeat=2)
        ctrl.write_string('', 0.5)

        run_shifted_animation(disp, SimpleAnimations.circle, 3)
        run_shifted_animation(disp, SimpleAnimations.eight, 3)
        run_shifted_animation(disp, SimpleAnimations.doublecircle, 6)


if __name__ == '__main__':

    # Parse arguments
    args = docopt(__doc__, version='v0.0.1')
    dev = args['--dev']

    # Check permissions
    if not os.access(dev, os.W_OK):
        print('Write access to {} not allowed. Run as root?'.format(dev))
        sys.exit(os.EX_NOPERM)

    # Set log level
    try:
        loglevel = int(args['--verbosity']) * 10
    except ValueError:
        print('Invalid verbosity.')
        sys.exit(os.EX_CONFIG)
    logging.basicConfig(level=loglevel)

    # Run main loop
    logging.info('Initializing...')
    disp = SevenSegmentDisplay(device=dev, digits=8)
    try:
        mainloop(disp, args)
    except KeyboardInterrupt:
        print()
        logging.info('Goodbye.')
