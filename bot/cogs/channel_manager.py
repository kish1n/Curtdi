import disnake
from disnake.ext import commands, tasks
from bot.utils.channels import create_voice_channel, delete_empty_voice_channels


class ChannelManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_empty_channels.start()

    @commands.slash_command(name='create_voice_channel', description='Create a voice channel with a user limit')
    async def create_voice_channel(self, interaction: disnake.ApplicationCommandInteraction,
                                   channel_name: str, user_limit: int):
        guild = interaction.guild
        category = disnake.utils.get(guild.categories, name="users voice channels")
        if not category:
            category = await guild.create_category("users voice channels")
        channel = await create_voice_channel(guild, channel_name, user_limit, category)
        await interaction.response.send_message(f'Voice channel {channel.mention} created successfully!')

    @tasks.loop(minutes=1)  # Проверяем каждые минуту
    async def check_empty_channels(self):
        for guild in self.bot.guilds:
            print(f"Checking guild {guild.name}")
            await delete_empty_voice_channels(guild, "users voice channels")

    @check_empty_channels.before_loop
    async def before_check_empty_channels(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(ChannelManager(bot))