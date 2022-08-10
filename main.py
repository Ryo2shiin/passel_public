from random import randrange

# TODO if using Github diff deployment on HeroKu uncomment the next line
import os
import discord
from discord.ext import commands

# Author: hyppytyynytyydytys#1010
# Created: 26 MAY 2020
# Last updated: 17 JULY 2022
# About: This is a version of Passel Bot that should ONLY be used as a private server bot.
#        Follow the instructions here on how to set up with heroku:
#
#        Passel Bot is a solution to the number of limited number of pins in a discord server.
#        It manages pins in 2 modes, Mode 1 and Mode 2. 
#
#        More information can be found on https://passelbot.wixsite.com/home
#        Passel Support Server: https://discord.gg/wmSsKCX
#
#        Mode 1: In mode 1, the most recent pinned message gets sent to a pins archive
#        channel of your choice. This means that the most recent pin wont be viewable in
#        the pins tab, but will be visible in the pins archive channel that you chose during setup
#
#        Mode 2: In mode 2, the oldest pinned message gets sent to a pins archive channel of
#        your choice. This means that the most recent pin will be viewable in the pins tab, and
#        the oldest pin will be unpinned and put into the pins archive channel
#
#        Furthermore: the p.sendall feature described later in the code allows the user to set
#        Passel so that all pinned messages get sent to the pins archive channel.

# TODO change command here if you want to use another command, replace p. with anything you want inside the single ('') quotes
client = commands.Bot(command_prefix='p.',
                      status='Online', case_insensitive=True)
client.remove_command("help")

# TODO change mode to 1 or 2 here
mode = 1

# TODO 
# sendall is set to 0 by default, change to 1 if you want
# the bot to send all pinned messages to the pins channel
sendall = 0

# TODO 
# replace the 0 with the pins channel ID for your sever
pins_channel = 924825971708801054

# TODO
# add any black listed channel IDs as a list separated by a comma (,)
# a good idea is to add admin channels to this
blacklisted_channels = [806176440265343056,738163047071219855,738163011746922536,738172138518872197,738510479101657218,738245909627797535,774793645143490570,738398695552450681,739870690462793758,738398796559417414,738411431615135788,738412016447782993,741538006095233108,866852232351842334,785778488338153472,923992915414503506,813808454456049695,813821115574517800,813919331515760660,813918583612244009,813821265965088769,813823816790048798,738213864587657307,818315457702264882,818227816017297458,738176632225005648,798798785860861992,738176544459194420,970329659197784134,810893243264008212,738176506513064067,794937967386820619,738176789272068106,826634172016623646,771015380583579659,811063857329995836,821044475358216226,831870045315268628,864877485711818802,831870045315268628,864877485711818802,822658003257917440,986091638432596030,986099711570243634,986103075230072863,986103856930889798,986455438159659029,986327989665005568,987490497918537738,822084483104505866,832228861633626143,822659203045916682,865318239479267340,865318266938720276,818326158885519421,818326158885519421,738177458695569478,817122815043567666,997734844043894805,738177511514701925,741027137737195520,738177808202989628,742394724069146645,801491410758139965,871919627788230706,853273689813811202]

# discord embed colors
EMBED_COLORS = [
    discord.Colour.magenta(),
    discord.Colour.blurple(),
    discord.Colour.dark_teal(),
    discord.Colour.blue(),
    discord.Colour.dark_blue(),
    discord.Colour.dark_gold(),
    discord.Colour.dark_green(),
    discord.Colour.dark_grey(),
    discord.Colour.dark_magenta(),
    discord.Colour.dark_orange(),
    discord.Colour.dark_purple(),
    discord.Colour.dark_red(),
    discord.Colour.darker_grey(),
    discord.Colour.gold(),
    discord.Colour.green(),
    discord.Colour.greyple(),
    discord.Colour.orange(),
    discord.Colour.purple(),
    discord.Colour.magenta(),
]

