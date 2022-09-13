from loguru import logger
from sys import stdout

logger.remove()
logger.add(stdout, colorize=True, format="<green>{time:DD.MM.YY H:mm:ss}</green> "
                                         "| <yellow><b>{level}</b></yellow> | <magenta>{file}</magenta> | <cyan>{"
                                         "message}</cyan>")

with open("config_data.txt", "r") as locfile:
    TOKEN = locfile.readline()
    MONGO_URI = locfile.readline()
    MONGO_DB = locfile.readline()


# local_server_url = "http://127.0.0.1:8888"
local_server_url = None

mongo_uri = MONGO_URI
mongo_db = MONGO_DB
user_collection = "Users"

admins = [290522978]  # global admin

GLOBAL_DELAY = .09
