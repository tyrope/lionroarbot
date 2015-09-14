#coding: utf8
"""
LRB-Quotes.py - LionRoarBot Quote module.
Copyright 2014-2015, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel.config import ConfigurationError
from sopel.tools import SopelMemory
from sopel.module import commands, NOLIMIT
import random, time

def setup(bot):
    bot.db.execute('CREATE TABLE IF NOT EXISTS lrb_quotes '+
        '(id STRING, quote STRING, PRIMARY KEY (ID))')

    if not bot.memory.contains('quotes'):
        bot.memory['quotes'] = SopelMemory()
    bot.memory['quotes']['lastused'] = 0

@commands('quote')
def quote(bot, trigger):
    if bot.memory['quotes']['lastused'] > int(time.time()) - 60:
        return NOLIMIT

    count = bot.db.execute('SELECT COUNT(*) FROM lrb_quotes').fetchone()[0]
    ID = str(random.randint(0, count))
    ret = bot.db.execute('SELECT quote FROM lrb_quotes LIMIT ?, 1',
        (ID,))
    try:
        msg = ret.fetchone()
        if len(msg[0]) < 1:
            bot.say("Tried to send quote %s, but it's empty." % ID)
        else:
            bot.say(msg[0])
            bot.memory['quotes']['lastused'] = int(time.time())
    except TypeError as e:
        bot.say("Tried to send quote %s, but it doesn't exist." % ID)

@commands('addquote')
def addquote(bot, trigger):
    if not trigger.admin:
        return bot.reply('Only moderators can add quotes')
    # Save the quote to the database
    count = bot.db.execute('SELECT COUNT(*) FROM lrb_quotes').fetchone()[0]
    bot.db.execute('INSERT INTO lrb_quotes (id, quote) VALUES (?, ?)',
        (count, trigger.group(2).replace('\'', '\'\'')))

    if bot.db.execute('SELECT quote FROM lrb_quotes WHERE id=?',
        (count,)).fetchone():
        bot.reply('Quote recorded.')
    else:
        bot.reply('Quote not recorded, try again later.')

