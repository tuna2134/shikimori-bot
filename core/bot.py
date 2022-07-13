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
from orjson import loads


class ShikimoriBot(commands.Bot):
    pool: Pool | None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("config.json") as f:
            self.config = loads(f.read())

        self.remove_command('help')
        self.version = "0.1.0"

    async def load_extensions(self):
        for file in listdir("cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"cogs.{file.replace('.py', '')}")

    async def setup_hook(self):
        self.config["mysql"]["autocommit"] = True
        self.config["mysql"]["loop"] = self.loop
        self.pool = await create_pool(**self.config["mysql"])
        await self.load_extension("jishaku")
        await self.load_extension("core.admin")
        await self.load_extension("core.help")
        await self.load_extensions()
        
    async def is_owner(self, user):
        return user.id in [739702692393517076] or await super().is_owner()
        
    def acquire(self, *args, **kwargs):
        return self.pool.acquire(*args, **kwargs)

    async def close(self):
        await super().close()
        self.pool.close()
        await self.pool.wait_closed()
