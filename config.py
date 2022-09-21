import os

from loguru import logger
from sys import stdout
import config_data_priv

logger.remove()
logger.add(stdout, colorize=True, format="<green>{time:DD.MM.YY H:mm:ss}</green> "
                                         "| <yellow><b>{level}</b></yellow> | <magenta>{file}</magenta> | <cyan>{"
                                         "message}</cyan>")

logger.debug("Bot connection establish")

TOKEN = config_data_priv.BOT_TOKEN
API_TOKEN = config_data_priv.YANDEX_OAUTH_TOKEN
ORG_ID = config_data_priv.ORG_ID
PROXIES = config_data_priv.PROXIES

# local_server_url = "http://127.0.0.1:8888"
local_server_url = None

superadmins = ['290522978']  # Глобальные админы

filename = "admins.txt"
with open(filename, "a+") as admins:
    if os.path.exists("admins.txt") and os.path.getsize("admins.txt") > 0:
        logger.debug(f'Файл {filename} существует, администраторы загружены.')
    else:
        logger.debug(f'Файл {filename} не существует, потому был создан и заполнен.')
        for i in superadmins:
            admins.write(i + "\n")




GLOBAL_DELAY = .09
