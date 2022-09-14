from aiogram import md, types
from loguru import logger

from support.bots import dp

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    is_reply=False,
    commands="help",
    commands_prefix="!"
)
async def help(message: types.Message):
    await message.answer('Help command')