from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

"""=================================Main Menu Keyboard============================================="""

inline_btn_users = InlineKeyboardButton('Все сотрудники', callback_data='users')
inline_menu = InlineKeyboardMarkup(row_width=2).add(inline_btn_users)
inline_menu.add(InlineKeyboardButton('Найти сотрудника', switch_inline_query_current_chat='get_user '))
inline_btn_add = InlineKeyboardButton('Добавить сотрудника', switch_inline_query_current_chat='add_user ')
inline_btn_edit = InlineKeyboardButton('Изменить данные', switch_inline_query_current_chat='edit_user ')
inline_btn_del = InlineKeyboardButton('Удалить сотрудника', switch_inline_query_current_chat='del_user ')
inline_menu.add(inline_btn_add, inline_btn_edit, inline_btn_del)
inline_btn_help = InlineKeyboardButton('Справка', callback_data='help')
inline_btn_support = InlineKeyboardButton('Обратная связь', url='https://t.me/trapinfourdimensionalspacetime')
inline_menu.add(inline_btn_help, inline_btn_support)

"""================================================================================================"""

"""=================================Users list keyboard============================================="""

def create_btn_list(pages):
    inline_btn_list = InlineKeyboardMarkup()
    inline_btn_list.row_width = 5

"""================================================================================================"""