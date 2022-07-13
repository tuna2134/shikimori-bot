from discord.ext import commands

from util import Embed


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="admin", invoke_without_command=True)
    @commands.is_owner()
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Admin commands")

    @admin.command(name="sql")
    async def sql(self, ctx, *, query):
        """Runs a SQL query"""
        results = []
        async with self.bot.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                returned = await cur.fetchall()
                print(returned)
                if returned is not None:
                    for row in returned:
                        results.append(" | ".join(str(col) for col in row))
        await ctx.send(embed=Embed(title="MySQL", description="\n".join(results)))


async def setup(bot):
    await bot.add_cog(Admin(bot))
