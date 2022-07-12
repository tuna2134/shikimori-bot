from discord.ext import commands
from aiomysql import create_pool, Pool
try:
    import uvloop
except ImportError:
    pass
else:
    uvloop.install()

from .types import Config

from os import listdir
from orjson import load


class ShikimoriBot(commands.Bot):
    pool: Pool | None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("config.json") as f:
            self.config = load(f)

        self.remove_command('help')
        self.version = "0.1.0"

    async def load_extensions(self):
        for file in listdir("cogs"):
            await self.load_extension(f"cogs.{file.replace('.py', '')}")

    async def setup_hook(self):
        self.config["mysql"]["autocommit"] = True
        self.config["mysql"]["loop"] = self.loop
        await create_pool(**self.config["mysql"])
        await self.load_extension("jishaku")
        await self.load_extension("core.help")
        await self.load_extensions()
        
    def acquire(*args, **kwargs):
        return self.pool.acquire(*args, **kwargs)
