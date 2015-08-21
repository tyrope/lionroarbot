#coding: utf8
"""
LRB-Core.py - LionRoarBot Core module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel.config import ConfigurationError
from sopel.tools import SopelMemory
from sopel.module import commands, OP, require_privilege, event, rule, NOLIMIT

def setup(bot):
    bot.db.execute('CREATE TABLE IF NOT EXISTS lrb_regulars '+
        '(ID INTEGER, nick STRING, channel STRING, PRIMARY KEY (ID))')

    bot.memory['moderators'] = SopelMemory()

@event('001')
@rule('.*')
def requestJoinsParts(bot, trigger):
    # Twitch turned off JOIN/PART by default, we have to ASK for it now...
    bot.write(["CAP REQ :twitch.tv/membership"])

@event('JOIN')
@rule('.*')
def requestModList(bot, trigger):
    if trigger.nick != bot.nick:
        return NOLIMIT
    return bot.say('.mods')

#@rule('.*')
#def getModList(bot, trigger):

@commands('reg','regular')
def regular(bot, trigger):
    if not trigger.admin:
        return bot.reply('Only moderators can alter regulars.')

    if not trigger.group(3):
        return bot.reply("Do what? (add/del)")
    if not trigger.group(4):
        return bot.reply("To who?")

    cmd = trigger.group(3).lower()
    target = trigger.group(4).lower()

    if cmd == 'add':
        bot.db.execute('INSERT INTO lrb_regulars (nick, channel) VALUES (?, ?)', (target,trigger.channel))
        return bot.reply('%s added to regulars list.' % (target,))
    elif cmd == 'del':
        bot.db.execute('DELETE FROM lrb_regulars WHERE nick=? AND channel=?', (target,trigger.channel))
        return bot.reply('%s removed from regulars list.' % (target,))
    else:
        return bot.reply("Unknown parameter. Valid commands: !reg add, !reg del")

