from bs4 import BeautifulSoup
import aiohttp


class News:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_news(self):
        async with self.session.get("https://shikimori-anime.com/news/list00010000.html") as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            news = soup.find("div", id="list_01")
            data = []
            for item in news.find_all("div", class_="title"):
                data.append(
                    {
                        "title": item.find("a").text,
                        "link": f'https://shikimori-anime.com/{item.find("a")["href"][3:]}'
                    }
                )
        return data


if __name__ == "__main__":
    import asyncio
    async def main():
        async with News() as news:
            print(await news.get_news())
    asyncio.run(main())
