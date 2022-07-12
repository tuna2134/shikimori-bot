from discord.ext import commands, tasks
from util import News as NewsFetch, Page

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
                await cursor.execute("SELECT * FROM News LIMIT 1;")
                if self.last:
                    self.last = (await cursor.fetchone())[0]
                await cursor.execute("SELECT * FROM NewsChannel;")
                self.channelids = [channelid for (channelid,) in await cursor.fetchall()]
        self.notice.start()
        
    @tasks.loop(minutes=1)
    async def notice(self):
        async with NewsFetch() as news:
            news = (await news.get_news())[0]
            if news["link"] != self.last:
                await self.send_notice(news)
    
    async def send_notice(self, news):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                for channelid in channelids:
                    channel = self.bot.get_channel(channelid)
                    if channel is not None:
                        await channel.send(embed=Embed(title=news["title"], description=news["link"]))
                await cursor.execute("DELETE FROM News;")
                await cursor.execute("INSERT INTO News VALUES(%s);", (news["link"],))
                self.link = news["link"]

    @commands.group()
    async def news(self, ctx):
        pass
    
    @news.command()
    async def show(self, ctx):
        page = Page()
        async with NewsFetch() as news:
            items = await news.get_news()
            for item in items:
                page.add_page(Embed(title=item["title"], description=item["link"]))
        await ctx.send(view=page, embed=page.first)
    
    @news.command()
    async def channel(self, ctx):
        if ctx.channel.id in self.channelids:
            return await ctx.send("既に登録されています。")
        self.channelids.append(ctx.channel.id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO NewsChannel VALUES(%s);", (ctx.channel.id,))
        await ctx.send("登録しました。")


async def setup(bot):
    await bot.add_cog(News(bot))
