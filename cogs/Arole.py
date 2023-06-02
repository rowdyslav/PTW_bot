import discord
from discord.ext import commands


class Arole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Команда arole работает!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def arole(self, ctx, role: discord.Role):
        if role.position > ctx.author.top_role.position:
            return await ctx.send('**:x: | Эта роль выше твоей!**')
        for mem in ctx.guild.members:
            if not mem.bot:
                await mem.add_roles(role)


async def setup(client):
    await client.add_cog(Arole(client))
