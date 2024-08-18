import asyncio
import json
import os

import aiofiles
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from parser_core.handlers.item_add_logic_wb import add_parapraph_send_application
from parser_core.inline_keyboard.files_parser_kb import generate_parser_kb
from parser_core.wb_scrapper.wb_aiohttp import WbScrapper

router = Router()


@router.callback_query(F.data.startswith('generate_next_paragraph_'))
async def generate_next_paragraph(callback: CallbackQuery, bot: Bot) -> None:
    user_id = callback.from_user.id
    page = int(callback.data.split('_')[3])
    leaf_call = int(callback.data.split('_')[4])
    leaf = 1

    final = int(leaf + leaf_call)

    try:
        async with aiofiles.open(f'wbs_{str(user_id)}.json', 'r', encoding='utf-8') as file:
            content = await file.read()
            existing_data = json.loads(content)
    except FileNotFoundError:
        await callback.answer('Please enter a new request')
        return

    request = existing_data[0]["search"]

    if len(existing_data) - page > 100:

        async with aiofiles.open(f'wbs_{str(user_id)}.json', 'r', encoding='utf-8') as file:
            content = await file.read()
            existing_data = json.loads(content)

        item = existing_data[int(final * 100 + 1)]
        category = "18+" if item["is_adult"] else "0+"

        end = page % 100
        if end == 0:
            xend = page + 1
        else:
            xend = page - end + 101

        path = os.path.join('parser_core\photo_error', 'img.jpg')
        kb = await generate_parser_kb(user_id=user_id, page=xend, leaf=final)
        try:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=InputMediaPhoto(
                    media=item["photo"],
                    caption=f'name: {item["name"]}\n'
                            f'brand: {item["brand"]}\n'
                            f'article: {item["id"]}\n'
                            f'discounted price: {item["skidka"]}\n'
                            f'price without discount: {item["iznachalno"]}\n'
                            f'rating: {item["raiting"]}\n'
                            f'feedbacks: {item["feedbacks"]}\n'
                            f'category: {category}\n\n'
                            f'link: https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx'
                ),
                reply_markup=kb
            )

        except (TelegramBadRequest, TelegramNetworkError):
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=InputMediaPhoto(
                    media=FSInputFile(path),
                    caption=f'name: {item["name"]}\n'
                            f'brand: {item["brand"]}\n'
                            f'article: {item["id"]}\n'
                            f'discounted price: {item["skidka"]}\n'
                            f'price without discount: {item["iznachalno"]}\n'
                            f'rating: {item["raiting"]}\n'
                            f'feedbacks: {item["feedbacks"]}\n'
                            f'category: {category}\n\n'
                            f'link: https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx'
                ),
                reply_markup=kb
            )
    else:
        counter = 0
        while True:
            async with WbScrapper() as wb:
                response = await wb.search_wb(url=
                                              f'https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-1257786&page={leaf + 1}&query={str(request)}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false',
                                              user_id=user_id)

                if 'data' in response and 'products' in response['data']:
                    products = response['data']['products']

                    if len(products) < 2:
                        counter += 1
                        await asyncio.sleep(2)
                        if counter < 4:
                            continue
                        else:
                            await callback.answer(
                                chat_id=callback.message.chat.id,
                                text='Not found. Please try again'
                            )
                            break

                    else:
                        await add_parapraph_send_application(
                            data=products,
                            user_id=user_id,
                            leaf=final,
                            existing_data=existing_data
                        )
                        async with aiofiles.open(f'wbs_{str(user_id)}.json', 'r', encoding='utf-8') as file:
                            content = await file.read()
                            existing_data = json.loads(content)

                        item = existing_data[int(final * 100 + 1)]
                        category = "18+" if item["is_adult"] else "0+"

                        end = page % 100
                        if end == 0:
                            xend = page + 1
                        else:
                            xend = page - end + 101

                        path = os.path.join('parser_core\photo_error', 'img.jpg')
                        kb = await generate_parser_kb(user_id=user_id, page=xend, leaf=final)
                        try:
                            await bot.edit_message_media(
                                chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                media=InputMediaPhoto(
                                    media=item["photo"],
                                    caption=f'name: {item["name"]}\n'
                                            f'brand: {item["brand"]}\n'
                                            f'article: {item["id"]}\n'
                                            f'discounted price: {item["skidka"]}\n'
                                            f'price without discount: {item["iznachalno"]}\n'
                                            f'rating: {item["raiting"]}\n'
                                            f'feedbacks: {item["feedbacks"]}\n'
                                            f'category: {category}\n\n'
                                            f'link: https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx'
                                ),
                                reply_markup=kb
                            )

                        except (TelegramBadRequest, TelegramNetworkError):
                            await bot.edit_message_media(
                                chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                media=InputMediaPhoto(
                                    media=FSInputFile(path),
                                    caption=f'name: {item["name"]}\n'
                                            f'brand: {item["brand"]}\n'
                                            f'article: {item["id"]}\n'
                                            f'discounted price: {item["skidka"]}\n'
                                            f'price without discount: {item["iznachalno"]}\n'
                                            f'rating: {item["raiting"]}\n'
                                            f'feedbacks: {item["feedbacks"]}\n'
                                            f'category: {category}\n\n'
                                            f'link: https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx'
                                ),
                                reply_markup=kb
                            )
                        break


@router.callback_query(F.data.startswith('generate_previous_paragraph_'))
async def generate_back_paragraph(callback: CallbackQuery, bot: Bot) -> None:
    user_id = callback.from_user.id
    page = int(callback.data.split('_')[3])
    leaf_call = int(callback.data.split('_')[4])
    leaf = 1

    final = int(leaf_call - leaf)

    try:
        async with aiofiles.open(f'wbs_{str(user_id)}.json', 'r', encoding='utf-8') as file:
            content = await file.read()
            existing_data = json.loads(content)
    except FileNotFoundError:
        await callback.answer('Please enter a new request')
        return

    item = existing_data[int(final if final > 0 else 1 * 100 - 99)]
    category = "18+" if item["is_adult"] else "0+"

    end = page % 100
    if end == 0:
        xend = page - 100 + 1
    else:
        xend = page - end - 99

    path = os.path.join('parser_core\photo_error', 'img.jpg')
    kb = await generate_parser_kb(user_id=user_id, page=xend, leaf=final)
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=item["photo"],
                caption=f'name: {item["name"]}\n'
                        f'brand: {item["brand"]}\n'
                        f'article: {item["id"]}\n'
                        f'discounted price: {item["skidka"]}\n'
                        f'price without discount: {item["iznachalno"]}\n'
                        f'rating: {item["raiting"]}\n'
                        f'feedbacks: {item["feedbacks"]}\n'
                        f'category: {category}\n\n'
                        f'link: https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx'
            ),
            reply_markup=kb
        )

    except (TelegramBadRequest, TelegramNetworkError):
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=FSInputFile(path),
                caption=f'name: {item["name"]}\n'
                        f'brand: {item["brand"]}\n'
                        f'article: {item["id"]}\n'
                        f'discounted price: {item["skidka"]}\n'
                        f'price without discount: {item["iznachalno"]}\n'
                        f'rating: {item["raiting"]}\n'
                        f'feedbacks: {item["feedbacks"]}\n'
                        f'category: {category}\n\n'
                        f'link: https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx'
            ),
            reply_markup=kb
        )