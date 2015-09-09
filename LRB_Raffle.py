#coding: utf8
"""
LRB-Raffle.py - LionRoarBot Raffle module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel.tools import SopelMemory
from sopel.module import commands, NOLIMIT
import random, time

def setup(bot):
    bot.memory['raffle'] = SopelMemory()
    bot.memory['raffle']['open'] = False
    bot.memory['raffle']['people'] = list()
    bot.memory['raffle']['lastcall'] = 0

@commands('openraffle')
def open_raffle(bot, trigger):
    if trigger.nick.lower() != trigger.sender.lower()[1:]:
        return NOLIMIT # Owner only.

    bot.memory['raffle']['people'] = list()
    bot.memory['raffle']['open'] = True
    return bot.say("RAFFLE ACTIVATED! Type !roar to enter.")

@commands('roar')
def enter_raffle(bot, trigger):
    if not bot.memory['raffle']['open']:
        return bot.reply("There is no raffle open.")

    if trigger.nick in bot.memory['raffle']['people']:
        return NOLIMIT # You're already in the raffle.
    else:
        bot.memory['raffle']['people'].append(trigger.nick)
        if bot.memory['raffle']['lastcall'] > int(time.time()) - 15:
            return NOLIMIT
        else:
            bot.memory['raffle']['lastcall'] = int(time.time())
            return bot.reply("Added 1 or more people to the raffle. (%s total)" % len(bot.memory['raffle']['people']))

@commands('winner')
def win_raffle(bot, trigger):
    if trigger.nick.lower() != trigger.sender.lower()[1:]:
        return NOLIMIT # Owner only.

    bot.memory['raffle']['open'] = False
    random.shuffle(bot.memory['raffle']['people'])
    try:
        winner = bot.memory['raffle']['people'].pop()
        return bot.say("AND THE WINNER IS...  %s! CONGRATULATIONS! Type in chat so we know you're here." % str(winner))
    except IndexError:
        return bot.reply("We appear to have a problem... nobody entered.")

