from loguru import logger
from aiogram import Bot, Dispatcher, executor, types

from support.dbmanager import mongo
from support.middleware import ClassicMiddleware, LoguruMiddleware

import config as cfg

# Initialize bot and dispatcher
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)

dp.middleware.setup(ClassicMiddleware())
dp.middleware.setup(LoguruMiddleware())  # ALL LOGGING

@dp.errors_handler()
async def errors(update: types.Update, error: Exception):
    logger.warning(update)
    try:
        raise error
    except Exception as e:
        logger.exception(e)
    return True


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


async def on_startup(dp: Dispatcher):
    botinfo = await dp.bot.me
    logger.info(f"Бот {botinfo.full_name} [@{botinfo.username}] запущен")


async def on_shutdown(dp: Dispatcher):
    logger.warning('Выключаюсь..')
    await mongo.close()
    await mongo.wait_closed()
    await bot.close()


if __name__ == '__main__':
    logger.info("Режим бота - POLLING")
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)