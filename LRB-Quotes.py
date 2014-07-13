#coding: utf8
"""
LRB-Quotes.py - LionRoarBot Quote module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from willie.config import ConfigurationError
from willie.module import commands

def setup(bot):
    if not bot.db:
        raise ConfigurationError("No database configured.")
    if not bot.db.lrb-quotes:
        # 404 - Table not found.
        bot.db.add_table('lrb-quotes',['id','quote'], 'id')

@commands('quote')
def quote(bot, trigger):
    bot.say('"This is a test quote" - LionRoarBot, 2014 (Debug)"')

@commands('addquote')
def addquote(bot, trigger):
    # Save the quote to the database
    recorded = False

    if recorded:
        bot.say('Quote recorded.')
    else:
        bot.say('Quote not recorded.')

