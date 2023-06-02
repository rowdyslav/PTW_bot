import discord
from discord.ext import commands


class Mdelete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Команда mdelete работает!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mdelete(self, ctx, *channels: discord.TextChannel):
        for channel in channels:
            await channel.delete()


async def setup(client):
    await client.add_cog(Mdelete(client))