# When the bot is ready following sets the status of the bot
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# Command to check what the settings of the bot
@client.command(name='settings', pass_context=True)
async def settings(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        return

    await ctx.send("The mode you have setup is: " + str(mode))
    await ctx.send("Sendall is toggled to: " + str(sendall))
    await ctx.send("The pins channel for this server is: " + ctx.channel.guild.get_channel(pins_channel).mention)
    await ctx.send("Black listed channels are: ")
    for c in blacklisted_channels:
        try:
            await ctx.send(ctx.channel.guild.get_channel(c).mention)
        except:
            await ctx.send("Error: Check black listed channels")
            return
    await ctx.send("done")


@client.command(name='pins', pass_context=True)
async def pins(ctx):
    numPins = await ctx.message.channel.pins()
    await ctx.send(ctx.message.channel.mention + " has " + str(len(numPins)) + " pins.")

# The method that takes care of pin updates in a server
@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    global data
    try:
        randomColor = randrange(len(EMBED_COLORS))
        numPins = await channel.pins()

        # checks to see if message is in the blacklist
        # message is only sent if there is a blacklisted server with 50 messages pinned, informs them
        # that passel is in the server and they can un-blacklist the channel to have passel work
        if str(channel.id) in blacklisted_channels:
            return

        isChannelThere = False
        # checks to see if pins channel exists in the server
        channnelList = channel.guild.channels
        for channel in channnelList:
            if int(pins_channel) == int(channel.id):
                isChannelThere = True

        # checks to see if pins channel exists or has been deleted
        if not isChannelThere:
            await channel.send("Check to see if the pins archive channel during setup has been deleted")
            return

        # only happens if send all is toggled on
        if len(numPins) < 49 and sendall == 1:
            last_pinned = numPins[0]
            pinEmbed = discord.Embed(
                description="\"" + last_pinned.content + "\"",
                colour=EMBED_COLORS[randomColor]
            )
            # checks to see if pinned message has attachments
            attachments = last_pinned.attachments
            if len(attachments) >= 1:
                pinEmbed.set_image(url=attachments[0].url)
            pinEmbed.add_field(
                name="Jump", value=last_pinned.jump_url, inline=False)
            pinEmbed.set_footer(
                text="sent in: " + last_pinned.channel.name + " - at: " + str(last_pinned.created_at))
            pinEmbed.set_author(name='Sent by ' + last_pinned.author.name)
            await channel.guild.get_channel(int(pins_channel)).send(embed=pinEmbed)
            
            # remove this message if you do not want the bot to send a message when you pin a message
            await last_pinned.channel.send(
                "See pinned message in " + channel.guild.get_channel(int(pins_channel)).mention)
            return

        # if guild mode is one does the process following mode 1
        if mode == 1:
            last_pinned = numPins[len(numPins) - 1]
            # sends extra messages
            if len(numPins) == 50:
                last_pinned = numPins[0]
                pinEmbed = discord.Embed(
                    # title="Sent by " + last_pinned.author.name,
                    description="\"" + last_pinned.content + "\"",
                    colour=EMBED_COLORS[randomColor]
                )
                # checks to see if pinned message has attachments
                attachments = last_pinned.attachments
                if len(attachments) >= 1:
                    pinEmbed.set_image(url=attachments[0].url)
                pinEmbed.add_field(
                    name="Jump", value=last_pinned.jump_url, inline=False)
                pinEmbed.set_footer(
                    text="sent in: " + last_pinned.channel.name + " - at: " + str(last_pinned.created_at))
                pinEmbed.set_author(name='Sent by ' + last_pinned.author.name)
                await channel.guild.get_channel(int(pins_channel)).send(embed=pinEmbed)

                # remove this message if you do not want the bot to send a message when you pin a message
                await last_pinned.channel.send(
                    "See pinned message in " + channel.guild.get_channel(int(pins_channel)).mention)
                await last_pinned.unpin()

        # if guild mode is two follows the process for mode 2
        if mode == 2:
            last_pinned = numPins[0]
            if len(numPins) == 50:
                last_pinned = numPins[len(numPins) - 1]
                pinEmbed = discord.Embed(
                    # title="Sent by " + last_pinned.author.name,
                    description="\"" + last_pinned.content + "\"",
                    colour=EMBED_COLORS[randomColor]
                )
                # checks to see if pinned message has attachments
                attachments = last_pinned.attachments
                if len(attachments) >= 1:
                    pinEmbed.set_image(url=attachments[0].url)
                pinEmbed.add_field(
                    name="Jump", value=last_pinned.jump_url, inline=False)
                pinEmbed.set_footer(
                    text="sent in: " + last_pinned.channel.name + " - at: " + str(last_pinned.created_at))
                pinEmbed.set_author(name='Sent by ' + last_pinned.author.name)
                await last_pinned.guild.get_channel(int(pins_channel)).send(embed=pinEmbed)

                # remove this message if you do not want the bot to send a message when you pin a message
                await last_pinned.channel.send(
                    "See oldest pinned message in " + channel.guild.get_channel(int(pins_channel)).mention)
                await last_pinned.unpin()
    except:
        print("unpinned a message, not useful for bot so does nothing")


# TODO Replace TOKEN with the token from discord developer portal 
# client.run('TOKEN')

# TODO If using GitHub diff deployment on HeroKu comment out the above line with '#' and remove '#' from the line below to uncomment it. 
client.run(os.environ.get('TOKEN'))
