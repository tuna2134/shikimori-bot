from discord.ext import commands
from lib.news import News


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def news(self, ctx):
        pass


async def setup(bot):
    await bot.add_cog(News(bot))