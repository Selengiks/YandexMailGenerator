from aiogram import md, types

from support.bots import dp


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    commands="help"
)
async def help(message: types.Message):

    result = f"Справка по использованию бота\n\n" \
             f"{md.bold('Посмотреть список всех сотрудников')} - /users\n" \
             f"Команда выводит всех сотрудников, их id, имя, фамилию, почту и статус (Администратор\Пользователь)\n" \
             f"{md.bold('Посмотреть конкретного пользователя')} - /get_user ID\n" \
             f"ID - идентификатор пользователя, который можно узнать, посмотрев список всех сотрудников\n" \
             f"{md.bold('Добавить пользователя')} - /add_user ИМЯ ФАМИЛИЯ\n" \
             f"Создаёт почту на заданное имя и фамилию человека. Внимание, порядок имени и фамилии при вводе важен!\n" \
             f"{md.bold('Удалить пользователя')} - /del_user ID\n" \
             f"Удаляет пользователя по его ID (во избежания проблем, связанных со схожей почтой или данными)\n" \
             f"{md.bold('Изменить пароль пользователя')} - /edit_user ID\n" \
             f"Изменяет пароль для выбранного пользователя. Пока не реализовано\n" \
             f"{md.bold('Изменить права пользователя')} - /set_role ID ROLE\n" \
             f"Позволяет назначить пользователя администратором, или сделать пользователем\n" \
             f"Role:\n" \
             f"True - делает его администратором\n" \
             f"False - снимает права администратора\n" \
             f"Пример: /set_role 0000000000 True - назначает пользователя 0000000000 администратором\n" \

    await message.answer(result)
