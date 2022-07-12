from discord.ext import commands

from .types import Config

from os import listdir
from orjson import load


class ShikimoriBot(commands.Bot):

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
        await self.load_extension("jishaku")
        await self.load_extension("core.help")
        await self.load_extensions()
        
    def acquire(*args, **kwargs):
        return self.pool.acquire(*args, **kwargs)
