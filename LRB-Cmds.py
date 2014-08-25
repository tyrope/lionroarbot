#coding: utf8
"""
LRB-Cmds.py - LionRoarBot Custom commands module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from willie.config import ConfigurationError
from willie.module import commands, NOLIMIT, rule, OP

def setup(bot):
    table_layout = ['cmd', 'level', 'response']

    if not bot.db:
        raise ConfigurationError("No database configured.")
    if not bot.db.lrb_commands:
        # 404 - Table not found.
        bot.db.add_table('lrb_commands', table_layout, 'cmd')

    for col in table_layout:
        # Just in case not all columns are present.
        if not bot.db.lrb_commands.has_columns(col):
            bot.db.lrb_commands.add_columns([col])

@rule('.*')
def command(bot, trigger):
    cmd = trigger.group().split(" ")[0]
    if not cmd in bot.db.lrb_commands:
        # Not actually a command.
        return NOLIMIT
    else:
        # Command found.
        dbresult = bot.db.lrb_commands.get(cmd, ('level','response'))
        lvl = dbresult[0]
        reply = dbresult[1]

        try:
            isOP = bot.privileges[trigger.sender][trigger.nick] >= OP
        except KeyError as e:
            isOP = False

        # Can the user actually trigger this command?
        if lvl == 'all':
            # Everybody can use this.
            bot.reply(reply)
        elif lvl == 'mod' and isOP:
            # Mods canuse this, This user is a mod, twitch admin or channel owner.
            bot.reply(reply)
        elif lvl == 'owner' and trigger.sender[1:].lower() == trigger.nick.lower():
            # Only owner can use this, and this is the channel owner.
            bot.reply(reply)
        else:
            # Access Denied.
            return NOLIMIT

@commands('addcom')
def addcom(bot, trigger):
    try:
        if bot.privileges[trigger.sender][trigger.nick] < OP:
            return bot.reply("Only moderators can add commands.")
    except KeyError as e:
        return bot.reply("I don't know if you're a mod. #BlameTwitch")

    try:
        if trigger.group(3).lower() in bot.db.lrb_commands:
            return bot.reply("That command already exists, try the editcom command")
        else:
            cmd = trigger.group(3).lower()
    except IndexError as e:
        return bot.reply("Add what command?")

    try:
        if trigger.group(4).lower() not in ('all', 'mod', 'owner'):
            return bot.reply("What access level? (all, mod, owner)")
        else:
            lvl = trigger.group(4).lower()
    except IndexError as e:
        return bot.reply("You forgot access level & response.")

    reply = trigger.group(0)[len(cmd)+len(lvl)+10:] # 10 = !addcom + 3 spaces
    if len(reply) < 1:
        return bot.reply("You forgot the response...")

    bot.db.lrb_commands.update(cmd, {'level': lvl, 'response': reply.replace('\'', '\'\'')})

    return bot.reply("Added command \"%s\", access level \"%s\", response: %s" % (cmd, lvl, reply))

@commands('delcom')
def delcom(bot, trigger):
    try:
        if bot.privileges[trigger.sender][trigger.nick] < OP:
            return bot.reply("Only moderators can remove commands.")
    except KeyError as e:
        return bot.reply("I don't know if you're a mod. #BlameTwitch")

    if trigger.group(3).lower() not in bot.db.lrb_commands:
        return bot.reply("That command doesn't exist...")
    else:
        bot.db.lrb_commands.delete(trigger.group(3).lower())
        return bot.reply("Command \"%s\" deleted." % (trigger.group(3).lower(),))

@commands('editcom')
def editcom(bot, trigger):
    try:
        if bot.privileges[trigger.sender][trigger.nick] < OP:
            return bot.reply("Only moderators can remove commands.")
    except KeyError as e:
        return bot.reply("I don't know if you're a mod. #BlameTwitch")

    try:
        if trigger.group(3).lower() not in bot.db.lrb_commands:
            return bot.reply("That command doesn't exists, try the addcom command")
        else:
            cmd = trigger.group(3).lower()
    except IndexError as e:
        return bot.reply("Edit what command?")

    try:
        if trigger.group(4).lower() not in ('all', 'mod', 'owner'):
            return bot.reply("What access level? (all, mod, owner)")
        else:
            lvl = trigger.group(4).lower()
    except IndexError as e:
        return bot.reply("You forgot access level & response.")

    reply = trigger.group(0)[len(cmd)+len(lvl)+11:] # 11 = !editcom + 3 spaces
    if len(reply) < 1:
        return bot.reply("You forgot the response...")

    bot.db.lrb_commands.update(cmd, {'level': lvl, 'response': reply.replace('\'', '\'\'')})
    return bot.reply("Command \"%s\" modified. Level: \"%s\", response: %s" % (cmd, lvl, reply))

