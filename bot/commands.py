import bot.yandex_api as yapi
import config as cfg
from aiogram import md, types
from loguru import logger
from support.bots import dp
from transliterate import translit

logger.debug("Bot commands module loaded")

"""====================    Admin layer     ===================="""


class AdminLayer:

    admin_id = cfg.admins

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        commands="set_role"
    )
    async def set_role(self: types.Message):

        id = self.text.split(" ")[1]
        setAdmin = self.text.split(" ")[2]

        payload = {
            'isAdmin': setAdmin
        }

        user = yapi.get_user_by_id(id)
        yapi.edit_user(id, payload)

        try:
            result = f'Права юзера {md.hcode(user["id"])} - {user["name"]["first"]} {user["name"]["last"]} изменены!\n'

        except Exception:
            result = f'Случилась ошибка при попытке выполнить /set_role {id}\n\n' \
                     'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

        await self.reply(result)

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        commands="users"
    )
    async def users(self: types.Message):

        users = yapi.users()
        result = ""
        c = 1

        for key, value in users.items():
            result += f'#: {c}\nID: {md.hcode(key)}\nИмя: {md.hcode(users[key]["name"]["first"])}\n' \
                      f'Фамилия: {md.hcode(users[key]["name"]["last"])}\n' \
                      f'Почта: {md.hcode(users[key]["email"])}\nАдминистратор: {md.hcode(users[key]["isAdmin"])}\n\n'

            c += 1

            if c % 15 == 0:  # сколько юзеров выводить в одном сообщении. Больше 15 не рекомендую, может не всех вывести
                await self.answer(result)
                result = ""

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        commands="add_user"
    )
    async def add_user(self: types.Message):

        try:
            first = translit(str(self.text.split(" ")[1]), "ru", reversed=True)
            last = translit(str(self.text.split(" ")[2]), "ru", reversed=True)
            user = yapi.add_user(first, last)

            result = f'Пользователь {self.text.split(" ")[1]} {self.text.split(" ")[2]} успешно добавлен\n\n' \
                     f'Данные:\nИмя: {first}\nФамилия: {last}\n' \
                     f'Почта: {md.hcode(user["user"][0])}\nПароль: {md.hcode(user["user"][1])}'

        except Exception:
            result = 'Случилась ошибка при попытке выполнить /add_user {Имя} {Фамилия}\n\n' \
                     'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

        await self.reply(result)

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        commands="edit_user"
    )
    async def edit_user(self):
        pass

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        commands="del_user"
    )
    async def del_user(self: types.Message):

        id = self.text.split(" ")[1]
        user = yapi.get_user_by_id(id)

        try:
            if user["isAdmin"] == True:
                result = f'Пользователь {md.hcode(id)} имеет права администратора, и не может быть удалён'

            else:
                yapi.del_user(id)
                result = f'Пользователь {md.hcode(id)} - успешно удалён'

        except Exception:
            result = f'Случилась ошибка при попытке выполнить /del_user {id}\n\n' \
                     'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

        await self.reply(result)


"""====================     User layer     ===================="""


class UserLayer:

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="get_user"
    )
    async def get_user(self: types.Message):

        id = self.text.split(" ")[1]
        user = yapi.get_user_by_id(id)

        try:

            result = f'Пользователь {md.hcode(self.text.split(" ")[1])}\n' \
                     f'Имя: {user["name"]["first"]}\nФамилия: {user["name"]["last"]}\n' \
                     f'Почта: {md.hcode(user["email"])}\nАдминистратор: {user["isAdmin"]}'

        except Exception:
            result = f'Случилась ошибка при попытке выполнить /get_user {id}\n\n' \
                     'Удостовертесь что команда выполнена в виде  /get_user ID\n\nСправка: /help'

        await self.reply(result)


"""====================   Service layer    ===================="""


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    commands="start"
)
async def send_welcome(message: types.Message):
    botinfo = await dp.bot.me
    await message.reply(f'На связи {botinfo.full_name}\n\nСправка по командам: /help')


@dp.message_handler()
async def echo(message: types.Message):
    result = f'Неопознанная команда\n\n{message.text}'
    await message.answer(result)