import disnake
from disnake.ext import commands
from disnake import ButtonStyle
from config import settings  # Импортируйте settings
from bot.utils.rolesbutton import Role  # Импортируйте класс Role
class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='game_roles', description='Выберите свою игру')
    async def game_roles(self, inter: disnake.ApplicationCommandInteraction):
        view = Role()
        await inter.response.send_message("Выберите игру:", view=view)

def setup(bot):
    bot.add_cog(RoleManager(bot))