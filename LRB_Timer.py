#coding: utf8
"""
LRB-Timer.py - LionRoarBot timed message module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel.tools import SopelMemory
from sopel.module import interval, commands, NOLIMIT
from sopel.config.types import StaticSection, ValidatedAttribute

class TimerSection(StaticSection):
    channel = ValidatedAttribute('channel', str, default='')
    ctt_default = ValidatedAttribute('ctt_default', str, default='')
    timers_folder = ValidatedAttribute('timers_folder', str, default='')
    timers_link = ValidatedAttribute('timers_link', str, default='')

def configure(config):
    config.define_section('lrb', TimerSection)
    config.lrb.configure_setting('channel',
                                 "The channel to spam these messages in.")
    config.lrb.configure_setting('ctt_default',
                                 "The defailt click to tweet URL ID.")
    config.lrb.configure_setting('timers_folder',
                                 "The location where the bot will store the timers list.")
    config.lrb.configure_setting('timers_link',
                                 "The URL where people can see the timers list.")

def setup(bot):
    bot.db.execute('CREATE TABLE IF NOT EXISTS lrb_timers '+
        '(id STRING, message STRING, PRIMARY KEY (id))')

    bot.memory['timer'] = SopelMemory()
    bot.memory['timer']['index'] = 0
    bot.memory['timer']['enabled'] = False

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

    # Click to tweet
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

