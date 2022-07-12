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

    @ui.button(label="左")
    async def left(self, interaction. button):
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = len(self.pages) - 1
        await self.update()