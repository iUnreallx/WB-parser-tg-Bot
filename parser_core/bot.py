import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv

from parser_core.handlers import start, search, next_pages_logic, next_paragraph_logic, search_by_article, exit

load_dotenv(find_dotenv())

TOKEN = getenv("TOKEN")

async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


    dp.include_routers(
        start.start_router,
        exit.router,
        search.search_router,
        next_pages_logic.router,
        next_paragraph_logic.router,
        search_by_article.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot polling stopped.')