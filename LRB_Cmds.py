#coding: utf8
"""
LRB-Cmds.py - LionRoarBot Custom commands module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel.module import commands, NOLIMIT, rule, interval
from sopel.config.types import StaticSection, ValidatedAttribute

class CmdsSection(StaticSection):
    cmds_folder = ValidatedAttribute('cmds_folder', str, default='')
    cmds_link = ValidatedAttribute('cmds_link', str, default='')

def configure(config):
    config.define_section('lrb', CmdsSection)
    config.lrb.configure_setting('cmds_folder', "The location where the bot will store the commands list.")
    config.lrb.configure_setting('cmds_link', "The URL where people can see the commands list.")

def setup(bot):
    bot.db.execute('CREATE TABLE IF NOT EXISTS lrb_commands '+
        '(cmd STRING, level STRING, response STRING, PRIMARY KEY (cmd))')

@interval(3600)
def update_cmds(bot):

    cmds = list()
    for cmd in bot.db.execute('SELECT cmd, level, response FROM lrb_commands'):
        # ALL THE COMMANDS!
        cmds.append(('%s - Level: %s - Response: %s\r\n' % (str(cmd[0]), cmd[1], cmd[2].replace('\'\'','\''))).encode('utf-8'))

    # Open the file (empty it)
    listfile = open(bot.config.LRB.cmds_folder + bot.nick.lower() + '-commands', 'w')
    # Write all the commands
    listfile.writelines(cmds)
    # Close and exit.
    listfile.close()
    return NOLIMIT

@rule('.*')
def command(bot, trigger):
    cmd = trigger.group().split(" ")[0].lower()
    ret = bot.db.execute('SELECT level, response FROM lrb_commands WHERE cmd=?',
        (cmd,)).fetchone()
    if not ret:
        # Not actually a command.
        return NOLIMIT
    else:
        # Command found.
        lvl = ret[0]
        reply = ret[1]

        # Can the user actually trigger this command?
        if lvl == 'all':
            # Everybody can use this.
            bot.reply(reply.replace('\'\'','\''))
        elif lvl == 'mod' and trigger.admin:
            # Mods can use this, This user is a mod or channel owner.
            bot.reply(reply.replace('\'\'','\''))
        elif lvl == 'owner' and trigger.sender[1:].lower() == trigger.nick.lower():
            # Only owner can use this, and this is the channel owner.
            bot.reply(reply.replace('\'\'','\''))
        else:
            # Access Denied.
            return NOLIMIT

@commands('addcom')
def addcom(bot, trigger):
    if not trigger.admin:
        return bot.reply('Only moderators can add commands.')
    try:
        if bot.db.execute('SELECT cmd FROM lrb_commands WHERE cmd =?',
            (trigger.group(3).lower(),)).fetchone():
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

    bot.db.execute('INSERT INTO lrb_commands (cmd, level, response) VALUES '+
        '(?,?,?)', (cmd, lvl, reply.replace('\'', '\'\'')))

    return bot.reply("Added command \"%s\", access level \"%s\", response: %s" % (cmd, lvl, reply))

@commands('commands')
def list_commands(bot, trigger):
    return bot.reply("I have a lot of commands... see %s (Updated hourly)" % (bot.config.LRB.cmds_link % (bot.nick.lower()+"-commands",),))

@commands('delcom')
def delcom(bot, trigger):
    if not trigger.admin:
        return bot.reply('Only moderators can delete commands.')
    cmd = trigger.group(3).lower()
    ret = bot.db.execute('SELECT * FROM lrb_commands WHERE cmd=?',
        (cmd,)).fetchone()

    if not ret:
        return bot.reply("That command doesn't exist...")
    else:
        bot.db.execute('DELETE FROM lrb_commands WHERE cmd=?', (cmd,))
        return bot.reply("Command \"%s\" deleted." % (cmd,))

@commands('editcom')
def editcom(bot, trigger):
    if not trigger.admin:
        return bot.reply('Only moderators can edit commands.')
    try:
        cmd = trigger.group(3).lower()
        ret = bot.db.execute('SELECT cmd FROM lrb_commands WHERE cmd=?',
            (cmd,)).fetchone()
        if not ret:
            return bot.reply("That command doesn't exists, try the addcom command")
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

    bot.db.execute('UPDATE lrb_commands SET level=?, response=? WHERE cmd=?',
        (lvl, reply.replace('\'', '\'\''), cmd))
    return bot.reply("Command \"%s\" modified. Level: \"%s\", response: %s" % (cmd, lvl, reply))

