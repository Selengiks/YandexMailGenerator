import time
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

HANDLED_STR = ['Unhandled', 'Handled']


class LoguruMiddleware(BaseMiddleware):

    def __init__(self):
        self.logger = logger
        super(LoguruMiddleware, self).__init__()

    @staticmethod
    def check_timeout(obj):
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
        self.logger.info(f"Received message [ID:{message.message_id}] "
                         f"from [ID:{message.from_user.id}][@{message.from_user.username}] "
                         f"\nMessage body: {message.text}\nRaw: {message}")

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"message [ID:{message.message_id}] "
                          f"from [ID:{message.from_user.id}][@{message.from_user.username}]")

    async def on_pre_process_edited_message(self, edited_message, data: dict):
        self.logger.info(f"Received edited message [ID:{edited_message.message_id}] "
                         f"from [ID:{edited_message.from_user.id}][@{edited_message.from_user.username}]")

    async def on_post_process_edited_message(self, edited_message, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"edited message [ID:{edited_message.message_id}] "
                          f"from [ID:{edited_message.from_user.id}][@{edited_message.from_user.username}]")

    async def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        self.logger.info(f"Received inline query [ID:{inline_query.id}] "
                         f"from [ID:{inline_query.from_user.id}][@{inline_query.from_user.username}]")

    async def on_post_process_inline_query(self, inline_query: types.InlineQuery, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"inline query [ID:{inline_query.id}] "
                          f"from [ID:{inline_query.from_user.id}][@{inline_query.from_user.username}]")

    async def on_pre_process_chosen_inline_result(self, chosen_inline_result: types.ChosenInlineResult, data: dict):
        self.logger.info(f"Received chosen inline result [Inline msg ID:{chosen_inline_result.inline_message_id}] "
                         f"from [ID:{chosen_inline_result.from_user.id}][@{chosen_inline_result.from_user.username}] "
                         f"result [ID:{chosen_inline_result.result_id}]")

    async def on_post_process_chosen_inline_result(self, chosen_inline_result, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"chosen inline result [Inline msg ID:{chosen_inline_result.inline_message_id}] "
                          f"from [ID:{chosen_inline_result.from_user.id}][@{chosen_inline_result.from_user.username}] "
                          f"result [ID:{chosen_inline_result.result_id}]")

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        if callback_query.message:
            text = (f"Received callback query [ID:{callback_query.id}] "
                    f"from [ID:{callback_query.from_user.id}][@{callback_query.from_user.username}] "
                    f"for message [ID:{callback_query.message.message_id}] ")

            if callback_query.message.from_user:
                text += f"Original by [ID:{callback_query.message.from_user.id}][@{callback_query.from_user.username}]"

            self.logger.info(text)

        else:
            self.logger.info(f"Received callback query [ID:{callback_query.id}] "
                             f"from [ID:{callback_query.from_user.id}][@{callback_query.from_user.username}] "
                             f"for inline message [ID:{callback_query.inline_message_id}] ")

    async def on_post_process_callback_query(self, callback_query, results, data: dict):
        if callback_query.message:
            text = (f"{HANDLED_STR[bool(len(results))]} "
                    f"callback query [ID:{callback_query.id}] "
                    f"from [ID:{callback_query.from_user.id}][@{callback_query.from_user.username}] "
                    f"for message [ID:{callback_query.message.message_id}] ")

            if callback_query.message.from_user:
                text += f"Originally posted by [ID:{callback_query.message.from_user.id}]" \
                        f"[@{callback_query.message.from_user.username}]"

            self.logger.info(text)

        else:
            self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                              f"callback query [ID:{callback_query.id}] "
                              f"from [ID:{callback_query.from_user.id}][@{callback_query.from_user.username}]"
                              f"from inline message [ID:{callback_query.inline_message_id}]")

    async def on_pre_process_shipping_query(self, shipping_query: types.ShippingQuery, data: dict):
        self.logger.info(f"Received shipping query [ID:{shipping_query.id}] "
                         f"from [ID:{shipping_query.from_user.id}][@{shipping_query.from_user.username}]")

    async def on_post_process_shipping_query(self, shipping_query, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"shipping query [ID:{shipping_query.id}] "
                          f"from [ID:{shipping_query.from_user.id}][@{shipping_query.from_user.username}]")

    async def on_pre_process_pre_checkout_query(self, pre_checkout_query: types.PreCheckoutQuery, data: dict):
        self.logger.info(f"Received pre-checkout query [ID:{pre_checkout_query.id}] "
                         f"from [ID:{pre_checkout_query.from_user.id}][@{pre_checkout_query.from_user.username}]")

    async def on_post_process_pre_checkout_query(self, pre_checkout_query, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"pre-checkout query [ID:{pre_checkout_query.id}] "
                          f"from [ID:{pre_checkout_query.from_user.id}][@{pre_checkout_query.from_user.username}]")

    async def on_pre_process_error(self, update, error, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.info(f"Process update [ID:{update.update_id}]: [failed] (in {timeout} ms)")
