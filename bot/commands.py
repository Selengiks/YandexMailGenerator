import bot.yandex_api as yapi
import config as cfg
from aiogram import md, types
from loguru import logger
from support.bots import dp, bot
from transliterate import translit
import bot.keyboard as kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

logger.debug("Bot commands module loaded")

sudo = cfg.superadmins
with open("admins.txt", "r") as admins:
    admin_id = admins.readlines()

"""====================    FSM     ===================="""


class FSM(StatesGroup):  # FSM for edit user info
    primary = State()  # main state of the bot
    edit_user_main = State()  # state for edit_user command
    edit_user_full_name = State()  # nested state for edit_user_main
    user_list = State()


"""====================    Commands via inline buttons     ===================="""


@dp.callback_query_handler(
    lambda c: c.data,
    state=FSM.primary,
    user_id=admin_id
)
async def process_callback_commands(callback_query: types.CallbackQuery):  # main method for processing callbacks
    code = callback_query.data

    if code == '/users':
        await bot.answer_callback_query(callback_query.id, text='users')
        await AdminLayer.users(callback_query.message)

    elif code == '/get_user ':
        await bot.answer_callback_query(callback_query.id, text='Получение информации...')

    elif code == '/add_user ':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/edit_user ':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/del_user ':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/help':
        await bot.answer_callback_query(callback_query.id, text='/help')
        await AdminLayer.help(callback_query.message)

    elif code == '/support':
        await bot.answer_callback_query(callback_query.id, text='/support')

    else:
        await bot.answer_callback_query(callback_query.id)

    logger.debug(f'Нажата инлайн кнопка! code= {code}')


"""====================    Bot control layer     ===================="""


@dp.message_handler(
    user_id=sudo,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.primary,
    commands="set_admin"
)
async def set_admin(message: types.Message):  # set access to bot commands for telegram users
    user_id = message.text.split()[1]
    setAdmin = message.text.split()[2]

    try:
        if setAdmin == "True":
            await add_admin(user_id)
        else:
            await del_admin(user_id)

        result = f'Права юзера {md.hcode(user_id)} в боте изменены.\n'

    except (Exception,):
        result = f'Случилась ошибка при попытке выполнить {message.get_command()} {message.get_args()}\n\n' \
                 'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

    await message.reply(result)


@dp.message_handler(
    state='*',
    commands='cancel',
    user_id=admin_id
)
async def cancel_handler(message: types.Message, state: FSMContext):  # allow user to cancel any action

    current_state = await state.get_state()
    if current_state is None:
        return

    logger.debug(f'Return to primary state')
    await FSM.primary.set()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


"""====================    Only sudo/admins commands     ===================="""


