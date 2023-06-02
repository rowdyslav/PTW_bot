# import discord
from discord.ext import commands


class Madd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Команда madd работает!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def madd(self, ctx, form: str, count: int, voice=0):
        for number in range(1, count + 1):
            if voice:
                ctx.message.guild.create_voice_channel(
                    form.replace('{n}', number)
                )
            else:
                ctx.message.guild.create_text_channel(
                    form.replace('{n}', number)
                )


async def setup(client):
    await client.add_cog(Madd(client))
