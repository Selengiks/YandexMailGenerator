from aiogram import md, types

from support.bots import dp


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    is_reply=False,
    commands="help",
    commands_prefix="!"
)
async def help(message: types.Message):
    await message.answer('Help command')