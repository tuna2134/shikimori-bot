from core import ShikimoriBot

import discord


bot = ShikimoriBot(command_prefix="sh.", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Started")


if __name__ == "__main__":
    bot.run()