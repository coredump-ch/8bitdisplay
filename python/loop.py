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
import time
import signal
import logging

from docopt import docopt
from sevensegment import SevenSegmentDisplay, SevenSegmentController, Segments


PIDFILE = '7segment.pid'


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

        ctrl.run_animation(SimpleAnimations.circle, repeat=3)
        ctrl.run_animation(SimpleAnimations.eight, repeat=3)
        ctrl.run_animation(SimpleAnimations.doublecircle, repeat=6)

        ctrl.write_string('', 0.5)
        ctrl.scroll_string('8bit bar ', repeat=2)
        ctrl.write_string('', 0.5)
        ctrl.scroll_string('Affentittengeil! ', repeat=2)
        ctrl.write_string('', 0.5)

        ctrl.run_shifted_animation(SimpleAnimations.circle, repeat=3)
        ctrl.run_shifted_animation(SimpleAnimations.eight, repeat=3)
        ctrl.run_shifted_animation(SimpleAnimations.doublecircle, repeat=6)


def get_counter(disp):
    global count  # TODO ugly hack, remove
    count = 0
    def count_up(signum, frame):
        global count
        count += 1
        disp.write_string(str(count))
        time.sleep(1)
    return count_up


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

    # Initialize display
    logging.info('Initializing...')
    disp = SevenSegmentDisplay(device=dev, digits=8)

    # Write PID file
    pid = str(os.getpid())
    with open(PIDFILE, 'w') as f:
        f.write(pid)

    # Register signal handlers
    signal.signal(signal.SIGUSR1, get_counter(disp))

    # Run main loop
    try:
        mainloop(disp, args)
    except KeyboardInterrupt:
        print()
        logging.info('Goodbye.')
    finally:
        try:
            os.remove(PIDFILE)
        except OSError:
            pass
