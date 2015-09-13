#coding: utf8
"""
LRB-Core.py - LionRoarBot Core module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Sopel system.
http://sopel.chat/
"""

from sopel.tools import SopelMemory
from sopel.module import commands, event, rule

def setup(bot):
    bot.db.execute('CREATE TABLE IF NOT EXISTS lrb_regulars '+
        '(ID INTEGER, nick STRING, channel STRING, PRIMARY KEY (ID))')

@event('001')
@rule('.*')
def requestJoinsParts(bot, trigger):
    # Twitch turned off JOIN/PART by default, we have to ASK for it now...
    bot.write(["CAP REQ :twitch.tv/membership"])

@commands('reg','regular')
def regular(bot, trigger):
    if not trigger.group(3):
        return bot.reply("Do what? (add/check/del/list)")
    cmd = trigger.group(3).lower()


    if cmd in ('add', 'del'):
        if not trigger.group(4):
            return bot.reply("To who?")
        else:
            target = trigger.group(4).lower()

    if cmd == 'add': #Adding regulars
        if not trigger.admin:
            bot.reply('Only moderators can alter regulars.')

        if isReg(bot, trigger.sender, target):
            return bot.reply('%s is already a regular here.' % (target,))
        else:
            bot.db.execute('INSERT INTO lrb_regulars (nick, channel) VALUES (?, ?)', (target,trigger.sender))
            return bot.reply('%s added to regulars list.' % (target,))
    elif cmd == 'del': #Removing regulars
        if not trigger.admin:
            bot.reply('Only moderators can alter regulars.')

        if not isReg(bot, trigger.sender, target):
            return bot.reply('%s is not a regular here.' % (target,))
        else:
            bot.db.execute('DELETE FROM lrb_regulars WHERE nick=? AND channel=?', (target,trigger.sender))
            return bot.reply('%s removed from regulars list.' % (target,))
    elif cmd == 'check': #Check if you're a regular.
        if trigger.admin:
            return bot.reply('You\'re a moderator, that outranks regular.')

        if isReg(bot, trigger.sender, trigger.nick):
            return bot.reply('You\'re a regular.')
        else:
            return bot.reply('You are not a regular.')

    elif cmd == 'list': #Listing regulars
        # TODO maybe, owner only?
        q = 'SELECT nick FROM lrb_regulars WHERE channel=?'
        regulars = ''
        for reg in bot.db.execute(q, (trigger.sender,))
            regulars += reg + ', '
        regulars = regulars[:-2] #remove the last ', '
        return bot.reply('Channel regulars: '+regulars)
    else:
        return bot.reply("Unknown parameter. Valid commands: !reg add, !reg del, !reg list")

def isReg(bot, channel, user):
    q = 'SELECT COUNT(*) FROM lrb_regulars WHERE nick=? AND channel=?'
    if bot.db.execute(q, (user, channel)).fetchone()[0] > 0:
        return True
    else:
        return False