class AdminLayer:

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        state=FSM.primary,
        commands="set_role"
    )
    async def set_role(self: types.Message):  # change users rights on yandex

        user_id = self.text.split()[1]
        setAdmin = self.text.split()[2]

        payload = {
            'isAdmin': setAdmin
        }

        user = yapi.get_user(user_id)
        yapi.edit_user(user_id, payload)

        try:
            result = f'Права юзера {md.hcode(user["json"]["id"])} - ' \
                     f'{user["json"]["name"]["first"]} {user["json"]["name"]["last"]} изменены!\n'

        except (Exception,):
            logger.debug(f'Code: {user["response"].status_code}. Content: {user["response"].content}')
            result = f'Случилась ошибка при попытке выполнить {self.get_command()} {self.get_args()}\n\n' \
                     'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

        logger.debug(f'Code: {user["response"].status_code}. Content: {user["response"].content}')
        await self.reply(result)

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        state=FSM.primary,
        commands="users"
    )
    async def users(self: types.Message):  # return all users on yandex

        users = yapi.users()
        logger.debug(f'Всего сотрудников: {len(users)}')
        result = ""
        num = 1

        for key, value in users.items():
            result += f'#: {num}\nID: {md.hcode(key)}\nИмя: {md.hcode(users[key]["name"]["first"])}\n' \
                      f'Фамилия: {md.hcode(users[key]["name"]["last"])}\n' \
                      f'Почта: {md.hcode(users[key]["email"])}\nАдминистратор: {users[key]["isAdmin"]}\n\n'
            num += 1
            if len(result) > 3900:
                await self.answer(result)
                result = ""
        await self.answer(result)

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        state=FSM.primary,
        commands="add_user"
    )
    async def add_user(self: types.Message):  # add new user on yandex

        try:
            first = translit(str(self.text.split()[1]), "ru", reversed=True)
            last = translit(str(self.text.split()[2]), "ru", reversed=True)
            user = yapi.add_user(first, last)

            if not user:
                result = f'Пользователь с именем {first}, и фамилией {last} - существует.\n' \
                         f'Попробуй команду {md.hcode(f"/get_user {first} {last}")}'
            else:
                result = f'Пользователь {self.text.split(" ")[1]} {self.text.split(" ")[2]} успешно добавлен\n\n' \
                         f'Данные:\nИмя: {first}\nФамилия: {last}\n' \
                         f'Почта: {md.hcode(user["user"][0] + "@traffbraza.com")}\nПароль: {md.hcode(user["user"][1])}'

        except (Exception,):
            result = f'Случилась ошибка при попытке выполнить {self.get_command()} {self.get_args()}\n\n' \
                     'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

        await self.reply(result)

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        state=FSM.primary,
        commands="edit_user"
    )
    async def edit_user(self: types.Message, state: FSMContext):  # edit selected users info

        try:
            user_id = self.text.split()[1]
            user = yapi.get_user(user_id)

            if not user:  # check if user exsist
                result = f'Пользователь с user_id {user_id} - не существует.\n' \
                         f'Попробуй команду {md.hcode(f"/get_user {user_id}")}, чтобы удостовериться.'

            else:
                async with state.proxy() as data:
                    data['user_id'] = user_id
                await FSM.edit_user_main.set()
                result = (f'Введи, что ты хочешь изменить:\nfull_name - изменить имя и фамилию\n'
                          f'password - сгенерировать новый пароль\nИли введи /cancel чтобы отменить операцию.')

        except (Exception,):
            result = f'Случилась ошибка при попытке выполнить {self.get_command()} {self.get_args()}\n\n' \
                     'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

        await self.reply(result)

    @dp.message_handler(
        state=FSM.edit_user_main,
        user_id=admin_id
    )
    async def process_mode(self: types.Message, state: FSMContext):  # process mode for edit_user

        async with state.proxy() as data:
            data['mode'] = self.text
        try:
            if data['mode'] == 'full_name':
                await FSM.edit_user_full_name.set()
                await self.reply('Введи новое имя и фамилию')

            elif data['mode'] == 'password':
                password = yapi.create_random_password()
                payload = {
                    'password': password
                }
                res = yapi.edit_user(data['user_id'], payload)
                result = f'Пароль пользователя {md.hcode(data["user_id"])} - изменён. Пароль - {md.hcode(password)}'
                logger.debug(f'Code: {res["response"].status_code}. Content: {res["response"].content}')
                await FSM.primary.set()
                await self.answer(result)
            else:
                raise Exception

        except (Exception,):
            result = f'Случилась ошибка при попытке выполнить {self.get_command()} {self.get_args()}\n\n' \
                     'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'
            await self.reply(result)

    @dp.message_handler(
        state=FSM.edit_user_full_name,
        user_id=admin_id
    )
    async def process_full_name(self: types.Message, state: FSMContext):  # process user first and last name

        payload = {
            "name": {
                "first": self.text.split()[0],
                "last": self.text.split()[1]
            }
        }

        async with state.proxy() as data:
            res = yapi.edit_user(data['user_id'], payload)

            result = f'Информация пользователя {md.hcode(data["user_id"])} - была обновлена.\n' \
                     f'Проверь командой /get_user {data["user_id"]}'
            logger.debug(f'Code: {res["response"].status_code}. Content: {res["response"].content}')
            await FSM.primary.set()

        await self.answer(result)

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        state=FSM.primary,
        commands="del_user"
    )
    async def del_user(self: types.Message):  # delete user from yandex

        try:
            user_id = self.text.split()[1]
            user = yapi.get_user(user_id)

            if not user:
                result = f'Пользователь с user_id {user_id} - не существует.\n' \
                         f'Попробуй команду {md.hcode(f"/get_user {user_id}")}, чтобы удостовериться.'
            else:

                if user["json"]["isAdmin"]:
                    result = f'Пользователь {md.hcode(user_id)} имеет права администратора, и не может быть удалён'

                else:
                    res = yapi.del_user(user_id)
                    logger.debug(f'Code: {res["response"].status_code}. Content: {res["response"].content}')
                    result = f'Пользователь {md.hcode(user_id)} - успешно удалён.\n Проверь командой get_user {user_id}'

        except (Exception,):
            result = f'Случилась ошибка при попытке выполнить {self.get_command()} {self.get_args()}\n\n' \
                     'Удостовертесь что команда выполнена правильно.\n\nСправка: /help'

        await self.reply(result)

    @dp.message_handler(
        user_id=admin_id,
        chat_type=[types.ChatType.PRIVATE],
        state="*",
        commands="help"
    )
    async def help(self: types.Message):
        result = f"Справка по использованию бота\n\n" \
                 f"{md.hbold('Посмотреть список всех сотрудников')} - /users\n" \
                 f"Команда выводит сотрудников, их id, имя, фамилию, почту и статус (Администратор/Пользователь)\n\n" \
                 f"{md.hbold('Посмотреть конкретного пользователя')} - /get_user [params]\n" \
                 f"[params] - варианты, как можно отобразить сотрудника:\n" \
                 f"ID - Идентификатор можно узнать, посмотрев список всех сотрудников (/users), пункт ID\n" \
                 f"MAIL - почта сотрудника, если известно\n" \
                 f"NAME SURNAME - поиск по имени и фамилии. Порядок имени и фамилии обязателен, возможен поиск " \
                 f"транслитом, вот примеры ввода:\n/get_user Пупа Лупович, /get_user Pupa Lupovich\n\n" \
                 f"{md.hbold('Добавить пользователя')} - /add_user ИМЯ ФАМИЛИЯ\n" \
                 f"Создаёт почту на заданное имя и фамилию человека. " \
                 f"Внимание, имя фамилия автоматичеки транслитерируются, порядок ввода имени и фамилии важен!\n\n" \
                 f"{md.hbold('Удалить пользователя')} - /del_user ID\n" \
                 f"Удаляет пользователя по ID (во избежания случайнойстей)\n\n" \
                 f"{md.hbold('Изменить данные пользователя')} - /edit_user ID\n" \
                 f"Включает режим редактирования юзера. Следуйте инструкциям бота при включении этого режима.\n\n" \
                 f"{md.hbold('Изменить права пользователя')} - /set_role ID ROLE\n" \
                 f"Позволяет назначить пользователя администратором, или сделать пользователем\n" \
                 f"Role:\n" \
                 f"True - делает его администратором\n" \
                 f"False - снимает права администратора\n" \
                 f"Пример: /set_role 0000000000 True - назначает пользователя 0000000000 администратором\n"

        await self.answer(result)


