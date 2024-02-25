import asyncio
import httpx


class WikiSearch:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(WikiSearch, cls).__new__(cls)
            cls.cache = {}
        return cls._instance

    async def search(self, query: str):
        await asyncio.sleep(5)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "format": "json",
                    "list": "search",
                    "srsearch": query
                }
            )
        return response
