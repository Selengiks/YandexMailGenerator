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
    pass


"""====================    Admin level     ===================="""


class AdminLevel:
    pass


"""====================     User level     ===================="""


class UserLevel:

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="start"
    )
    async def send_welcome(message: types.Message):
        botinfo = await dp.bot.me
        await message.reply(f'Привет, я {botinfo.full_name}\n')

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="profile"
    )
    async def get_userinfo(message: types.Message):
        result = None
        user = {"id": int(), "name": None, "username": None, "role": None, "mail": None, "password": None}
        for ent in message.entities:
            if ent.type == MessageEntityType.TEXT_MENTION:  # for user without username
                user_db = await call_db(message, "id", ent.user.id)
                result = await user_check(message, user_db._id)
                user["id"] = user_db._id
                user["name"] = user_db.name
                user["username"] = "no username"
                user["role"] = user_db.role
                user["mail"] = user_db.mail
                user["password"] = user_db.password

            if ent.type == MessageEntityType.MENTION:  # for user with username
                search_user = message.text.split(" ")[1]
                user_db = await call_db(message, "username", search_user)
                result = await user_check(message, user_db._id)
                user["id"] = user_db._id
                user["name"] = user_db.name
                user["username"] = user_db.username
                user["role"] = user_db.role
                user["mail"] = user_db.mail
                user["password"] = user_db.password

        if result is None:
            await message.reply("Пользователь не найден")
            return False

        elif result:
            if message.from_user.id in cfg.superadmins:
                await message.reply(f'Id: {md.hcode(user["id"])}\nName: {md.hcode(user["name"])}\n'
                                    f'Username: {md.hcode(user["username"])}\nRole: {md.hcode(user["role"])}\n'
                                    f'Mail: {md.hcode(user["mail"])}\nPassword: {md.hcode(user["password"])}')

            elif message.from_user.id in cfg.admins:
                await message.reply(f'Id: {md.hcode(user["id"])}\nName: {md.hcode(user["name"])}\n'
                                    f'Username: {md.hcode(user["username"])}\nRole: {md.hcode(user["role"])}\n'
                                    f'Mail: {md.hcode(user["mail"])}\nPassword: {md.hcode(user["password"])}')

            else:
                user_db = await call_db(message, "_id", message.from_user.id)
                if message.text.split(" ")[1] == user_db.username:
                    await message.reply(f'Id: {md.hcode(user["id"])}\nName: {md.hcode(user["name"])}\n'
                                        f'Username: {md.hcode(user["username"])}\nRole: {md.hcode(user["role"])}\n'
                                        f'Mail: {md.hcode(user["mail"])}\nPassword: {md.hcode(user["password"])}')
                else:
                    await message.reply(f'Id: {md.hcode(user["id"])}\nName: {md.hcode(user["name"])}\n'
                                        f'Username: {md.hcode(user["username"])}\nRole: {md.hcode(user["role"])}\n')
            return False

        else:
            await message.reply("get_userinfo return None")
            return False

    @dp.message_handler()
    async def echo(message: types.Message):
        await message.answer(message.text)


"""====================   Service level    ===================="""


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
        return "Нельзя трогать няшку"
    if id in cfg.admins:
        return "Нельзя трогать админа"
    else:
        return "Юзера трогать можно"