"""====================     Commands for all users     ===================="""


class UserLayer:

    @dp.message_handler(
        chat_type=[types.ChatType.PRIVATE],
        state="*",
        commands="get_user"
    )
    async def get_user(self: types.Message):  # return info about user

        if len(self.text.split()) == 2:
            param1 = self.text.split()[1]
            user = yapi.get_user(param1)

        elif len(self.text.split()) == 3:
            param1 = self.text.split()[1]
            param2 = self.text.split()[2]
            user = yapi.get_user(translit(param1, "ru", reversed=True), translit(param2, "ru", reversed=True))

        else:
            raise Exception

        try:
            result = f'Пользователь {md.hcode(user["json"]["id"])}\n' \
                     f'Имя: {user["json"]["name"]["first"]}\nФамилия: {user["json"]["name"]["last"]}\n' \
                     f'Почта: {md.hcode(user["json"]["email"])}\nАдминистратор: {user["json"]["isAdmin"]}'

        except (Exception,):
            logger.debug(f'Code: {user["response"].status_code}. Content: {user["response"].content}')
            result = f'Случилась ошибка при попытке выполнить {self.get_command()} {self.get_args()},' \
                     f' или юзера не существует.\n\nУдостовертесь что команда выполнена правильно.\n\nСправка: /help'

        logger.debug(f'Code: {user["response"].status_code}. Content: {user["response"].content}')
        await self.reply(result)


"""====================   Some service methods for   ===================="""


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    state="*",
    commands="start",
    user_id=admin_id
)
async def main_menu(message: types.Message):  # bot main menu, and start method
    await FSM.primary.set()
    botinfo = await dp.bot.me
    await message.reply(f'{botinfo.full_name} [{md.hcode(f"@{botinfo.username}")}] на связи!\n\n'
                        f'{md.hbold("Менеджмент происходит через команды во избежание ошибок! Смотрите справку")}\n\n'
                        f'Главное меню (WIP):',
                        reply_markup=kb.inline_menu)


@dp.message_handler(
    state=FSM.primary
)
async def echo(message: types.Message):  # for unrecognized commands or user random input
    result = f'Неопознанная команда\n\n{message.text}'
    await message.answer(result)


async def add_admin(user_id):  # add telegram user to bot admins
    with open(cfg.filename, "a+") as f:
        f.write(f'{user_id}\n')


async def del_admin(user_id):  # delete telegram user from bot admins
    with open(cfg.filename, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != f'{user_id}\n':
                f.write(i)
        f.truncate()


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.primary,
    commands="sukablyatebuchayaklava"
)
async def del_keyb(message: types.Message):  # for delete fucking reply keyboard, if you failed due experiments
    delete = types.ReplyKeyboardRemove(True)
    await message.answer(f'Done', reply_markup=delete)
