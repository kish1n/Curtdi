import os

import disnake
from disnake.ext import commands
from config import settings
from bot.events.events import setup_events

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=settings.COMMAND_PREFIX, intents=intents, test_guilds=[settings.ID_SERVER])

@bot.event
async def on_ready():
    print('Bot started')

# При готовности бота, загружает расширения из папки "cogs"
for file in os.listdir("./bot/cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"bot.cogs.{file[:-3]}")

setup_events(bot)

bot.run(settings.DISCORD_TOKEN)