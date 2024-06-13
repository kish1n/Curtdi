import re
import disnake
from disnake.ext import commands

CENSORED_WORDS = ['ananas', 'pineapple', 'ананас']

def _contains_prohibited_word(message_content):
    normalized_content = re.sub(r'[^а-яА-Яa-zA-Z]', '', message_content.lower())
    for word in CENSORED_WORDS:
        if re.search(rf'{re.sub(r"[^а-яА-Яa-zA-Z]", "", word)}', normalized_content):
            return True
    return False

def setup_events(bot):

    @bot.event
    async def on_member_join(member):
        role = disnake.utils.get(member.guild.roles, name='new')
        channel = member.guild.system_channel
        if channel:
            await channel.send(f'Welcome, {member.mention}!')

        embed = disnake.Embed(
            title='Welcome!',
            description=f'Welcome, {member.mention}!',
            color=disnake.Color.green()
        )

        await member.add_roles(role)
        await member.send(embed=embed)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if _contains_prohibited_word(message.content):
            await message.delete()
            await message.channel.send(
                f'{message.author.mention}, ваше сообщение было удалено за использование запрещенного содержания.')
