"""
Sample for counting button presses on rising edges.
Button inputs are taken from stdin: on -> pressed, anything else -> not pressed
Prints out the current count of button presses after successful increment
"""

import shelve
import sys


class Button:
    def __init__(self):
        pass

    def read(self):
        """Reads Button state, do not forget to debounce..."""
        print "Please give input"
        reading = sys.stdin.readline()
        if 'on' in reading:
            return True
        return False


filename = 'db.dat'
d = shelve.open(filename)
if not 'count' in d:
    d['count'] = 0
button = Button()

while True:
    button_input = button.read()
    if button_input is True:
        #Rising Edge
        d['count'] = int(d['count']) + 1
        if d['count'] == 256:
            d['count'] = 0

        while button.read() is True:
            print 'awaiting falling edge'
            pass
        d.sync()
        print 'count is ' + str(d['count'])