import datetime as dt
import time
from typing import Union

import config as cfg
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ChatType as AioChatType
from loguru import logger

from support.dbmanager import mongo
from support.types import UserType

HANDLED_STR = ['Unhandled', 'Handled']


class ClassicMiddleware(BaseMiddleware):

    def __init__(self):
        super(ClassicMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = await self.validate(message)

        data["User"] = user

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        user = await self.validate(callback_query)

        data["User"] = user

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        pass

    async def validate(self, update: Union[types.Message, types.CallbackQuery]) -> UserType:

        if isinstance(update, types.CallbackQuery):
            User = update.from_user

        else:
            update: types.Message
            User = update.from_user

        if User.id == 777000 or User.is_bot:
            raise CancelHandler()

        user = await self.get_user(User, update)

        return user

    async def get_user(self, user: types.User, update: Union[types.Message, types.CallbackQuery]):
        db = mongo.get_db()
        db_users = db[cfg.user_collection]
        user_db = await db_users.find_one({"_id": user.id})
        to_pm = False

        if isinstance(update, types.CallbackQuery):
            if update.message.chat.type == AioChatType.PRIVATE:
                to_pm = True
        else:
            if update.chat.type == AioChatType.PRIVATE:
                to_pm = True

        if user_db:
            user_db = UserType(user_db)
            user_db.update_counter += 1
            user_db.last_online = dt.datetime.now()
            user_db.name = user.full_name
            user_db.username = user.username or None
            user_db.to_pm = to_pm
            await user_db.save()
            return user_db

        user_db = UserType()

        user_db._id = user.id
        user_db.name = user.full_name
        user_db.username = user.username or None
        # user_db.role = True if user.id in cfg.admins else False
        if user.id in cfg.superadmins:
            user_db.role = "Superadmin"
        elif user.id in cfg.admins:
            user_db.role = "Admin"
        else:
            user_db.role = "User"
        user_db.language = user.language_code
        user_db.fsm = str()
        user_db.update_counter = 1
        user_db.to_pm = to_pm
        user_db.reg_date = dt.datetime.now()
        user_db.last_online = dt.datetime.now()

        await db_users.insert_one(user_db)
        logger.debug(f"Новый пользователь {user_db.name} [{user_db._id}], role [{user_db.role}]")

        return user_db


class LoguruMiddleware(BaseMiddleware):

    def __init__(self):
        self.logger = logger
        super(LoguruMiddleware, self).__init__()

    def check_timeout(self, obj):
        start = obj.conf.get('_start', None)
        if start:
            del obj.conf['_start']
            return round((time.time() - start) * 1000)
        return -1

    async def on_pre_process_update(self, update: types.Update, data: dict):
        update.conf['_start'] = time.time()
        self.logger.debug(f"Received update [ID:{update.update_id}]")

    async def on_post_process_update(self, update: types.Update, result, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.info(f"Process update [ID:{update.update_id}]: [success] (in {timeout} ms)")

    async def on_pre_process_message(self, message: types.Message, data: dict):
        self.logger.info(f"Received message [ID:{message.message_id}] from user [ID:{message.from_user.id}]")

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"message [ID:{message.message_id}] from user [ID:{message.from_user.id}]")

    async def on_pre_process_edited_message(self, edited_message, data: dict):
        self.logger.info(f"Received edited message [ID:{edited_message.message_id}] "
                         f"from user [ID:{edited_message.from_user.id}]")

    async def on_post_process_edited_message(self, edited_message, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"edited message [ID:{edited_message.message_id}] "
                          f"from user [ID:{edited_message.from_user.id}]")

    async def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        self.logger.info(f"Received inline query [ID:{inline_query.id}] "
                         f"from user [ID:{inline_query.from_user.id}]")

    async def on_post_process_inline_query(self, inline_query: types.InlineQuery, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"inline query [ID:{inline_query.id}] "
                          f"from user [ID:{inline_query.from_user.id}]")

    async def on_pre_process_chosen_inline_result(self, chosen_inline_result: types.ChosenInlineResult, data: dict):
        self.logger.info(f"Received chosen inline result [Inline msg ID:{chosen_inline_result.inline_message_id}] "
                         f"from user [ID:{chosen_inline_result.from_user.id}] "
                         f"result [ID:{chosen_inline_result.result_id}]")

    async def on_post_process_chosen_inline_result(self, chosen_inline_result, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"chosen inline result [Inline msg ID:{chosen_inline_result.inline_message_id}] "
                          f"from user [ID:{chosen_inline_result.from_user.id}] "
                          f"result [ID:{chosen_inline_result.result_id}]")

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        if callback_query.message:
            text = (f"Received callback query [ID:{callback_query.id}] "
                    f"from user [ID:{callback_query.from_user.id}] "
                    f"for message [ID:{callback_query.message.message_id}] ")

            if callback_query.message.from_user:
                text += f" originally posted by user [ID:{callback_query.message.from_user.id}]"

            self.logger.info(text)

        else:
            self.logger.info(f"Received callback query [ID:{callback_query.id}] "
                             f"from user [ID:{callback_query.from_user.id}] "
                             f"for inline message [ID:{callback_query.inline_message_id}] ")

    async def on_post_process_callback_query(self, callback_query, results, data: dict):
        if callback_query.message:
            text = (f"{HANDLED_STR[bool(len(results))]} "
                    f"callback query [ID:{callback_query.id}] "
                    f"from user [ID:{callback_query.from_user.id}] "
                    f"for message [ID:{callback_query.message.message_id}] ")

            if callback_query.message.from_user:
                text += f" originally posted by user [ID:{callback_query.message.from_user.id}]"

            self.logger.info(text)

        else:
            self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                              f"callback query [ID:{callback_query.id}] "
                              f"from user [ID:{callback_query.from_user.id}]"
                              f"from inline message [ID:{callback_query.inline_message_id}]")

    async def on_pre_process_shipping_query(self, shipping_query: types.ShippingQuery, data: dict):
        self.logger.info(f"Received shipping query [ID:{shipping_query.id}] "
                         f"from user [ID:{shipping_query.from_user.id}]")

    async def on_post_process_shipping_query(self, shipping_query, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"shipping query [ID:{shipping_query.id}] "
                          f"from user [ID:{shipping_query.from_user.id}]")

    async def on_pre_process_pre_checkout_query(self, pre_checkout_query: types.PreCheckoutQuery, data: dict):
        self.logger.info(f"Received pre-checkout query [ID:{pre_checkout_query.id}] "
                         f"from user [ID:{pre_checkout_query.from_user.id}]")

    async def on_post_process_pre_checkout_query(self, pre_checkout_query, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"pre-checkout query [ID:{pre_checkout_query.id}] "
                          f"from user [ID:{pre_checkout_query.from_user.id}]")

    async def on_pre_process_error(self, update, error, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.info(f"Process update [ID:{update.update_id}]: [failed] (in {timeout} ms)")
