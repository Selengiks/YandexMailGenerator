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

admins = [290522978]  # admins

GLOBAL_DELAY = .09
