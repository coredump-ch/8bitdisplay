# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import
import sys
import time
from itertools import tee, cycle
from sevensegment import SevenSegmentDisplay, Segments, Shapes



d = SevenSegmentDisplay('/dev/ttyUSB0')
frames = (cycle(snakehead),) + tee(cycle(pattern), 7)

# Shift frames
init = 8
while init > 0:
    for frame in frames[:-init]:
        frame.next()
    init -= 1

while 1:
    d.write([frame.next() for frame in frames])
    time.sleep(0.1)


#frames = [
#    doublecircle,
#    circle,
#    eight,
#]
#generators = [itertools.cycle(frame) for frame in frames]
#while 1:
#    d.write([gen.next() for gen in generators])
#    time.sleep(0.1)
