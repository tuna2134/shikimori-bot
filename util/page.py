from discord import ui, Embed


class Page(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self.current_page = 0

    def add_page(self, embed: Embed):
        self.pages.append(embed)

    def remove_page(self, index: int):
        self.pages.pop(index)

    @ui.button(label="<")
    async def left(self, interaction, button):
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = len(self.pages) - 1
        await self.update(interaction)
        
    @ui.button(label=">")
    async def right(self, interaction, button):
        self.current_page += 1
        if self.current_page > len(self.pages) - 1:
            self.current_page = 0
        await self.update(interaction)
        
    async def update(self, interaction):
        await interaction.message.edit(embed=self.pages[self.current_page])
        
    @property
    def first(self):
        return self.pages[0]
