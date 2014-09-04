#coding: utf8
"""
LRB-Cmds.py - LionRoarBot Custom commands module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from willie.config import ConfigurationError
from willie.module import commands, NOLIMIT, rule, OP, interval

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

    if not bot.config.has_option('LRB','cmds_folder') or not bot.config.has_option('LRB','cmds_link'):
        raise ConfigurationError("LRB Cmds not configured.")

def configure(config):
    """
| [LRB] | example | purpose |
| -------- | ------- | ------- |
| cmds_folder | /home/lionroarbot/cmdfiles/%s | The location where the bot will store the commands list. |
| cmds_link | http://lrb.tyrope.nl/%s | The URL where people can see the commands list. |
"""
    chunk = ''
    if config.option('Configuring LRB Commands module', False):
        config.interactive_add('LRB', 'cmds_folder', 'cmds_folder', '')
        config.interactive_add('LRB', 'cmds_link', 'cmds_link', '')
    return chunk

@interval(3600)
def update_cmds(bot):

    cmds = list()
    for cmd in bot.db.lrb_commands.keys():
        # ALL THE COMMANDS!
        result = bot.db.lrb_commands.get(cmd[0], ('level','response'))
        cmds.append(('%s - Level: %s - Response: %s\r\n' % (str(cmd[0]), result[0], result[1])).encode('utf-8'))

    # Open the file (empty it)
    listfile = open(bot.config.LRB.cmds_folder + bot.nick.lower(), 'w')
    # Write all the commands
    listfile.writelines(cmds)
    # Close and exit.
    listfile.close()
    return NOLIMIT

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

@commands('commands')
def list_commands(bot, trigger):
    return bot.reply("I have a lot of commands... see %s (Updated hourly)" % (bot.config.LRB.cmds_link % (bot.nick.lower(),),))

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

