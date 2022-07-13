from discord import ui, Embed, Interaction


class Page(ui.View):
    def __init__(self, *args, **kwargs):
        self.ext = kwargs.pop("ext", None)
        super().__init__(*args, **kwargs)
        self.pages = []
        self.current_page = 0

    def add_page(self, embed: Embed):
        self.pages.append(embed)

    def remove_page(self, index: int):
        self.pages.pop(index)

    @ui.button(emoji="⬅", custom_id="page_left")
    async def left(self, interaction, button):
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = len(self.pages) - 1
        await self.update(interaction)

    @ui.button(emoji="⏹", custom_id="page_close")
    async def page_close(self, interaction, button):
        self.stop()
        await interaction.response.edit_message(view=None)

    @ui.button(emoji="➡", custom_id="page_right")
    async def right(self, interaction, button):
        self.current_page += 1
        if self.current_page > len(self.pages) - 1:
            self.current_page = 0
        await self.update(interaction)
        
    async def update(self, interaction):
        embed = self.pages[self.current_page]
        embed.set_footer(text=f"{self.current_page + 1}/{len(self.pages)}")
        await interaction.response.edit_message(embed=embed)
        
    @property
    def first(self):
        embed = self.pages[0]
        embed.set_footer(text=f"1/{len(self.pages)}")
        return embed
