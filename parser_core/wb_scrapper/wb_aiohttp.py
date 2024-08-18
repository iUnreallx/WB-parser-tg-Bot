import json
from typing import Union

import aiohttp

class WbScrapper:
    headers = {
        'Accept': "*/*",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def search_wb(self, url, user_id: Union[int, None] = None) -> Union[dict, list]:
        async with self.session.get(url) as response:
            response_text = await response.text()
            data = json.loads(response_text)
            return data