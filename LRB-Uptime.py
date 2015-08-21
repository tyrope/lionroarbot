#coding: utf8
"""
LRB-Uptime.py - LionRoarBot Stream uptime module.
Copyright 2015, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel import web
from sopel.module import commands, NOLIMIT
import json
import datetime

@commands('uptime')
def uptime(bot, trigger):
    """
    Report the stream uptime.
    """
    try:
        query_url = 'https://api.twitch.tv/kraken/streams/'+trigger.sender[1:]
        answer = web.get(query_url)
    except:
        return bot.reply("The Twitch API be derp. :( #BlameTwitch")

    try:
        data = json.loads(answer)
    except:
        return bot.reply("The Twitch API returned an invalid object. :( #BlameTwitch")

    startTime = data['stream']['created_at']

    f = '%Y-%m-%dT%H:%M:%SZ'

    tStart = datetime.datetime.strptime(startTime, f)
    now = datetime.datetime.utcnow()
    uptime = (now - tStart).seconds

    h, r = divmod(uptime, 3600)
    m, s = divmod(r, 60)

    if h > 0:
        return bot.reply('Stream has been online for %s:%s:%s' % (h,m,s))
    else:
        return bot.reply('Stream has been online for %s:%s' % (m,s))

