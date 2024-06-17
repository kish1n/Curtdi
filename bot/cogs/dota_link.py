import disnake
from disnake.ext import commands

class DotaLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='get_dota_rank', description='Get Dota 2 rank from linked Steam account')
    async def get_dota_rank(self, interaction: disnake.ApplicationCommandInteraction, username: str):
        await interaction.response.send_message(f'Getting Dota 2 rank for {interaction.user.name} '
                                                f'with Steam username {username}')

def setup(bot):
    bot.add_cog(DotaLink(bot))