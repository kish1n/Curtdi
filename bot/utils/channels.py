import disnake
from disnake.ext import commands

async def create_voice_channel(guild: disnake.Guild, channel_name: str, user_limit: int, category: disnake.CategoryChannel = None):
    """Создает голосовой канал с ограничением по количеству участников."""
    channel = await guild.create_voice_channel(
        name=channel_name,
        user_limit=user_limit,
        category=category
    )
    return channel

async def delete_empty_voice_channels(guild: disnake.Guild, category_name: str):
    """Удаляет пустые голосовые каналы в указанной категории."""
    category = disnake.utils.get(guild.categories, name=category_name)
    if not category:
        return

    for channel in category.voice_channels:
        if len(channel.members) == 0:
            await channel.delete()