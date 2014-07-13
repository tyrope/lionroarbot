#coding: utf8
"""
LRB-Cmds.py - LionRoarBot Misc. Custom module.
Copyright 2014, Dimitri "Tyrope" Molenaars <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.

These modules are built on top of the Willie system.
http://willie.dftba.net/
"""

from willie.module import commands

@commands('arrow')
def arrow(bot, trigger):
    bot.say("http://img.4plebs.org/boards/tg/image/1374/03/1374030368304.jpg")

@commands('initiative')
def initiative(bot, trigger):
    bot.say("http://31.media.tumblr.com/1dc5316076bfe562f803647a294872ed/tumblr_mk7t4vCTek1rjq9lao1_500.gif")

@commands('mountain')
def ip(bot, trigger):
    bot.say("http://2.bp.blogspot.com/-3E782nyfAXY/UwGAgoYpszI/AAAAAAAAHs0/qAxtatRJ0ho/w555-h495-no/DM+is+sick+of+your+shit.jpg")

@commands('portal')
def mods(bot, trigger):
    bot.say("Tyrope is speedrunning, meaning he's trying to play the game as fast as possible. The Glitchless category means he can't abuse many of the \"faults\" in the coding. Current leader-boards are available here: http://dft.ba/-P1speedrun")

@commands('roulette')
def roulette(bot, trigger):
    bot.say("Put your spelunkbucks on the table and bet on my cause of death! (Stream and chat are included on the page) http://spelunkyroulette.sparklinlabs.com/play/tyrope")

@commands('timer')
def timer(bot, trigger):
    bot.say("The timer at the bottom of the screen during speedruns is LiveSplit. This program is used to track personal best times for specific parts of the game, and ofcourse the overall time. LiveSplit is free to download at http://livesplit.org/")

@commands('words')
def words(bot, trigger):
    bot.say("HOW DO I WORDS?!?!")

