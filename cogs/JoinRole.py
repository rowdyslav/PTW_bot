import discord
from discord.ext import commands
import json


class JoinRole(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('join_role.json') as f:
            data = json.load(f)
            self.join_role_id = data.get('join_role_id', 0)

    @commands.Cog.listener()
    async def on_ready(self):
        print('JoinRole работает!')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if self.join_role_id:
            role = member.guild.get_role(self.join_role_id)
            await member.add_roles(role)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def join(self, ctx, role: discord.Role):
        self.join_role_id = role.id
        with open('join_role.json', 'w') as f:
            json.dump({'join_role_id': self.join_role_id}, f)
        await ctx.send(f'Join role set to {role.name}')


async def setup(client):
    await client.add_cog(JoinRole(client))
