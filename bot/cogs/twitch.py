import disnake
from disnake.ext import commands, tasks
from bot.utils.twitch import is_streaming
from bot.utils.twitch import authenticate

class TwitchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.streamer_name = 'Ghostik'  # Укажите имя стримера
        self.channel_id = 1251174386828841172  # Укажите ID канала, куда бот будет отправлять сообщения
        self.check_stream_status.start()

    @tasks.loop(minutes=1)
    async def check_stream_status(self):
        print('Checking stream loop')
        if await is_streaming(self.streamer_name):
            channel = self.bot.get_channel(self.channel_id)
            embed = disnake.Embed(
                title='Ghostik is live on Twitch!',
                description='Check out the stream: https://www.twitch.tv/ghostik',
                color=disnake.Color.purple()
            )

            embed.set_image(url='https://static-cdn.jtvnw.net/'
                                'jtv_user_pictures/a1a3f2b2-22a6-4c99-b211-96a28edd1304-profile_image-300x300.png')
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
