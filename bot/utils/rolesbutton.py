import disnake
from disnake.ext import commands
from typing import Optional

class Role(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = Optional[str]

    @staticmethod
    async def handle_role(self, inter: disnake.CommandInteraction, role_name: str):
        role = disnake.utils.get(inter.guild.roles, name=role_name)
        if role in inter.author.roles:
            await inter.author.remove_roles(role)
            await inter.response.send_message(f"Роль {role_name} удалена.", ephemeral=True)
        else:
            await inter.author.add_roles(role)
            await inter.response.send_message(f"Роль {role_name} добавлена.", ephemeral=True)

    @disnake.ui.button(label='Dota', style=disnake.ButtonStyle.red)
    async def dota(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        self.value = "Dota"
        await self.handle_role(self, inter, "Dota")

    @disnake.ui.button(label='CS:GO', style=disnake.ButtonStyle.green)
    async def csgo(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        self.value = "CS:GO"
        await self.handle_role(self, inter, "CS:GO")

    @disnake.ui.button(label='Valorant', style=disnake.ButtonStyle.blurple)
    async def pubg(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        self.value = "Valorant"
        await self.handle_role(self, inter, "Valorant")