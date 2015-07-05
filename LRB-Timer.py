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
from willie.module import interval, commands, NOLIMIT

def setup(bot):
    bot.db.execute('CREATE TABLE IF NOT EXISTS lrb_timers '+
        '(id STRING, message STRING, PRIMARY KEY (id))')

    bot.memory['timer'] = WillieMemory()
    bot.memory['timer']['index'] = 0
    bot.memory['timer']['enabled'] = False
    if not bot.config.has_option('LRB','channel') \
    or not bot.config.has_option('LRB','ctt_default') \
    or not bot.config.has_option('LRB','timers_folder') \
    or not bot.config.has_option('LRB','timers_link'):
        raise ConfigurationError("LRB Timer Module not configured.")

def configure(config):
    """
| [LRB] | example | purpose |
| -------- | ------- | ------- |
| channel | #LionRoarBot | The channel to spam these messages in. |
| ctt_default | kiRU4 | The default click to tweet URL ID. |
| timers_folder | /home/lionroarbot/timerfiles/%s | The location where the bot will store the timers list. |
| timers_link | http://lrb.tyrope.nl/%s | The URL where people can see the timers list. |
"""
    chunk = ''
    if config.option('Configuring LRB Timer module', False):
        config.interactive_add('LRB', 'channel', 'channel', '')
        config.interactive_add('LRB', 'ctt_default', 'ctt-default', '')
        config.interactive_add('LRB', 'timers_folder', 'timers_folder', '')
        config.interactive_add('LRB', 'timers_link', 'timers_link', '')
    return chunk

@interval(3600)
def update_timers(bot):
    timers = list()
    for timer in bot.db.execute('SELECT * FROM lrb_timers'):
        # ALL THE TIMERS!
        timers.append(
            ('[%s] - %s\r\n' % (str(timer[0]), timer[1])).encode('utf-8'))

    # Open the file (empty it)
    listfile = open(bot.config.LRB.timers_folder + bot.nick.lower() + \
        '-timers', 'w')
    # Write all the timers
    listfile.writelines(timers)
    # Close and exit.
    listfile.close()
    return NOLIMIT

@interval(900)
def timed_message(bot):
    """
    Spit out one of the pre-configured messages every 15 minutes.
    """
    if not 'index' in bot.memory['timer']:
        # Because for some reason in setup() it doesn't trigger all the time?
        bot.memory['timer']['index'] = 0

    if not bot.memory['timer']['enabled']:
        # Timed messages are disabled.
        return NOLIMIT

    # Fetch line.
    ret = bot.db.execute('SELECT message FROM lrb_timers WHERE id=?',
        str(bot.memory['timer']['index']))
    msg = ret.fetchone()[0]

    # CTT thing.
    if 'http://ctt.ec/' in msg:
        if 'ctt' not in bot.memory['timer']:
            bot.memory['timer']['ctt'] = bot.config.LRB.ctt_default
        msg = msg % bot.memory['timer']['ctt']

    # Move index up one, or loop.
    bot.memory['timer']['index'] += 1
    count = bot.db.execute('SELECT COUNT(*) FROM lrb_timers').fetchone()[0]
    if bot.memory['timer']['index'] >= int(count):
        bot.memory['timer']['index'] = 0

    # Say!
    bot.msg(bot.config.LRB.channel, msg)

@commands('ctt')
def ctt(bot, trigger):
    if not trigger.admin: return NOLIMIT

    if trigger.group(2):
        bot.memory['timer']['ctt'] = trigger.group(2)
        bot.reply('Updated click to tweet link to http://ctt.ec/%s' %
            trigger.group(2))
    else:
        bot.memory['timer']['ctt'] = bot.config.LRB.ctt_default
        bot.reply('Reset click to tweet link to default.')

@commands('spam')
def timer(bot, trigger):
    if not trigger.admin:
        return bot.reply('No spam unless you\'re a moderator.')
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

@commands('listtimers')
def list_timers(bot, trigger):
    return bot.reply(
        "My pre-programmed spam can be found at %s (Updated hourly)" %
        (bot.config.LRB.timers_link % (bot.nick.lower()+"-timers",),))

