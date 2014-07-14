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
    table_layout = ['id','quote']

    if not bot.db:
        raise ConfigurationError("No database configured.")
    if not bot.db.lrb-quotes:
        # 404 - Table not found.
        bot.db.add_table('lrb-quotes',table_layout , 'id')

    for col in table_layout:
        # Just in case not all columns are present.
        bot.db.lrb-quotes.add_columns([col])

@commands('quote')
def quote(bot, trigger):
    quote = '"This is a test quote" - LionRoarBot, 2014 (Debug)'
    bot.say(quote)

@commands('addquote')
def addquote(bot, trigger):
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return bot.reply("Only moderators can add quotes.")
    # Save the quote to the database
    bot.db.lrb-quotes.update(bot.db.lrb-quotes.size(), {'quote': trigger.group(2)})
    if recorded:
        bot.say('Quote recorded.')
    else:
        bot.say('Quote not recorded.')

