import discord
from discord.ext import commands


class Mclear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Команда mclear работает!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mclear(self, ctx, categ_id: int, message=''):
        categ = discord.utils.get(ctx.guild.categories, id=categ_id)
        for channel in categ.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.purge()
                if message:
                    try:
                        with open(
                            'mclear_message.txt', 'r', encoding='utf-8'
                        ) as f:
                            mclear_message = f.read()
                    except FileNotFoundError:
                        mclear_message = "Ого! Это похоже на еще не \
настроенное сообщение от команды mclear!"
                    await channel.send(mclear_message)


def setup(client):
    client.add_cog(Mclear(client))
