import disnake
from typing import Optional
from disnake.ext import commands, tasks
from bot.utils.channels import create_voice_channel, create_voice_open_channel, delete_empty_voice_channels

class SearchParty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_empty_channels.start()

    @commands.slash_command(name='search_party', description='Create a search party')
    async def search_party(
            self, interaction: disnake.ApplicationCommandInteraction,
            channel_name: str,
            description: str = "A search party for finding new friends",
            user_limit: Optional[int] = None
    ):
        guild = interaction.guild
        category = disnake.utils.get(guild.categories, name="search party")

        if not category:
            category = await guild.create_category("search party")

        channel = None
        if user_limit:
            channel = await create_voice_channel(guild=guild, channel_name=channel_name,
                                                 user_limit=user_limit, category=category)
        else:
            channel = await create_voice_open_channel(guild=guild, channel_name=channel_name, category=category)

        await interaction.response.send_message(f'Search party {channel.mention} created successfully!', ephemeral=True)

    @tasks.loop(minutes=1)  # Проверяем каждые минуту
    async def check_empty_channels(self):
        for guild in self.bot.guilds:
            print(f"Checking guild {guild.name}")
            await delete_empty_voice_channels(guild, "search party")

    @check_empty_channels.before_loop
    async def before_check_empty_channels(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(SearchParty(bot))
