import disnake
from disnake.ext import commands
from bot.utils.music import YTDLSource

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_player = None
        self.queue = []
        self.is_paused = False

    async def play_next(self, interaction):
        if self.queue:
            url = self.queue.pop(0)
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            self.current_player = player
            interaction.guild.voice_client.play(player, after=lambda e: self.bot.loop.create_task(self.play_next(interaction)))
            await interaction.followup.send(f'Now playing: {player.title}')
        else:
            await interaction.guild.voice_client.disconnect()

    @commands.slash_command(name='play', description='Plays or adds audio from a YouTube video')
    async def play(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        await interaction.response.defer()
        if interaction.user.voice is None:
            await interaction.followup.send('You are not connected to a voice channel.', ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel

        if interaction.guild.voice_client is None:
            await voice_channel.connect()
        elif interaction.guild.voice_client.channel != voice_channel:
            await interaction.guild.voice_client.move_to(voice_channel)

        if self.is_paused:
            self.queue.append(url)
            await interaction.followup.send(f'Added to queue: {url}')
        else:
            self.queue.append(url)
            await interaction.followup.send(f'Added to queue: {url}')
            if not interaction.guild.voice_client.is_playing():
                await self.play_next(interaction)

        # Create buttons
        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(label="Previous", style=disnake.ButtonStyle.danger, custom_id="previous"))
        view.add_item(disnake.ui.Button(label="Pause", style=disnake.ButtonStyle.danger, custom_id="pause"))
        view.add_item(disnake.ui.Button(label="Next", style=disnake.ButtonStyle.danger, custom_id="next"))
        view.add_item(disnake.ui.Button(label="Repeat", style=disnake.ButtonStyle.danger, custom_id="repeat"))

        await interaction.followup.send(f'Now playing: {self.current_player.title if self.current_player else "No song playing"}', view=view)

    @commands.slash_command(name='stop', description='Stop the music and disconnect')
    async def stop(self, interaction: disnake.ApplicationCommandInteraction):
        if interaction.guild.voice_client is not None:
            self.queue.clear()
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message('Disconnected from the voice channel.')

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        if interaction.component.custom_id == "previous":
            await interaction.followup.send("Previous button clicked!")
        elif interaction.component.custom_id == "pause":
            if interaction.guild.voice_client.is_playing():
                interaction.guild.voice_client.pause()
                self.is_paused = True
                await interaction.followup.send("Paused the music.")
            elif self.is_paused:
                interaction.guild.voice_client.resume()
                self.is_paused = False
                await interaction.followup.send("Resumed the music.")
            else:
                await interaction.followup.send("No music is currently playing.", ephemeral=True)
        elif interaction.component.custom_id == "next":
            if self.queue:
                interaction.guild.voice_client.stop()
                await interaction.followup.send("Skipped to the next song.")
            else:
                await interaction.followup.send("No songs in the queue.", ephemeral=True)
        elif interaction.component.custom_id == "repeat":
            await interaction.followup.send("Repeat button clicked!")

def setup(bot):
    bot.add_cog(Music(bot))
