#coding: utf8
"""
LRB-Core.py - LionRoarBot Core module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from willie.config import ConfigurationError
from willie.module import commands, OP

def setup(bot):
    bot.db.execute('CREATE TABLE IF NOT EXISTS lrb_regulars '+
        '(nick STRING, PRIMARY KEY (nick))')

@commands('reg','regular')
def regular(bot, trigger):
    try:
        if bot.privileges[trigger.sender][trigger.nick] < OP:
            return bot.reply("Only moderators can alter regulars.")
    except KeyError as e:
        return bot.reply("I don't know if you're a mod. #BlameTwitch")

    if not trigger.group(3):
        return bot.reply("Do what?")
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

