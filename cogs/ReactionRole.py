from discord.ext import commands
import json
import os
import discord


def data_from_reaction(X, ctx):
    guild = X.get_guild(ctx.guild_id)
    member = guild.get_member(ctx.user_id)
    emoji = ctx.emoji.name
    return guild, member, emoji


class ReactionRoles(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rroles = {
            1: {
                '🍎': 1230,
                '🍊': 1231
            },
            2: {
                '🍏': 1232
            }
        }

        if os.path.isfile('rroles.json'):
            with open('rroles.json', 'r', encoding='UTF-8') as f:
                self.rroles = json.load(f)
                self.rroles = {int(x): self.rroles[x] for x in self.rroles}
        else:
            with open('rroles.json', 'w', encoding='UTF-8') as f:
                json.dump(self.rroles, f)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Команда rroles работает!')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id in self.rroles and payload.member != self.client.user:
            guild, member, emoji = data_from_reaction(self.client, payload)
            role_id = self.rroles[message_id].get(emoji)

            if role_id is not None:
                role = guild.get_role(role_id)
                await member.add_roles(role)
                print(f'Added role {role.name} to {member.name}')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id in self.rroles:
            guild, member, emoji = data_from_reaction(self.client, payload)
            role_id = self.rroles[message_id].get(emoji)

            if role_id is not None:
                role = guild.get_role(role_id)
                await member.remove_roles(role)
                print(f'Removed role {role.name} from {member.name}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rroles(self, ctx, message_id: int, *roles: str):
        if not roles or len(roles) % 2 != 0:
            await ctx.send('Пожалуйста, предоставьте роли в формате:\
🍒 @Роль1 🥺 @Роль2')
            return False

        try:
            rroles_message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send('Сообщение не найдено! Проверьте ID')
            return False

        new_rroles = {}
        for role in list(zip(roles[::2], roles[1::2])):
            emoji = role[0].strip()
            role_mention = role[1].strip()
            role_id = int(role_mention[3:-1])
            new_rroles[emoji] = role_id

        self.rroles[message_id] = new_rroles

        with open('rroles.json', 'w', encoding='UTF-8') as f:
            json.dump(self.rroles, f)

        for emoji in new_rroles:
            await rroles_message.add_reaction(emoji)

        await ctx.send('Реакционные роли успешно добавлены.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delrroles(self, ctx, message_id: int):
        self.rroles.pop(message_id, None)
        with open('rroles.json', 'w', encoding='UTF-8') as f:
            json.dump(self.rroles, f)
        try:
            await ctx.fetch_message(message_id).clear_reactions()
            await ctx.send(f'Rroles на {message_id} успешны удалены!')
        except discord.NotFound:
            return False


async def setup(client):
    await client.add_cog(ReactionRoles(client))
