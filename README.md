# Бот для управления корпоративными почтами сотрудников в Яндексе

## Установка:
> -pip install -r requirements.txt

### Так же для работы нужно переименовать файл config_data.txt в config_data_priv.txt, а также заполнить его необходимыми значениями

## На данный момент бот может:
### Вывести справку с командами 
> /help
### Выводить список сотрудников
### Добавлять\Удалять сотрудников
### Добавлять\убрать сотруднику роль администратора
### Посмотреть конкретного сотрудника по его id
### Возможность назначать/удалять новых администраторов бота через команду
> /set_admin 290522978 True
> 
> /set_admin 290522978 False