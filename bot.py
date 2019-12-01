# bot.py
import os
import discord
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.voice_client import VoiceClient

load_dotenv(find_dotenv())
token = "NjUwMTczMDI0MDMyNTIyMjYx.XeHhmw.I9WJgBbwXg2zIWc7Y0o5AQv1Zu8"
GUILD = "650175743904448512"
client = discord.Client()

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'Bot has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    greeting = [
        'Hi',
        'Hello',
    ]

    if message.content.casefold() == 'hi':
        response = random.choice(greeting)
        await message.channel.send(response)
@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)
@bot.command()
async def test(ctx):
    await ctx.send("Working")
@bot.command(name='create-text')
@commands.has_role('admin')
async def create_text(ctx, arg1):
    channel_name=arg1
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await ctx.send('Created a chanel {}'.format(channel_name))
        await guild.create_text_channel(channel_name)

@bot.command(name='create-voice')
@commands.has_role('admin')
async def create_voice(ctx, arg1):
    channel_name=arg1
    guild = ctx.guild
    
    print(f'Creating a new voice channel: {channel_name}')
    await ctx.send('Created a chanel {}'.format(channel_name))    
    await guild.create_voice_channel(channel_name)

@bot.command(pass_context=True)
async def join(ctx):
    author = ctx.message.author
    channel = author.voice_channel
    await .join_voice_channel(channel)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message': #writes all into error into err.log file 
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise




bot.run(token)