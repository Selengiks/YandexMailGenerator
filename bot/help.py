from aiogram import md, types

from support.bots import dp


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    commands="help"
)
async def help(message: types.Message):
    result = ""
    await message.answer(result)