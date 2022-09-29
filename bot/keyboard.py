from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""=================================Main Menu Keyboard============================================="""

inline_btn_users = InlineKeyboardButton('Все сотрудники', callback_data='/users')
inline_menu = InlineKeyboardMarkup(row_width=2).add(inline_btn_users)
# for get, add, edit and del callback_data change to switch_inline_query_current_chat, or find other solution
inline_menu.add(InlineKeyboardButton('Найти сотрудника', callback_data='/get_user '))
inline_btn_add = InlineKeyboardButton('Добавить сотрудника', callback_data='/add_user ')
inline_btn_edit = InlineKeyboardButton('Изменить данные', callback_data='/edit_user ')
inline_btn_del = InlineKeyboardButton('Удалить сотрудника', callback_data='/del_user ')
inline_menu.add(inline_btn_add, inline_btn_edit, inline_btn_del)
inline_btn_help = InlineKeyboardButton('Справка', callback_data='/help')
inline_btn_support = InlineKeyboardButton('Если ничего не помогло', url='https://t.me/trapinfourdimensionalspacetime')
inline_menu.add(inline_btn_help, inline_btn_support)

"""================================================================================================"""

"""=================================Users list keyboard============================================="""

"""================================================================================================"""
