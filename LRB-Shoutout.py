#coding: utf8
"""
LRB-Caps.py - LionRoarBot Shout-Out module.
Copyright 2015, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from collections import Counter
from willie import web
from willie.module import commands, NOLIMIT, OP
import json

def configure(config):
    """
| [LRB] | example | purpose |
| -------- | ------- | ------- |
| shoutmsg | 'Check out %(name)s on %(link)s! They were last playing %(game)s. | Shout-out message format |
"""
    chunk = ''
    if config.option('Configuring LRB Shout-Out module', False):
        config.interactive_add('LRB', 'shoutmsg', 'shoutmsg',
            'Check out %(name)s on %(link)s! They were last playing %(game)s.')
    return chunk

@commands('so')
def shoutout(bot, trigger):
    """
    Share a little bit of twitch love.
    """
    try:
        if bot.privileges[trigger.sender][trigger.nick] < OP:
            return NOLIMIT
    except KeyError as e:
        return bot.reply("I don't know if you're a mod. #BlameTwitch")

    if trigger.group(2):
        query_url = 'https://api.twitch.tv/kraken/channels/'+trigger.group(2)
        answer = web.get(query_url)

        data = json.loads(answer)

        replaceData = {'name': data['display_name'],
            'link': data['url'], 'game': data['game']}
        return bot.say(bot.config.LRB.shoutmsg % replaceData)
    else:
        return NOLIMIT

