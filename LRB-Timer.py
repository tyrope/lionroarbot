#coding: utf8
"""
LRB-Timer.py - LionRoarBot timed message module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from willie.config import ConfigurationError
from willie.tools import WillieMemory
from willie.module import interval, commands, NOLIMIT, OP

def setup(bot):
    table_layout = ['id', 'message']

    if not bot.db:
        raise ConfigurationError("No database configured.")
    if not bot.db.lrb_timers:
        #404 - Table not found
        bot.db.add_table('lrb_timers', table_layout, 'id')

    for col in table_layout:
        # Just in case not all columns are present.
        if not bot.db.lrb_timers.has_columns(col):
            bot.db.lrb_timers.add_columns([col])

    bot.memory['timer'] = WillieMemory()
    bot.memory['timer']['index'] = 0
    bot.memory['timer']['enabled'] = False
    if not bot.config.has_option('LRB','channel') or not bot.config.has_option('LRB','ctt_default'):
        raise ConfigurationError("LRB Timer Module not configured.")

def configure(config):
    """
| [LRB] | example | purpose |
| -------- | ------- | ------- |
| channel | #LionRoarBot | The channel to spam these messages in. |
| ctt_default | kiRU4 | The default click to tweet URL ID. |
"""
    chunk = ''
    if config.option('Configuring LRB Timer module', False):
        config.interactive_add('LRB', 'channel', 'channel', '')
        config.interactive_add('LRB', 'ctt_default', 'ctt-default', '')
    return chunk


@interval(900)
def timed_message(bot):
    """
    Spit out one of the pre-configured messages every 15 minutes.
    """
    if not bot.memory['timer']['enabled']:
        # Timed messages are disabled.
        return NOLIMIT

    # Fetch line.
    msg = bot.db.lrb_timers.get([bot.memory['timer']['index'], 'message')

    # CTT thing.
    if 'http://ctt.ec/' in msg:
        if 'ctt' not in bot.memory['timer']:
            bot.memory['timer']['ctt'] = bot.config.LRB.ctt_default
        msg = msg % bot.memory['timer']['ctt']

    # Move index up one, or loop.
    bot.memory['timer']['index'] += 1
    if bot.memory['timer']['index'] >= bot.db.lrb_timers.size()-1:
        bot.memory['timer']['index'] = 0

    # Say!
    bot.msg(bot.config.LRB.channel, msg)

@commands('ctt')
def ctt(bot, trigger):
    try:
        if bot.privileges[trigger.sender][trigger.nick] < OP:
            return NOLIMIT
    except KeyError as e:
        pass

    if trigger.group(2):
        bot.memory['timer']['ctt'] = trigger.group(2)
        bot.reply('Updated click to tweet link to http://ctt.ec/%s' % trigger.group(2))
    else:
        bot.memory['timer']['ctt'] = bot.config.LRB.ctt_default
        bot.reply('Reset click to tweet link to default.')

@commands('spam')
def timer(bot, trigger):
    try:
        if bot.privileges[trigger.sender][trigger.nick] < OP:
            return NOLIMIT
    except KeyError as e:
        pass

    if not trigger.group(3):
        return NOLIMIT

    arg = trigger.group(3).lower()

    if arg in ('on', 'enable', 'true'):
        bot.memory['timer']['enabled'] = True
        bot.say("Timed messages enabled.")
    elif arg in ('off', 'disable', 'false'):
        bot.memory['timer']['enabled'] = False
        bot.say("Timed messages disabled.")
    else:
        return NOLIMIT

