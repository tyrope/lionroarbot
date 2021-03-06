#coding: utf8
"""
LRB-Caps.py - LionRoarBot Shout-Out module.
Copyright 2015, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from collections import Counter
from sopel import web
from sopel.module import commands, NOLIMIT, OP,require_privilege
import json

def configure(config):
    """
| [LRB] | example | purpose |
| -------- | ------- | ------- |
| shoutmsg | 'Check out %(name)s on %(link)s! They were last playing %(game)s. | Shout-out message format |
| api_key | 0123456789abcdefghijklmnopqrstu | Twitch API Client-ID.
"""
    chunk = ''
    if config.option('Configuring LRB Shout-Out module', False):
        config.interactive_add('LRB', 'shoutmsg', 'shoutmsg',
            'Check out %(name)s on %(link)s! They were last playing %(game)s.')
        config.interactive_add('LRB', 'api_key', 'api_key',
            '0123456789abcdefghijklmnopqrstu')
    return chunk

@commands('so')
def shoutout(bot, trigger):
    """
    Share a little bit of twitch love.
    """
    if not trigger.admin:
        return bot.reply('I only let mods do shoutouts.')
    if trigger.group(2):
        try:
            query_url = 'https://api.twitch.tv/kraken/channels/{0}?api_version=4&client_id={1}'
            answer = web.get(query_url.format(trigger.group(2),
                                              bot.config.LRB.api_key))
        except:
            return bot.reply("Couldn't contact the Twitch API servers. :( #BlameTwitch")
        try:
            data = json.loads(answer)
        except:
            return bot.reply("The Twitch API returned an invalid object. :( #BlameTwitch")

        try:
            replaceData = {'name': data['display_name'],
                'link': data['url'], 'game': data['game']}
            return bot.say(bot.config.LRB.shoutmsg % replaceData)
        except:
            return bot.reply("The Twitch API be derp. :( #BlameTwitch")
    else:
        return NOLIMIT

