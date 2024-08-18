from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



async def start_kb():
    buttons = [
        [
            InlineKeyboardButton(text='🔎 Search', callback_data='start_kb_search')
        ],
        [
            InlineKeyboardButton(text='😶‍🌫️ Search by article', callback_data='start_kb_search_by_article')
        ],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def menu_kb():
    buttons = [
        [
            InlineKeyboardButton(text='🔄️ Menu', callback_data='menu_kb')
        ],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard