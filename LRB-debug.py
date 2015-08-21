# coding=utf-8
"""
LRB-debug.py - LRB Debugging Module - Based on Sopel's Debug module.
Copyright 2013, Dimitri "Tyrope" Molenaars, Tyrope.nl
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel.module import commands, example, require_admin

@require_admin
@commands('privs')
@example('.privs', '.privs #channel')
def privileges(bot, trigger):
    """Print the privileges of a specific channel, or the entire array."""
    if trigger.group(2):
        try:
            bot.say(str(bot.privileges[trigger.group(2)]))
        except Exception:
            bot.say("Channel not found.")
    else:
        bot.say(str(bot.privileges))

