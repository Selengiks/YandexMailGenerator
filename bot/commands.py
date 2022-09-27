import bot.yandex_api as yapi
import config as cfg
from aiogram import md, types
from loguru import logger
from support.bots import dp
from transliterate import translit

logger.debug("Bot commands module loaded")

"""====================    Admin layer     ===================="""

sudo = cfg.superadmins


# Хендлер и метод на добавление админов этого бота
@dp.message_handler(
    user_id=sudo,
    chat_type=[types.ChatType.PRIVATE],
    commands="set_admin"
)
async def set_admin(message: types.Message):
    id = message.text.split(" ")[1]
    setAdmin = message.text.split(" ")[2]

    try:
        if setAdmin == "True":
            await add_admin(id)
        else:
            await del_admin(id)

        result = f'Права юзера {md.hcode(id)} в боте изменены.\n'

    except Exception:
        result = f'Случилась ошибка при попытке выполнить /set_admin {message.get_args()}\n\n' \
                 'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

    await message.reply(result)


class AdminLayer:
    with open("admins.txt", "r") as admins:
        admin_id = admins.readlines()

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

        user = yapi.get_user(id)
        yapi.edit_user(id, payload)

        try:
            result = f'Права юзера {md.hcode(user["id"])} - {user["name"]["first"]} {user["name"]["last"]} изменены!\n'

        except Exception:
            result = f'Случилась ошибка при попытке выполнить /set_role {self.get_args()}\n\n' \
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

            if user == False:
                result = f'Пользователь с именем {first}, и фамилией {last} - существует.\n' \
                         f'Попробуй команду {md.hcode(f"/get_user {first} {last}")}'
            else:
                result = f'Пользователь {self.text.split(" ")[1]} {self.text.split(" ")[2]} успешно добавлен\n\n' \
                         f'Данные:\nИмя: {first}\nФамилия: {last}\n' \
                         f'Почта: {md.hcode(user["user"][0] + "@traffbraza.com")}\nПароль: {md.hcode(user["user"][1])}'

        except Exception:
            result = f'Случилась ошибка при попытке выполнить /add_user {self.get_args()}\n\n' \
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
        user = yapi.get_user(id)
        print(user)

        if user == False:
            result = f'Пользователь с id {id} - не существует.\n' \
                     f'Попробуй команду {md.hcode(f"/get_user {id}")}, чтобы удостовериться.'
        else:

            try:
                if user["isAdmin"] == True:
                    result = f'Пользователь {md.hcode(id)} имеет права администратора, и не может быть удалён'

                else:
                    yapi.del_user(id)
                    result = f'Пользователь {md.hcode(id)} - успешно удалён'

            except Exception:
                result = f'Случилась ошибка при попытке выполнить /del_user {self.get_args()}\n\n' \
                         'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

        await self.reply(result)


"""====================     User layer     ===================="""


class UserLayer:

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        commands="get_user"
    )
    async def get_user(self: types.Message):

        user = None

        if len(self.text.split(" ")) == 2:
            param1 = self.text.split(" ")[1]
            user = yapi.get_user(translit(param1, "ru", reversed=True))

        elif len(self.text.split(" ")) == 3:
            param1 = self.text.split(" ")[1]
            param2 = self.text.split(" ")[2]
            user = yapi.get_user(translit(param1, "ru", reversed=True), translit(param2, "ru", reversed=True))

        else:
            pass

        try:

            result = f'Пользователь {md.hcode(user["id"])}\n' \
                     f'Имя: {user["name"]["first"]}\nФамилия: {user["name"]["last"]}\n' \
                     f'Почта: {md.hcode(user["email"])}\nАдминистратор: {user["isAdmin"]}'

        except Exception:
            result = f'Случилась ошибка при попытке выполнить /get_user {self.get_args()},' \
                     f' или юзера не существует.\n\nУдостовертесь что команда выполнена правильно.\n\nСправка: /help'

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


async def add_admin(id):
    with open(cfg.filename, "a+") as f:
        f.writelines(id)


async def del_admin(id):
    with open(cfg.filename, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != id:
                f.write(i)
        f.truncate()
