#coding: utf8

"""
LRB-Links.py - LionRoarBot Link module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel.tools import SopelMemory, Identifier
from sopel.module import commands, rule, NOLIMIT
try:
    from LRB_Core import isReg
except ImportError as e:
    print "Error loading Core module. Regular detection will not function."
    def isReg(bot, chan, nick): return False # placeholder

def setup(bot):
    bot.memory['permitted_users'] = SopelMemory()

@rule('.*(\.[A-z]{2}|com|info|net|org).*') # http://regexr.com/3bp6d
def link_detection(bot, trigger):
    """
    Automatically detect links and act on it.
    """
    try:
        if trigger.admin:
            #Channel ops can link just fine.
            return NOLIMIT
    except KeyError as e:
        pass

    if trigger.nick in bot.memory['permitted_users']:
        bot.memory['permitted_users'].pop(trigger.nick, None)
        return NOLIMIT
    elif isReg(bot, trigger.sender, trigger.nick):
        return NOLIMIT # Regulars can link just fine.
    else:
        bot.say('.ban '+trigger.nick)
        bot.reply('Sharing knowledge is cool and all, but ask the mods before sending links, ok?')
        bot.say('.unban '+trigger.nick)

@commands('allow', 'permit')
def permit(bot, trigger):
    """
    Permit somebody to link.
    """
    if not trigger.admin:
        return NOLIMIT
    if trigger.group(3):
        if Identifier(trigger.group(3)) in bot.memory['permitted_users']:
            bot.reply("%s already had permission." % trigger.group(3))
        else:
            bot.memory['permitted_users'][Identifier(trigger.group(3))] =  True
            bot.reply('%s has permission to post 1 message with links.' % trigger.group(3))
    else:
        bot.reply("Who do you want me to give permission?")

