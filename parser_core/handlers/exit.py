from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from parser_core.inline_keyboard.start_kb import start_kb
from parser_core.state.aricle_state import SearchArticle
from parser_core.state.search_state import SearchState

router = Router()


@router.message(Command('exit'), SearchArticle.search)
async def exit_handler(message: Message, bot: Bot, state: FSMContext):
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


@router.message(Command('exit'), SearchState.search)
async def exit_handler(message: Message, bot: Bot, state: FSMContext):
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