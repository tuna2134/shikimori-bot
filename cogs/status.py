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
                    time BIGINT, cpu TEXT, memory TEXT, disk TEXT, ping TEXT
                );""")
        self.change_status.start()
    
    @tasks.loop(minutes=5)
    async def change_status(self):
        async with self.bot.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO Status VALUES(%s, %s, %s, %s, %s);",
                    (int(time()), str(psutil.cpu_percent(interval=None)), str(psutil.virtual_memory().percent),
                    str(psutil.disk_usage("./").percent), str(round(self.bot.latency * 1000, 1))
                )
                week = 60 * 60 * 24 * 7
                await cursor.execute("DELETE FROM Status WHERE time <= %s;", (int(time()) - week,))

async def setup(bot):
    await bot.add_cog(Status(bot))
