import json
import os

import aiofiles
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from parser_core.inline_keyboard.files_parser_kb import generate_parser_kb

router = Router()


@router.callback_query(F.data.startswith('generate_next_page'))
async def generate_next_page(callback: CallbackQuery, bot: Bot) -> None:
    user_id = callback.from_user.id
    page = int(callback.data.split('_')[3])
    leaf = int(callback.data.split('_')[4])

    try:
        async with aiofiles.open(f'wbs_{str(user_id)}.json', 'r', encoding='utf-8') as file:
            content = await file.read()
            files = json.loads(content)
    except FileNotFoundError:
        await callback.answer('Please enter a new request')
        return

    if page < len(files):
        item = files[page + 1]
        category = "18+" if item["is_adult"] else "0+"

        path = os.path.join('parser_core', 'photo_error', 'img.jpg')
        kb = await generate_parser_kb(user_id=user_id, page=page + 1, leaf=leaf)

        try:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=(
                    InputMediaPhoto(
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
                    )
                ),
            reply_markup=kb
            )
        except (TelegramBadRequest, TelegramNetworkError):
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=(
                    InputMediaPhoto(
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
                    )
                ),
                reply_markup=kb
            )


@router.callback_query(F.data.startswith('generate_back_page'))
async def generate_back_page(callback: CallbackQuery, bot: Bot) -> None:
    user_id = callback.from_user.id
    page = int(callback.data.split('_')[3])
    leaf = int(callback.data.split('_')[4])

    try:
        async with aiofiles.open(f'wbs_{str(user_id)}.json', 'r', encoding='utf-8') as file:
            content = await file.read()
            files = json.loads(content)
    except FileNotFoundError:
        await callback.answer('Please enter a new request')
        return

    if page < len(files):
        item = files[page - 1]
        category = "18+" if item["is_adult"] else "0+"

        path = os.path.join('parser_core', 'photo_error', 'img.jpg')
        kb = await generate_parser_kb(user_id=user_id, page=page - 1, leaf=leaf)

        try:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=(
                    InputMediaPhoto(
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
                    )
                ),
            reply_markup=kb
            )
        except (TelegramBadRequest, TelegramNetworkError):
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=(
                    InputMediaPhoto(
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
                    )
                ),
                reply_markup=kb
            )


@router.callback_query(F.data.startswith('generate_skip_10'))
async def generate_skip_10(callback: CallbackQuery, bot: Bot) -> None:
    user_id = callback.from_user.id
    page = int(callback.data.split('_')[3])
    leaf = int(callback.data.split('_')[4])

    try:
        async with aiofiles.open(f'wbs_{str(user_id)}.json', 'r', encoding='utf-8') as file:
            content = await file.read()
            files = json.loads(content)
    except FileNotFoundError:
        await callback.answer('Please enter a new request')
        return

    if page < len(files):
        try:
           item = files[page + 10]
           kb = await generate_parser_kb(user_id=user_id, page=page + 10, leaf=leaf)
        except IndexError:
            item = files[len(files) - 1]
            kb = await generate_parser_kb(user_id=user_id, page=len(files) - 1, leaf=leaf)
        category = "18+" if item["is_adult"] else "0+"

        path = os.path.join('parser_core', 'photo_error', 'img.jpg')

        try:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=(
                    InputMediaPhoto(
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
                    )
                ),
                reply_markup=kb
            )
        except (TelegramBadRequest, TelegramNetworkError):
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=(
                    InputMediaPhoto(
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
                    )
                ),
                reply_markup=kb
            )