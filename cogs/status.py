from discord.ext import commands, tasks
import psutil

from time import time


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def cog_load(self):
        async with self.bot.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""CREATE TABLE IF NOT EXISTS Status(
                    time BIGINT, cpu BIGINT, memory BIGINT, disk BIGINT, ping BIGINT
                );""")
        self.change_status.start()
    
    @tasks.loop(minutes=5)
    async def change_status(self):
        async with self.bot.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO Status VALUES(%s, %s, %s, %s, %s);",
                    (int(time()), int(psutil.cpu_percent(interval=None)), int(psutil.virtual_memory().percent),
                    int(psutil.disk_usage("./").percent), round(self.bot.latency * 1000, 1))
                )
                week = 60 * 60 * 24 * 7
                await cursor.execute("DELETE FROM Status WHERE time <= %s;", (int(time()) - week,))

async def setup(bot):
    await bot.add_cog(Status(bot))
