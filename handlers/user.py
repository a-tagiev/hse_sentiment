import orjson as json
from aiohttp import ClientSession

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.text_decorations import markdown_decoration as md

from misc.config import API_URL, rate_limit_timeout
from misc.rate_limiter import RateLimiter


router = Router()
rate_limiter = RateLimiter(rate_limit_timeout)


@router.message(Command(commands=["start", "help"]))
async def start_help_command(message: Message) -> None:
    await message.answer(
        "Привет! Я - бот, который умеет определять тональность русского текста.\n"
        "Для этого просто напишите мне любое сообщение, и я его проанализирую.\n"
        f"(Минимальный интервал между запросами в секундах: {rate_limit_timeout})",
        parse_mode=ParseMode.HTML
    )


@router.message()
async def on_message(message: Message) -> None:
    until_next_request = round(await rate_limiter.check(str(message.from_user.id)), 2)

    if until_next_request > 0:
        await message.reply(
            md.italic(
                f"Вы сможете отправить следующий запрос через {md.bold(md.quote(str(until_next_request)))} секунд"
            )
        )
        return

    async with ClientSession() as session:
        async with session.post(
                url=API_URL,
                data=json.dumps({"text": message.text}),
                headers={"Content-Type": "application/json", "Accept": "application/json"}
        ) as response:
            if response.status == 200:
                response_json = await response.json()
                sentiment = response_json["sentiment"].upper()
            else:
                sentiment = "NEUTRAL"

            await message.reply(f"Тональность текста: {md.bold(sentiment)}")
