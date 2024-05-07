import asyncio
import os
import random
import re
import sys
from functools import reduce, partial
from multiprocessing import Pool, Lock
from operator import or_, iconcat

import orjson
from aiohttp import ClientSession

proxy_string = os.getenv("PROXY")

regex_uuid = re.compile(r'(?<="uuid":")[0-9a-f-]{36}(?=")')
regex_article_url = re.compile(r'link--(?:g3Vwe|ILico)" href="((?:https://journal.tinkoff.ru)?/[\w-]+?/)[?"]')
regex_flow_url = re.compile(r'item--gPa1X" href="(/flows/[\w-]+?/)[?"]')


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0'
}


def absolute_from_relative(url: str) -> str:
    return f"https://journal.tinkoff.ru{url}" if not url.startswith("http") else url


async def get_comments(article_url: str) -> list[dict]:
    await asyncio.sleep(random.random() * 0.2)
    async with ClientSession() as session:
        async with session.get(url=article_url, headers=headers, proxy=proxy_string) as uuid_response:
            uuid = regex_uuid.search(await uuid_response.text()).group()
            # print(uuid)

        async with session.get(
            url="https://social.journal.tinkoff.ru/api/v20/comments/",
            params={"uuid": uuid, "unsafe": "true"},
            headers=headers, proxy=proxy_string
        ) as comments_response:
            return (await comments_response.json())["data"]


def article_urls_from_text(text: str) -> set[str]:
    return set(map(absolute_from_relative, regex_article_url.findall(text)))


async def get_article_urls(flow_url: str) -> set[str]:
    flow_url = flow_url.strip("/")
    pages = []

    async with ClientSession() as session:
        for suffix in ["/best", "/posts", ""]:
            for page in range(1, 10):
                # print(f"{suffix}/{page} {flow_url}")
                # print(f"{flow_url}{suffix}/page/{page}")
                async with session.get(
                        url=f"{flow_url}/{suffix}/page/{page}",
                        headers=headers, proxy=proxy_string
                ) as response:
                    pages.append(await response.text())

    return reduce(or_, map(article_urls_from_text, pages))


async def get_flow_urls() -> list[str]:
    url = "https://journal.tinkoff.ru/flows/"

    async with ClientSession() as session:
        return list(
            map(
                absolute_from_relative,
                regex_flow_url.findall(
                    await (await session.get(url=url, headers=headers, proxy=proxy_string)).text()
                )
            )
        )


async def process_flow(flow_url: str, visited_article_urls: set[str]) -> list[dict]:
    # print(f"Pinging flow {flow_url}")

    try:
        article_urls = await get_article_urls(flow_url=flow_url)

        visited_update_lock.acquire()
        new_article_urls = article_urls - visited_article_urls
        visited_article_urls.update(new_article_urls)
        visited_update_lock.release()

        current_comments = []
        for article_url in new_article_urls:
            comments = await get_comments(article_url=article_url)
            current_comments.append(comments)

        flat_current_comments = reduce(iconcat, current_comments, [])

        print(f"PROCESSED {len(flat_current_comments)} comments from {flow_url}")

        return flat_current_comments
    except Exception:
        return []


def process_flow_wrapper(flow_url, visited_article_urls) -> list[dict]:
    return asyncio.run(process_flow(flow_url, visited_article_urls))


def pool_initializer(lock_: Lock):
    # noinspection PyGlobalUndefined
    global visited_update_lock
    visited_update_lock = lock_


async def main() -> None:
    visited_article_urls = set()
    visited_update_lock = Lock()

    with Pool(8, initializer=pool_initializer, initargs=(visited_update_lock,)) as pool:
        all_comments = pool.map(
            partial(
                process_flow_wrapper,
                visited_article_urls=visited_article_urls
            ),
            await get_flow_urls()
        )

    flat_comments = reduce(iconcat, all_comments, [])

    with open("data/comments.json", "wb") as json_file:
        json_file.write(orjson.dumps(flat_comments))


if __name__ == "__main__":
    asyncio.run(main())


# print(get_comments("https://journal.tinkoff.ru/1000-km-by-bike/"))
# print(get_article_urls("https://journal.tinkoff.ru/flows/invest"))
# print(get_flow_urls())
