#coding: utf8
"""
LRB-Quotes.py - LionRoarBot Quote module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from willie.config import ConfigurationError
from willie.module import commands, OP
import random

def setup(bot):
    table_layout = ['id','quote']

    if not bot.db:
        raise ConfigurationError("No database configured.")
    if not bot.db.lrb_quotes:
        # 404 - Table not found.
        bot.db.add_table('lrb_quotes', table_layout, 'id')

    for col in table_layout:
        # Just in case not all columns are present.
        if not bot.db.lrb_quotes.has_columns(col):
            bot.db.lrb_quotes.add_columns([col])

@commands('quote')
def quote(bot, trigger):
    quote_id = random.randint(0, bot.db.lrb_quotes.size()-1)
    quote = bot.db.lrb_quotes.get(str(quote_id), 'quote')
    bot.say(quote)

@commands('addquote')
def addquote(bot, trigger):
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return bot.reply("Only moderators can add quotes.")
    # Save the quote to the database

    quote_id = str(bot.db.lrb_quotes.size())
    bot.db.lrb_quotes.update(quote_id, {'quote': trigger.group(2)})

    if quote_id in bot.db.lrb_quotes:
        bot.say('Quote recorded.')
    else:
        bot.say('Quote not recorded, try again later.')

