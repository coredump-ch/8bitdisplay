"""
Sample for counting button presses on rising edges.
Button inputs are taken from stdin: on -> pressed, anything else -> not pressed
Prints out the current count of button presses after successful increment
"""

import shelve
import sys
import time
import RPi.GPIO as GPIO


class Button(object):
    INPUT_GPIO_PIN = 23

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.INPUT_GPIO_PIN, GPIO.IN)

    def read(self):
        """Reads Button state, do not forget to debounce..."""
        input_vals = []
        for i in xrange(5):
            input_vals.append(GPIO.input(self.INPUT_GPIO_PIN))
            time.sleep(0.01)
        return sum(input_vals) == 5


filename = 'db.dat'
d = shelve.open(filename)
if not 'count' in d:
    d['count'] = 0
button = Button()

while True:
    if button.read():
        # Await falling edge
        while button.read() is True:
            print 'awaiting falling edge'
            pass

        d['count'] = int(d['count']) + 1
        if d['count'] >= 256:
            d['count'] = 0

        d.sync()  # Make sure shelve is synced
        print 'count is %s' % d['count']
