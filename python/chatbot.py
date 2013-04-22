# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
from cleverbot import cleverbot

jonas = cleverbot.Cleverbot()
chrigi = cleverbot.Cleverbot()
initial_question = 'Hello. Do you like the 8 bit bar?'

resp1 = jonas.ask(initial_question)
print('Jonas: {}'.format(initial_question))
while 1:
    print('Chrigi: {}'.format(resp1))
    resp2 = chrigi.ask(resp1)
    print('Jonas: {}'.format(resp2))
    resp1 = jonas.ask(resp2)
