import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import time

token= "NjUwMTczMDI0MDMyNTIyMjYx.XeHhmw.I9WJgBbwXg2zIWc7Y0o5AQv1Zu8"
BOT_PREFIX = '.'
bot = commands.Bot(command_prefix=BOT_PREFIX)
bot_name = 'Hackathon bot'
@bot.event
async def on_ready():
    print("Bot is up and ready to go")
    

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


@bot.command(pass_context=True, aliases=['s', 'shutdown', 'sd'])
async def shutDown(ctx):
    ctx.send(f'{bot_name} is shutting down...')
    await bot.logout()
bot.run(token)