from twitchAPI.twitch import Twitch
import os
from config import settings

twitch = Twitch(settings.TWITCH_CLIENT_ID, settings.TWITCH_CLIENT_SECRET)
twitch.authenticate_app([])

async def authenticate():
    try:
        await twitch.authenticate_app([])
        print('Twitch authenticated')
    except Exception as e:
        print(f'Error: {e}')

async def is_streaming(user_login):
    # Получаем информацию о стриме пользователя
    streams = twitch.get_streams(user_login=[user_login])
    async for stream in streams:
        if stream:
            return True
    return False
