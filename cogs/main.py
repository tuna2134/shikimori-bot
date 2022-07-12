from discord.ext import commands

from .news import Embed

from inspect import cleandoc


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(extras={
        "args": []
    }, description="pingコマンド")
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.bot.latency * 1000, 1)}`ms")

    @commands.command(extras={
        "args": []
    }, description="Infoコマンド")
    async def info(self, ctx):
        await ctx.send(embed=Embed(title="Information", description=cleandoc(f"""
        Version: v{self.bot.version}
        
        このbotは「可愛いだけじゃない式守さん」を応援するために作られたボットです。
　　　　　著作権者などにbot開発中止命令及び提供中止命令が出た場合、それに従いますので、悪しからずご了承ください。
     　　
        ※著作権者はこの場合式守さん制作委員会及び真木圭吾さんのことを表します。""")))

async def setup(bot):
    await bot.add_cog(Main(bot))
