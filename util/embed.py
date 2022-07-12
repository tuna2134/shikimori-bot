import discord


class Embed(discord.Embed):
    def __init__(self, *args, **kwargs):
        kwargs["color"] = 0xf9c1cf
        super().__init__(*args, **kwargs)
