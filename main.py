import os
import disnake
from disnake.ext import commands
from config import settings
from bot.events.events import setup_events
from disnake import ButtonStyle  # Импортируйте ButtonStyle

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=settings.COMMAND_PREFIX, intents=intents, test_guilds=[settings.ID_SERVER])

@bot.event
async def on_ready():
    print('Bot started')


# Загружаем все расширения (cogs) из папки "cogs"
for file in os.listdir("./bot/cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"bot.cogs.{file[:-3]}")

# Инициализация событий
setup_events(bot)

# Запуск бота
bot.run(settings.DISCORD_TOKEN)
