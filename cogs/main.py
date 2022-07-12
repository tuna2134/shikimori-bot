from discord.ext import commands


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{self.bot.latency}`ms")

    @commands.command()
    async def info(self, ctx):
        await ctx.send(f"ShikimoriBot v{self.bot.version}")

async def setup(bot):
    await bot.add_cog(Main(bot))