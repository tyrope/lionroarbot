#coding: utf8
"""
LRB-Quotes.py - LionRoarBot Quote module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from willie.config import ConfigurationError
from willie.tools import WillieMemory
from willie.module import commands, OP, NOLIMIT
import random, time

def setup(bot):
    bot.db.execute('CREATE TABLE IF NOT EXISTS lrb_quotes '+
        '(id STRING, quote STRING, PRIMARY KEY (ID))')

    bot.memory['quotes'] = WillieMemory()
    bot.memory['quotes']['lastused'] = 0

@commands('quote')
def quote(bot, trigger):
    if bot.memory['quotes']['lastused'] > int(time.time()) - 60:
        return NOLIMIT
    else:
        bot.memory['quotes']['lastused'] = int(time.time())

    count = bot.db.execute('SELECT COUNT(*) FROM lrb_quotes').fetchone()[0]
    ret = bot.db.execute('SELECT quote FROM lrb_quotes WHERE id=?',
        (str(random.randint(0, count)),))
    msg = ret.fetchone()[0]
    bot.say(msg)

@commands('addquote')
def addquote(bot, trigger):
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return bot.reply("Only moderators can add quotes.")
    # Save the quote to the database

    count = bot.db.execute('SELECT COUNT(*) FROM lrb_quotes').fetchone()[0]
    bot.db.execute('INSERT INTO lrb_quotes (id, quote) VALUES ?, ?',
        (count, trigger.group(2).replace('\'', '\'\'')))

    if bot.db.execute('SELECT quote FROM lrb_quotes WHERE id=?',
        (count,)).fetchone():
        bot.reply('Quote recorded.')
    else:
        bot.reply('Quote not recorded, try again later.')

