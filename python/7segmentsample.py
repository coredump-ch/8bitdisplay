#!/usr/bin/python

import time
import serial


ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Wait for serial device to become ready

data = [0x7f, 0x1f, 0x04, 0x07, 0x00, 0x1f, 0x77, 0x05]
padding = 2


def writeToDisplay(list):
    ser.write("".join(chr(i) for i in list))
    ser.flush()


def createString(list):
    if len(list) < 8:
        list.append(0x00)
        for i in range(8 - len(list)):
            list.append(data[i])
    return list


# MAIN Program-Loop

bar_bottom = 0x8
bar_middle = 0x1
bar_top = 64
list = [2, 4, 8, 16, 64, 32]
#for count in range(2):
#    for e in list:
#        output = []
#        for b in range(8):
#            output.append(e)
#        print output
#        writeToDisplay(output)
#        time.sleep(0.05)


circle_sequence = [
    [8, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 64],
    [0, 0, 0, 0, 0, 0, 64, 0],
    [0, 0, 0, 0, 0, 64, 0, 0],
    [0, 0, 0, 0, 64, 0, 0, 0],
    [0, 0, 0, 64, 0, 0, 0, 0],
    [0, 0, 64, 0, 0, 0, 0, 0],
    [0, 64, 0, 0, 0, 0, 0, 0],
    [64, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0],
]

#Printing circle_sequence
#for f in range(10):
#    for frame in circle_sequence:
#        writeToDisplay(frame)
#        time.sleep(0.01)

while 1:
    writeToDisplay(data)
    for idx in range(len(data) + 1):
        newString = createString(data[idx:])
        print newString
        writeToDisplay(newString)
        time.sleep(0.2)

    print "finished"
