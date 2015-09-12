#coding: utf8
"""
LRB-Caps.py - LionRoarBot ALLCAPS module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from collections import Counter
from sopel.module import rule, NOLIMIT
try:
    from LRB_Core import isReg
except ImportError as e:
    print "Error loading Core module. Regular detection will not function."
    def isReg(bot, chan, nick): return False # placeholder

core_complained = False

@rule('.*')
def caps_detection(bot, trigger):
    """
    Automatically detect allcaps and act on it.
    """
    try:
        if trigger.admin:
            # This person is a moderator.
            return NOLIMIT
    except KeyError as e:
        # This potentially lets new-joiners shout for a little bit.
        # #blametwitch
        return NOLIMIT

    if len(trigger.group(0)) < 10:
        # This message was very short, could be something like "OMG",
        # let's not make a fuss about it.
        return NOLIMIT

    if isReg(bot, trigger.sender, trigger.nick):
        #This person is a regular.
        return NOLIMIT

    counter = Counter(trigger.group(0))
    caps = 0
    lowercase = 0
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        caps += counter[c]
    for c in "abcdefghijklmnopqrstuvwxyz":
        lowercase += counter[c]

    if caps >= lowercase:
        bot.say('.ban '+trigger.nick)
        bot.reply('Oi! I\'m the only one allowed to ROAAAAAAAAAAAAR around here! (Caps purge)')
        bot.say('.unban '+trigger.nick)
    else:
        return NOLIMIT

