import random
import string
from collections import OrderedDict
import re

import requests
import config as cfg

HEADERS = {
    'Authorization': 'OAuth ' + cfg.API_TOKEN,
    'User-Agent': 'TBMailBot Agent',
}

PATTERN = re.compile('[A-Za-z0-9._%+-]+@traffbraza\.com')

user_list = OrderedDict()


def users():
    params = {
        'per_page': 1000,
    }

    response = requests.get(
        f'https://api360.yandex.net/directory/v1/org/{cfg.ORG_ID}/users/',
        params=params,
        headers=HEADERS,
        proxies=cfg.PROXIES,
        timeout=10,
    ).json()

    for x in response['users']:
        user_list[x['id']] = {'nickname': x['nickname'], 'email': x['email'], 'password': None,
                              'name': {'first': x['name']['first'], 'last': x['name']['last']},
                              'isAdmin': x['isAdmin'], 'createdAt': x['createdAt'], 'updatedAt': x['updatedAt']}

    return user_list


def get_user(datatype, *args):
    param = ""

    if datatype == 'int':
        param = args[0]

    else:
        if PATTERN.match(args[0]):
            userId = 0
            data = users()

            for key, value in data.items():
                if value['email'] == args[0]:
                    userId = key

            param = userId

        elif len(args) > 1:
            userId = 0
            data = users()

            for key, value in data.items():
                if value['name']['first'] == args[0] and value['name']['last'] == args[1]:
                    userId = key

            param = userId

    response = requests.get(
        f'https://api360.yandex.net/directory/v1/org/{cfg.ORG_ID}/users/{param}',
        headers=HEADERS,
        proxies=cfg.PROXIES,
        timeout=10
    ).json()

    return response


def add_user(first, last):
    nickname = f'{first.lower()}.{last.lower()}'
    password = create_random_password()

    payload = {
        'department_id': 1,
        'name': {'first': first, 'last': last},
        'nickname': nickname,
        'password': password,
    }

    response = requests.post(
        'https://api.directory.yandex.net/v6/users/',
        json=payload,
        headers=HEADERS,
        proxies=cfg.PROXIES,
        timeout=10,
    ).json()

    out = {'response': response, 'user': [nickname, password]}

    return out


def del_user(id):
    data = get_user('int', id)

    response = requests.delete(
        f'https://api360.yandex.net/directory/v1/org/{cfg.ORG_ID}/users/{data["id"]}',
        headers=HEADERS,
        proxies=cfg.PROXIES,
        timeout=10
    ).json()

    return response


def edit_user(id, payload):
    data = get_user('int', id)

    params = payload

    response = requests.patch(
        f'https://api360.yandex.net/directory/v1/org/{cfg.ORG_ID}/users/{data["id"]}',
        params=params,
        headers=HEADERS,
        proxies=cfg.PROXIES,
        timeout=10
    ).json()

    return response


def create_random_password(length=12):
    symbols = string.ascii_letters + string.digits
    return ''.join(
        random.choice(symbols)
        for _ in range(length)
    )
