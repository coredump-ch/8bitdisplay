# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
from cleverbot import cleverbot

mario = cleverbot.Cleverbot()
pauline = cleverbot.Cleverbot()
initial_question = 'Hello. Do you like the 8 bit bar?'

resp1 = mario.ask(initial_question)
print('Mario: {}'.format(initial_question))
while 1:
    print('Pauline: {}'.format(resp1))
    resp2 = pauline.ask(resp1)
    print('Mario: {}'.format(resp2))
    resp1 = mario.ask(resp2)
