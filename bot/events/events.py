import re
import disnake
from disnake.ext import commands
from config import settings
from bot.utils.log import logger

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
        logger.info(f'New member joined: {member.name}')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if _contains_prohibited_word(message.content):
            await message.delete()
            await message.channel.send(
                f'{message.author.mention}, ваше сообщение было удалено за использование запрещенного содержания.')
            logger.info(f'User {message.author} said a prohibited word: {message.content}')

    @bot.event
    async def on_member_join(member):
        role = disnake.utils.get(member.guild.roles, id=1250808114748456980)
        channel = bot.get_channel(settings.CHANNEL_ID_WELCOME)

        embed = disnake.Embed(
            title='Welcome!',
            description=f'Welcome, {member.mention}!',
            color=disnake.Color.green()
        )

        embed.set_image(url='https://i.pinimg.com/originals/0b/2a/62/0b2a624bc3952975a32a7f314c0770b9.gif')

        await member.add_roles(role)
        await channel.send(embed=embed)
        logger.info(f'New member joined: {member.name}')
