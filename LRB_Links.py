#coding: utf8

"""
LRB-Links.py - LionRoarBot Link module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel.tools import SopelMemory, Nick
from sopel.module import commands, rule, NOLIMIT

def setup(bot):
    bot.memory['permitted_users'] = SopelMemory()

@rule('.*(?:\.[A-z]{2,5})+.*') # http://regexr.com/39583
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
    else:
        bot.say('.ban '+trigger.nick)
        bot.reply('Sharing knowledge is cool and all, but ask Tyrope before sending links, ok?')
        bot.say('.unban '+trigger.nick)

@commands('allow', 'permit')
def permit(bot, trigger):
    """
    Permit somebody to link.
    """
    if not trigger.admin:
        return NOLIMIT
    if trigger.group(3):
        if Nick(trigger.group(3)) in bot.memory['permitted_users']:
            bot.reply("%s already had permission." % trigger.group(3))
        else:
            bot.memory['permitted_users'][Nick(trigger.group(3))] =  True
            bot.reply('%s has permission to post a link.' % trigger.group(3))
    else:
        bot.reply("Who do you want me to give permission?")

