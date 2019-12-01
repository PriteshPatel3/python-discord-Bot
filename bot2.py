import discord
import random
from discord import TextChannel
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import time
from discord.ext.commands import has_permissions, MissingPermissions

token= "NjUwMTczMDI0MDMyNTIyMjYx.XeM3kw.kM_6DT-ZUwDbytn3O9wXJPFDgUk"
BOT_PREFIX = '.'
bot = commands.Bot(command_prefix=BOT_PREFIX)
bot_name = 'Hackathon bot'
@bot.event
async def on_ready():
    print("Bot is up and ready to go")
"""   
@bot.command(pass_context=True, aliases=['del-text', 'dt'])
@commands.has_permissions(manage_channels=True)
async def delete_channel(ctx, arg1):
    guild = ctx.guild
    exisiting_channel = discord.utils.get(guild.channels, name=arg1)
    if exisiting_channel:
        print(f'Deletomg a channel: {arg1}')
        await ctx.send('Delete channel: {}'.format(arg1))
        #await TextChannel.delete(arg1)
        #await guild.delete_text_channel(arg1)
    else:
        await ctx.send('Channel {} does not exist '.format(arg1))
        """

@bot.command(pass_context=True, aliases=['create-text', 'create-t', 'ct'])
@commands.has_permissions(manage_channels=True)
async def create_channel(ctx, arg1):
    guild = ctx.guild
    exisiting_channel = discord.utils.get(guild.channels, name=arg1)
    if not exisiting_channel:
        print(f'Creating a new channel: {arg1}')
        await ctx.send('Created a channel {}'.format(arg1))
        await guild.create_text_channel(arg1)
    else:
        await ctx.send('Channel name {} already exist '.format(arg1))

@bot.command(pass_context=True, aliases=['create-voice', 'create-v', 'cv'])
@commands.has_permissions(manage_channels=True)
async def create_voice(ctx, arg1):
    guild = ctx.guild
    exisiting_channel = discord.utils.get(guild.channels, name=arg1)
    if not exisiting_channel:
        print(f'Creating a new voice channel: {arg1}')
        await ctx.send('Created a voice channel {}'.format(arg1))
        await guild.create_voice_channel(arg1)
    else:
        await ctx.send('Channel name {} already exist '.format(arg1))

@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected')

    await ctx.send(f'{bot_name} has joined {channel}')

@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):

    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Bot has left {channel}')
        await ctx.send(f'{bot_name} has left {channel}')
    else:
        print('{bot_name} is not in any channel')
        await ctx.send(f'{bot_name} is not in any channel')



@bot.command(pass_context=True, aliases=['p'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Tryinng to delete song file")
        await ctx.send("Error: Music playing")
        return

    await ctx.send("Everything is ready")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f'Renamed file {file}')
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print(f'{name} has finished playing'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    nname = name.rsplit('-',2)
    await ctx.send(f'PLaying {nname[0]}')
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    greeting = [
        'Hi',
        'Hello',
    ]

    if message.content.casefold() == 'hi':
        response = random.choice(greeting)
        await message.channel.send(response)
    await bot.process_commands(message)

@bot.command(pass_context=True, aliases=['s', 'shutdown', 'sd'])
@commands.has_permissions(administrator=True)
async def shutDown(ctx):
    await ctx.send(f'{bot_name} is shutting down...')
    await bot.logout()
bot.run(token)