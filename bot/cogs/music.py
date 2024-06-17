import disnake
from disnake.ext import commands
# from bot.utils.music import YTDLSource

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_player = None

    @commands.slash_command(name='play', description='Plays audio from a YouTube video')
    async def play(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        # if interaction.user.voice is None:
        #     await interaction.response.send_message('You are not connected to a voice channel.', ephemeral=True)
        #     return
        #
        # voice_channel = interaction.user.voice.channel
        #
        # if interaction.guild.voice_client is None:
        #     await voice_channel.connect()
        # elif interaction.guild.voice_client.channel != voice_channel:
        #     await interaction.guild.voice_client.move_to(voice_channel)
        #
        # player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        # interaction.guild.voice_client.play(player)
        # self.current_player = player
        await interaction.response.send_message(f'Now playing: ')

    # @commands.slash_command(name='stop', description='Stops and disconnects the bot from voice')
    # async def stop(self, interaction: disnake.ApplicationCommandInteraction):
    #     if interaction.guild.voice_client is not None:
    #         await interaction.guild.voice_client.disconnect()
    #         await interaction.response.send_message('Disconnected from voice channel.')
#
async def setup(bot):
    await bot.add_cog(Music(bot))
