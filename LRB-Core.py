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
    table_layout = ['nick']

    if not bot.db:
        raise ConfigurationError("No database configured.")
    if not bot.db.lrb_regulars:
        # 404 - Table not found.
        bot.db.add_table('lrb_regulars', table_layout, 'nick')

    for col in table_layout:
        # Just in case not all columns are present.
        if not bot.db.lrb_regulars.has_columns(col):
            bot.db.lrb_regulars.add_columns([col])

@commands('reg','regular')
def regular(bot, trigger):
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return bot.reply("Only moderators can alter regulars.")

    if not trigger.group(3):
        return bot.reply("Do what?")
    if not trigger.group(4):
        return bot.reply("To who?")

    cmd = trigger.group(3).lower()
    target = trigger.group(4).lower()

    if cmd == 'add':
        bot.db.lrb_regulars.update(target, {})
        return bot.reply('%s added to regulars list.' % (target,))
    elif cmd == 'del':
        bot.db.lrb_regulars.delete(target)
        return bot.reply('%s removed from regulars list.' % (target,))
    else:
        return bot.reply("Unknown parameter. Valid commands: !reg add, !reg del")

