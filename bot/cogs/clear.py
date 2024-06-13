from disnake.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='clear', description='Clear messages in the channel')
    async def clear(self, ctx, amount: int):
        await ctx.response.send_message(f'Clearing {amount} messages...')
        await ctx.channel.purge(limit=amount + 1)

def setup(bot):
    bot.add_cog(Clear(bot))