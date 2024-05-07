import aiohttp
import asyncio
import os


proxy_string = os.getenv("PROXY")

async def get_response_using_proxy():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                'https://ip.oxylabs.io/',
                proxy=proxy_string
        ) as response:
            print('Status Code: ', response.status)
            print('Body: ', await response.text())

asyncio.run(get_response_using_proxy())
