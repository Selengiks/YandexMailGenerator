from typing import Union

import config as cfg
from aiogram import md, types
from aiogram.types.message_entity import MessageEntityType
from loguru import logger
from support import ttypes
from support.bots import dp
from support.dbmanager import mongo

logger.debug("Bot commands module loaded")

"""====================  Superadmin level  ===================="""


class TrapLevel:

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="set_role"
    )
    async def set_role(self):
        pass


"""====================    Admin level     ===================="""


class AdminLevel:

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="list_user"
    )
    async def list_user(self):
        pass

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="add_used"
    )
    async def add_used(self):
        pass

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="edit_user"
    )
    async def edit_user(self):
        pass

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="del_user"
    )
    async def del_user(self):
        pass


"""====================     User level     ===================="""


class UserLevel:

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="profile"
    )
    async def get_userinfo(message: types.Message):
        sender = await user_check(message, message.from_user.id)
        target = None
        user = {"id": int(), "name": None, "username": None, "role": None, "mail": None, "password": None}
        if len(message.text.split(" ")) == 1:
            user_db = await call_db(message, "_id", message.from_user.id)
            target = await user_check(message, user_db._id)
            user["id"] = user_db._id
            user["name"] = user_db.name
            user["username"] = user_db.username
            user["role"] = user_db.role
            user["mail"] = user_db.mail
            user["password"] = user_db.password
        else:
            for ent in message.entities:
                if ent.type == MessageEntityType.TEXT_MENTION:  # for user without username
                    user_db = await call_db(message, "id", ent.user.id)
                    target = await user_check(message, user_db._id)
                    user["id"] = user_db._id
                    user["name"] = user_db.name
                    user["username"] = "no username"
                    user["role"] = user_db.role
                    user["mail"] = user_db.mail
                    user["password"] = user_db.password

                if ent.type == MessageEntityType.MENTION:  # for user with username
                    search_user = message.text.split(" ")[1]
                    user_db = await call_db(message, "username", search_user)
                    target = await user_check(message, user_db._id)
                    user["id"] = user_db._id
                    user["name"] = user_db.name
                    user["username"] = user_db.username
                    user["role"] = user_db.role
                    user["mail"] = user_db.mail
                    user["password"] = user_db.password

        if target is None:
            await message.reply("Пользователь не найден")
            return False

        elif sender == "superadmin" or sender == "admin":
            if len(message.text.split(" ")) == 1:
                key = "_id"
                search_user = message.from_user.id
            else:
                key = "username"
                search_user = message.text.split(" ")[1]
            user_db = await call_db(message, key, search_user)
            await message.reply(f'Id: {md.hcode(user_db._id)}\nName: {md.hcode(user_db.name)}\n'
                                f'Username: {md.hcode(user_db.username)}\nRole: {md.hcode(user_db.role)}\n'
                                f'Mail: {md.hcode(user_db.mail)}\nPassword: {md.hcode(user_db.password)}')

        elif sender == "user":
            user_db = await call_db(message, "_id", message.from_user.id)
            if len(message.text.split(" ")) == 1 or message.text.split(" ")[1] == user_db.username:
                user_db = await call_db(message, "_id", message.from_user.id)
                await message.reply(f'Id: {md.hcode(user_db._id)}\nName: {md.hcode(user_db.name)}\n'
                                    f'Username: {md.hcode(user_db.username)}\nRole: {md.hcode(user_db.role)}\n'
                                    f'Mail: {md.hcode(user_db.mail)}\nPassword: {md.hcode(user_db.password)}')
            elif message.text.split(" ")[1] is not user["username"]:
                user_db = await call_db(message, "username", message.text.split(" ")[1])
                await message.reply(f'Id: {md.hcode(user_db._id)}\nName: {md.hcode(user_db.name)}\n'
                                    f'Username: {md.hcode(user_db.username)}\nRole: {md.hcode(user_db.role)}\n')

        else:
            await message.reply("get_userinfo return None")
            return False


"""====================   Service level    ===================="""


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    commands="start"
)
async def send_welcome(message: types.Message):
    botinfo = await dp.bot.me
    await message.reply(f'Привет, я {botinfo.full_name}\n')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


async def call_db(message: types.Message, key, value):
    db = mongo.get_db()
    db_users = db[cfg.user_collection]
    user_db = await db_users.find_one({key: value})
    if not user_db:
        await message.reply("Не знаю такого пользователя")
        return False
    user_db = ttypes.UserType(user_db)
    return user_db


async def user_check(message: types.Message, id: int) -> Union[str, bool]:
    if id in cfg.superadmins:
        return "superadmin"
    if id in cfg.admins:
        return "admin"
    else:
        return "user"
