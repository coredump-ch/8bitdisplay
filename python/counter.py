import shelve
import sys


class Button:
    def __init__(self):
        pass

    def read(self):
        print "Please give input"
        reading = sys.stdin.readline()
        if "on" in reading:
            print "returning true"
            return True
        print "returning false"
        return False


counter = 0
filename = 'db.dat'
d = shelve.open(filename)
if not 'count' in d:
    d['count'] = 0
button = Button()

while True:
    print "reading button"
    button_input = button.read()
    if button_input is True:
        #Rising Edge
        print "increment count"
        d['count'] = int(d['count']) + 1
        if d['count'] == 256:
            d['count'] = 0

        while button.read() is True:
            print "awaiting falling edge"
            pass
        d.sync()
        print "count is " + str(d['count'])