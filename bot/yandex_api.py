import json
import random
import string
from collections import OrderedDict
import re

import requests
import config as cfg

HEADERS = {
    'Authorization': 'OAuth ' + cfg.API_TOKEN,
    'User-Agent': 'TBMailBot Agent',
    'Content-Type': 'application/json'
}

PATTERN = re.compile(f'[A-Za-z0-9._%+-]+@traffbraza\.com')

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
        user_list[x['user_id']] = {'nickname': x['nickname'], 'email': x['email'], 'password': None,
                                   'name': {'first': x['name']['first'], 'last': x['name']['last']},
                                   'isAdmin': x['isAdmin'], 'createdAt': x['createdAt'], 'updatedAt': x['updatedAt']}
    return user_list


def get_user(*args):
    params = io(args)

    if type(params[0]) == int:
        param = params[0]

    else:
        if PATTERN.match(params[0]):
            userId = 0
            data = users()

            for key, value in data.items():
                if value['email'] == params[0]:
                    userId = key

            param = userId

        elif len(params) == 2:
            userId = 0
            data = users()

            for key, value in data.items():
                if value['name']['first'] == params[0] and value['name']['last'] == params[1]:
                    userId = key

            param = userId

        else:
            return False

    response = requests.get(
        f'https://api360.yandex.net/directory/v1/org/{cfg.ORG_ID}/users/{param}',
        headers=HEADERS,
        proxies=cfg.PROXIES,
        timeout=10
    ).json()

    return response


def add_user(first, last):
    data = users()

    for key, value in data.items():
        if first == value['name']['first'] and last == value['name']['last']:
            return False

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
    data = get_user(id)

    response = requests.delete(
        f'https://api360.yandex.net/directory/v1/org/{cfg.ORG_ID}/users/{data["user_id"]}',
        headers=HEADERS,
        proxies=cfg.PROXIES,
        timeout=10
    ).json()

    return response


def edit_user(id, payload):
    user_id = get_user(id)

    response = requests.patch(
        f'https://api.directory.yandex.net/v6/users/{user_id["user_id"]}',
        json=payload,
        headers=HEADERS,
        proxies=cfg.PROXIES,
        timeout=10
    )
    print(response.text)
    return response.json()


def create_random_password(length=12):
    symbols = string.ascii_letters + string.digits
    return ''.join(
        random.choice(symbols)
        for _ in range(length)
    )


def io(*args):
    output = []

    for p in args:
        for i in p:
            try:
                output.append(int(i))
            except ValueError:
                output.append(i)

    return output
