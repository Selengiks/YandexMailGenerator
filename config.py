from loguru import logger
from sys import stdout

logger.remove()
logger.add(stdout, colorize=True, format="<green>{time:DD.MM.YY H:mm:ss}</green> "
                                         "| <yellow><b>{level}</b></yellow> | <magenta>{file}</magenta> | <cyan>{"
                                         "message}</cyan>")

logger.debug("Bot connection establish")

with open("config_data.txt", "r") as locfile:
    lines = locfile.readlines()
    TOKEN = lines[0].strip()
    MONGO_URI = lines[1].strip()
    MONGO_DB = lines[2].strip()

# local_server_url = "http://127.0.0.1:8888"
local_server_url = None

mongo_uri = MONGO_URI
mongo_db = MONGO_DB
user_collection = "Users"

superadmins = [290522978]  # superadmins
admins = [570477907]  # admins

GLOBAL_DELAY = .09
