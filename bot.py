import os
from webserver import keep_alive
import asyncio
import discord
from discord.ext import commands


token = os.environ['PTW_bot']

client = commands.Bot(command_prefix='ptw!', intents=discord.Intents.all())


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Файл {filename[:-3]} загружен!')


async def main():
    async with client:
        await load()
        keep_alive()
        await client.start(token)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(''))
    print('бот робит двк')


asyncio.run(main())

# https://discord.com/api/oauth2/authorize?client_id=1113908816061407242&permissions=8&scope=bot
