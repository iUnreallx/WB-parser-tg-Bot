import os

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from parser_core.handlers.item_add_logic_wb import choose_basket
from parser_core.inline_keyboard.start_kb import menu_kb
from parser_core.state.aricle_state import SearchArticle
from parser_core.wb_scrapper.wb_aiohttp import WbScrapper

router = Router()


@router.callback_query(F.data == 'start_kb_search_by_article')
async def start_kb_search_by_article(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    kb = await menu_kb()
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text='Enter the article number!',
        reply_markup=kb
    )

    await state.set_state(SearchArticle.search)


@router.message(F.text, SearchArticle.search)
async def search_article(message: Message, bot: Bot) -> None:
    await bot.send_message('Searching...\n'
                           'exit - /exit')
    article = message.text
    try:
        if isinstance(int(article), int):
            async with WbScrapper() as wb:
                response = await wb.search_wb(url=f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-5551776&spp=30&ab_testing=false&nm={int(article)}')

                if response['data']['products'] == []:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text='Not found\n'
                             'exit - /exit'
                    )
                elif 'data' in response and 'products' in response['data']:
                    response = response['data']['products'][0]

                    path = os.path.join('parser_core\photo_error', 'img.jpg')
                    photo = await choose_basket(id_value=str(response['id']))
                    try:
                        await bot.send_photo(
                            chat_id=message.chat.id,
                            photo=photo,
                            caption=f'name: {response["name"]}\n'
                                    f'brand {response["brand"]}\n'
                                    f'article: {response["id"]}\n'
                                    f'discounted price: {response["sizes"][0]["price"]["total"] / 100}\n'
                                    f'price without discount: {response["sizes"][0]["price"]["basic"] / 100}\n'
                                    f'rating: {response["reviewRating"]}\n'
                                    f'feedbacks: {response["feedbacks"]}\n\n'
                                    f'link: https://www.wildberries.ru/catalog/{response["id"]}/detail.aspx'
                        )
                    except (TelegramBadRequest, TelegramNetworkError):
                        await bot.send_photo(
                            chat_id=message.chat.id,
                            photo=FSInputFile(path),
                            caption=f'name: {response["name"]}\n'
                                    f'brand {response["brand"]}\n'
                                    f'article: {response["id"]}\n'
                                    f'discounted price: {response["sizes"]["price"]["total"] / 100}\n'
                                    f'price without discount: {response["sizes"]["price"]["basic"] / 100}\n'
                                    f'rating: {response["reviewRating"]}\n'
                                    f'feedbacks: {response["feedbacks"]}\n\n'
                                    f'link: https://www.wildberries.ru/catalog/{response["id"]}/detail.aspx'
                        )
    except ValueError:
        await bot.send_message(
            chat_id=message.chat.id,
            text='enter the article number.\n'
                 'exit - /exit'
        )
