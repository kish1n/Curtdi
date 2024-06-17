import disnake
from disnake.ext import commands, tasks
from bot.utils.twitch import is_streaming
from bot.utils.twitch import authenticate
from config import settings

class TwitchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.streamer_name = 'iltw1'  # Укажите имя стримера
        self.channel_id = settings.CHANNEL_ID_TWITCH  # Укажите ID канала, куда бот будет отправлять сообщения
        self.check_stream_status.start()

    @tasks.loop(minutes=1)
    async def check_stream_status(self):
        print('Checking stream loop')
        if await is_streaming(self.streamer_name):
            channel = self.bot.get_channel(self.channel_id)
            embed = disnake.Embed(
                title=f'{self.streamer_name} is live on Twitch!',
                description=f'Check out the stream: https://www.twitch.tv/{self.streamer_name}',
                color=disnake.Color.purple()
            )

            embed.set_image(url='https://dota2.net/thumb/post/size-og-image/2023/12/101945/MTAxOTQ1c0pFeDlhMzhudg==.jpg')
            await channel.send(embed=embed)
            self.check_stream_status.stop()

    @commands.slash_command(name='checkstream', description='Check if the streamer is live on Twitch')
    async def check_stream(self, interaction: disnake.ApplicationCommandInteraction):
        if await is_streaming(self.streamer_name):
            await interaction.response.send_message(f'{self.streamer_name} is live on Twitch! Check it out: '
                                                    f'https://www.twitch.tv/{self.streamer_name}')
        else:
            await interaction.response.send_message(f'{self.streamer_name} is not live on Twitch.')

    @check_stream_status.before_loop
    async def before_check_stream_status(self):
        await authenticate()
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(TwitchCog(bot))
