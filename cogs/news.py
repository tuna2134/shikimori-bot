from discord.ext import commands, tasks
from util.news import News

import discord


class Embed(discord.Embed):
    def __init__(self, *args, **kwargs):
        kwargs["color"] = 0xf9c1cf
        super().__init__(*args, **kwargs)

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last = None
        
    async def cog_load(self):
        async with self.bot.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS News(link TEXT);")
                await cursor.execute("CREATE TABLE IF NOT EXISTS NewsChannel(channelid BIGINT);")
                await cursor.execute("SELECT * FROM News limit=1;")
                self.last = await cursor.fetchone()[0]
        self.notice.start()
        
    @tasks.loop(minutes=1)
    async def notice(self):
        async with News() as news:
            news = await news.get_news()[0]
            if news["link"] != self.last:
                await self.send_notice(news)
    
    async def send_notice(self, news):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM NewsChannel;")
                for (channelid,) in await cursor.fetchall():
                    channel = self.bot.get_channel(channelid)
                    if channel is not None:
                        await channel.send(embed=Embed(title=news["title"], description=news["link"]))
                await cursor.execute("INSERT INTO News(%s);", (news["link"],))
                await cursor.execute("DELECT FROM News WHERE link=%s", (self.link,))
                self.link = news["link"]

    @commands.group()
    async def news(self, ctx):
        pass
    
    @news.command()
    async def channel(self, ctx):
        pass


async def setup(bot):
    await bot.add_cog(News(bot))
