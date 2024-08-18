from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from parser_core.inline_keyboard.start_kb import start_kb

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.clear()
    nickname = message.from_user.full_name if message.from_user.full_name else message.from_user.username
    kb = await start_kb()
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'🤩 Hello, {nickname}!\n\n'
             f'A bot that can search for products on wildberries, '
             f'display pictures, links and save the product to your favorites!\n\n'
             f'There is also a search by article!',
        reply_markup=kb
    )


@start_router.callback_query(F.data == 'menu_kb')
async def start_callback(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await state.clear()
    nickname = callback.message.from_user.full_name if callback.message.from_user.full_name else callback.message.from_user.username
    kb = await start_kb()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f'🤩 Hello, {nickname}!\n\n'
             f'A bot that can search for products on wildberries, '
             f'display pictures, links and save the product to your favorites!\n\n'
             f'There is also a search by article!',
        reply_markup=kb
    )