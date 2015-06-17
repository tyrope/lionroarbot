#coding: utf8
"""
LRB-Core.py - LionRoarBot Core module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from willie.config import ConfigurationError
from willie.module import commands, OP, require_privilege, event, rule

def setup(bot):
    bot.db.execute('CREATE TABLE IF NOT EXISTS lrb_regulars '+
        '(nick STRING, PRIMARY KEY (nick))')

# Twitch turned off JOIN/PART by default, we have to ASK for it now...
@event('001')
@rule('.*')
def requestJoinsParts(bot, trigger):
    bot.write(["CAP REQ :twitch.tv/membership"])

@require_privilege(OP, 'Only moderators can alter regulars.')
@commands('reg','regular')
def regular(bot, trigger):
    if not trigger.group(3):
        return bot.reply("Do what? (add/del)")
    if not trigger.group(4):
        return bot.reply("To who?")

    cmd = trigger.group(3).lower()
    target = trigger.group(4).lower()

    if cmd == 'add':
        bot.db.execute('INSERT INTO lrb_regulars (nick) VALUES (?)', (target,))
        return bot.reply('%s added to regulars list.' % (target,))
    elif cmd == 'del':
        bot.db.execute('DELETE FROM lrb_regulars WHERE nick=?', (target,))
        return bot.reply('%s removed from regulars list.' % (target,))
    else:
        return bot.reply("Unknown parameter. Valid commands: !reg add, !reg del")

