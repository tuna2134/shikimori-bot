from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands = []

    @commands.Cog.listener()
    async def on_ready(self):
        for command in self.bot.commands:
            if command.hidden:
                continue
            await self.add_command(command)

    async def add_command(self, command):
        self.commands.append({
            "name": command.name,
            "description": command.description,
            "aliases": command.aliases,
            "args": command.extras["args"]
        })

    @commands.command()
    async def help(self, ctx, *, command: str | None = None):
        if command:
            for cmd in self.commands:
                if cmd["name"] == command:
                    await ctx.send(f"```\n{cmd['name']} - {cmd['description']}\n\n{cmd['args']}\n```")
        else:
            message = []
            for cmd in self.commands:
                message.append(f"```\n{cmd['name']} - {cmd['description']}\n\n{cmd['args']}\n```")
            await ctx.send("\n".join(message))


async def setup(bot):
    await bot.add_cog(Help(bot))