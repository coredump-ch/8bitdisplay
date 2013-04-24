# -*- coding: utf-8 -*-
"""
Makes two chatbots talk to each other.

To make this run correctly, you need to install the
C64UserMono-Style font and the xtermcontrol program.

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import os

from termcolor import colored
from cleverbot import cleverbot


INITIAL_QUESTION = 'Pauline, do you like the 8 bit bar?'
FONT = 'C64UserMono-Style'


print_mario = lambda s: print(colored('Mario: ' + s, 'green'))
print_pauline = lambda s: print(colored('Pauline: ' + s, 'cyan'))


def setup():
    os.system('xtermcontrol --font=' + FONT)
    os.system('clear')


def main():
    mario = cleverbot.Cleverbot()
    pauline = cleverbot.Cleverbot()

    resp1 = mario.ask(INITIAL_QUESTION)
    print_mario(INITIAL_QUESTION)
    while 1:
        print_pauline(resp1)
        resp2 = pauline.ask(resp1)
        print_mario(resp2)
        resp1 = mario.ask(resp2)


if __name__ == '__main__':
    try:
        setup()
        main()
    except KeyboardInterrupt:
        print('\nGoodbye.')
