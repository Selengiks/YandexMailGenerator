from aiogram import Bot
from aiogram.bot.api import TELEGRAM_PRODUCTION, TelegramAPIServer
from aiogram.dispatcher import Dispatcher

import config as cfg

local_server = TELEGRAM_PRODUCTION
if cfg.local_server_url:
    local_server = TelegramAPIServer.from_base(cfg.local_server_url)
bot = Bot(token=cfg.TOKEN, validate_token=True, parse_mode="HTML", server=local_server)
dp = Dispatcher(bot)
