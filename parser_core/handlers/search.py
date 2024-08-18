import asyncio
import os

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from parser_core.handlers.item_add_logic_wb import send_application
from parser_core.inline_keyboard.files_parser_kb import generate_parser_kb
from parser_core.inline_keyboard.start_kb import menu_kb
from parser_core.state.search_state import SearchState
from parser_core.wb_scrapper.wb_aiohttp import WbScrapper

search_router = Router()


@search_router.callback_query(F.data == 'start_kb_search')
async def start_kb_search(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    kb = await menu_kb()
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id)
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text='Enter a query',
        reply_markup=kb
    )
    await state.set_state(SearchState.search)


@search_router.message(F.text, SearchState.search)
async def search_handler(message: Message, bot: Bot) -> None:
    await bot.send_message(chat_id=message.chat.id, text='searching...\n'
                                                         'exit - /exit')
    user_id = message.from_user.id
    client_response = message.text

    del_sym = ['!', '?', '#', '@', '$', '%', '^', '&', '*', '(', ')',
               '-', '_', '=', '+', '{', '}', '[', ']', '|', '\\', ':',
               ';', '"', "'", '<', '>', ',', '.', '/', '~', '`']

    result = [symbols for symbols in client_response if symbols not in del_sym]
    filtered_text = ''.join(result)
    text = (filtered_text).replace(' ', '%20')

    counter = 0
    while True:
        async with WbScrapper() as wb:
            response = await wb.search_wb(url=
            f'https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-5551776&query={str(text)}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false',
            user_id=user_id)

            if 'data' in response and 'products' in response['data']:
                products = response['data']['products']
                if len(products) < 2:
                    counter += 1
                    await asyncio.sleep(2)
                    if counter < 4:
                        continue
                    else:
                        await bot.send_message(
                            chat_id=message.chat.id,
                            text='Not fount. Please, try again'
                        )
                        break

                else:
                    item = await send_application(
                        data=products,
                        user_id=user_id,
                        text=text
                    )
                    result.clear()
                    category = "18+" if item["is_adult"] else "0+"

                    path = os.path.join('parser_core\photo_error', 'img.jpg')
                    kb = await generate_parser_kb(user_id=user_id, page=1)
                    try:
                        await bot.send_photo(
                            chat_id=message.chat.id,
                            photo=item["photo"],
                            caption=f'name: {item["name"]}\n'
                                    f'brand: {item["brand"]}\n'
                                    f'article: {item["id"]}\n'
                                    f'discounted price: {item["skidka"]}\n'
                                    f'price without discount: {item["iznachalno"]}\n'
                                    f'rating: {item["raiting"]}\n'
                                    f'feedbacks: {item["feedbacks"]}\n'
                                    f'category: {category}\n\n'
                                    f'link: https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx',
                            reply_markup=kb
                                )

                    except (TelegramBadRequest, TelegramNetworkError):
                        await bot.send_photo(
                            chat_id=message.chat.id,
                            photo=FSInputFile(path),
                            caption=f'name: {item["name"]}\n'
                                    f'brand: {item["brand"]}\n'
                                    f'article: {item["id"]}\n'
                                    f'discounted price: {item["skidka"]}\n'
                                    f'price without discount: {item["iznachalno"]}\n'
                                    f'rating: {item["raiting"]}\n'
                                    f'feedbacks: {item["feedbacks"]}\n'
                                    f'category: {category}\n\n'
                                    f'link: https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx',
                            reply_markup=kb
                        )
                    break