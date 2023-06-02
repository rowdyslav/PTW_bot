import discord
from discord.ext import commands


class Madd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Команда madd работает!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def madd(self, ctx, *, form: str, count: int, voice='',
                   categ='Default Category Name'):
        if categ == 'Default Category Name':
            category = await ctx.guild.create_category_channel(categ)
        else:
            category = discord.utils.get(ctx.guild.categories, name=categ)

        if voice:
            create_channel = ctx.guild.create_voice_channel
        else:
            create_channel = ctx.guild.create_text_channel

        for number in range(1, count + 1):
            await create_channel(
                form.replace('{n}', str(number)), category=category
            )


async def setup(client):
    await client.add_cog(Madd(client))
