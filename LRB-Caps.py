#coding: utf8
"""
LRB-Caps.py - LionRoarBot ALLCAPS module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from collections import Counter
from willie.module import rule, NOLIMIT, OP

@rule('.*')
def caps_detection(bot, trigger):
    """
    Automatically detect allcaps and act on it.
    """
    try:
        if bot.privileges[trigger.sender][trigger.nick] >= OP:
            return NOLIMIT
    except KeyError as e:
        pass

    if len(trigger.group(0)) < 10:
        return NOLIMIT

    counter = Counter(trigger.group(0))
    c = 0
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        c += counter[char]

    if c*2 >= len(trigger.group(0).replace(' ','')):
        bot.say('.ban '+trigger.nick)
        bot.reply('Oi! I\'m the only one allowed to ROAAAAAAAAAAAAR around here!')
        bot.say('.unban '+trigger.nick)
    else:
        return NOLIMIT

