import json
from typing import Union

import aiofiles
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def generate_parser_kb(user_id: int, page: int, leaf: Union[int, None] = None):
    async with aiofiles.open(f'wbs_{user_id}.json', 'r', encoding='utf-8') as file:
        content = await file.read()
    data = json.loads(content)

    if isinstance(data, list) and len(data) > 0:
        data.pop(0)

    all_page = len(data)
    page = page

    inline = []
    button_all_pages = InlineKeyboardButton(text=f'[{page}/{all_page}]', callback_data='generate_page_counter')
    button_back_pages = InlineKeyboardButton(text=f'<<< Previous page', callback_data=f'generate_back_page_{page}_{leaf if leaf is not None else 0}')
    button_next_pages = InlineKeyboardButton(text=f'Next page >>>', callback_data=f'generate_next_page_{page}_{leaf if leaf is not None else 0}')
    skip_10 = InlineKeyboardButton(text='[Skip 10 pages]', callback_data=f'generate_skip_10_{page}_{leaf if leaf is not None else 0}')
    next_paragraph = InlineKeyboardButton(text='Next paragraph >>', callback_data=f'generate_next_paragraph_{page}_{leaf if leaf is not None else 0}')
    previous_paragraph = InlineKeyboardButton(text='<< Previous paragraph', callback_data=f'generate_previous_paragraph_{page}_{leaf if leaf is not None else 0}')


    if page == 1 or page % 100 == 1:
        inline.append([button_all_pages, button_next_pages])
        inline.append([skip_10])
        if page % 100 == 1 and page > 100:
            inline.append([previous_paragraph, next_paragraph])
        elif len(data) < 100:
            pass
        else:
            inline.append([next_paragraph])
    elif page > 1 and page % 100 != 0:
            inline.append([button_back_pages, button_all_pages, button_next_pages])
            inline.append([skip_10])
            if page < 99:
                inline.append([next_paragraph])
            elif page >= 99:
                inline.append([previous_paragraph, next_paragraph])
    elif page % 100 == 0:
        inline.append([button_back_pages, button_all_pages])
        inline.append([next_paragraph])

    keyboard = InlineKeyboardMarkup(inline_keyboard=inline)
    return keyboard