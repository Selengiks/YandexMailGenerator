from aiogram import types
from loguru import logger
from support.bots import dp
from support.utils import get_args
from support.utils import is_command

logger.debug("Bot commands module loaded")

@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    commands="start",
    commands_prefix="!"
)
async def send_welcome(message: types.Message):
    botinfo = await dp.bot.me
    await message.reply(f'Привет, я {botinfo.full_name}\n')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
