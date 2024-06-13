import disnake
from disnake.ext import commands, tasks
import asyncio
from datetime import timedelta, datetime

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """TEXT MUTE COMMAND"""

    @commands.slash_command(name='txtmute', description='Mute a user')
    @commands.has_permissions(manage_messages=True)
    async def txtmute(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member, mute_time: int):
        """Mute a member for a specified number of seconds."""
        mute_role = disnake.utils.get(interaction.guild.roles, name="Muted")

        if mute_role is None:
            mute_role = await interaction.guild.create_role(name="Muted")

            for channel in interaction.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role)
        await interaction.response.send_message(f"{member.mention} has been muted for {mute_time} seconds.")

        self.unmute_task.start(interaction.guild.id, member.id, mute_role.id, mute_time)

    @tasks.loop(count=1)
    async def unmute_task(self, guild_id: int, member_id: int, mute_role_id: int, mute_time: int):
        await asyncio.sleep(mute_time * 60)
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(member_id)
        mute_role = guild.get_role(mute_role_id)

        if member and mute_role:
            await member.remove_roles(mute_role)
            channel = guild.system_channel  # Можно выбрать другой канал для уведомления
            if channel:
                await channel.send(f"{member.mention} has been unmuted.")

    @unmute_task.before_loop
    async def before_unmute_task(self):
        await self.bot.wait_until_ready()

    @txtmute.error
    async def mute_error(self, interaction: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have the necessary permissions to use this command.")
        elif isinstance(error, commands.BadArgument):
            await interaction.response.send_message("Please ensure you've mentioned a"
                                                    " valid member and provided a valid time in seconds.")
        else:
            await interaction.response.send_message("An error occurred while trying to mute the member.")
            print(error)

    """TIMEOUT COMMAND"""

    @commands.slash_command(name='timeout', description='Timeout a user')
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member,
                      timeout_minutes: int):
        """Timeout a member for a specified number of minutes."""
        timeout_duration = timedelta(minutes=timeout_minutes)
        until_time = datetime.utcnow() + timeout_duration
        await member.timeout(until=until_time)
        await interaction.response.send_message(f"{member.mention} has been timed out for {timeout_minutes} minutes.")

        self.remove_timeout_task.start(interaction.guild.id, member.id, timeout_minutes)

    @tasks.loop(count=1)
    async def remove_timeout_task(self, guild_id: int, member_id: int, timeout_minutes: int):
        await asyncio.sleep(timeout_minutes * 60)
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(member_id)

        if member:
            await member.timeout(until=None)  # Remove timeout
            channel = guild.system_channel  # Можно выбрать другой канал для уведомления
            if channel:
                await channel.send(f"{member.mention} is no longer timed out.")

    @remove_timeout_task.before_loop
    async def before_remove_timeout_task(self):
        await self.bot.wait_until_ready()

    @timeout.error
    async def timeout_error(self, interaction: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have the necessary permissions to use this command.")
        elif isinstance(error, commands.BadArgument):
            await interaction.response.send_message(
                "Please ensure you've mentioned a valid member and provided a valid time in minutes.")
        else:
            await interaction.response.send_message("An error occurred while trying to timeout the member.")
            print(error)

def setup(bot):
    bot.add_cog(Admin(bot))
