from loguru import logger
from aiogram import Dispatcher, executor, types
from support.bots import dp, bot


from support.middleware import LoguruMiddleware
import bot

dp.middleware.setup(LoguruMiddleware())  # ALL LOGGING

@dp.errors_handler()
async def errors(update: types.Update, error: Exception):
    logger.warning(update)
    try:
        raise error
    except Exception as e:
        logger.exception(e)
    return True


async def on_startup(dp: Dispatcher):
    botinfo = await dp.bot.me
    logger.info(f"Бот {botinfo.full_name} [@{botinfo.username}] запущен")


async def on_shutdown(dp: Dispatcher):
    logger.warning('Выключаюсь..')
    await bot.close()


if __name__ == '__main__':
    logger.info("Режим бота - POLLING")
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)