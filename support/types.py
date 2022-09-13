import datetime
from typing import Any, Dict, List, Tuple, Union

from support.dbmanager import mongo
from config import user_collection


class UserType(dict):
    """
    Объект пользователя
    """

    _id: int
    name: str
    username: Union[str, None]
    role: str
    language: str
    fsm: str
    update_counter: int
    to_pm: bool
    reg_date: datetime.datetime
    last_online: datetime.datetime

    def __init__(self, *args, **kwargs):
        super(UserType, self).__init__(*args, **kwargs)
        self.__dict__ = self

    async def save(self):
        db = mongo.get_db()
        await db[user_collection].replace_one({"_id": self._id}, self)

    async def reset_state(self, save=True):
        if self.fsm != str():
            self.fsm = str()
            if save:
                await self.save()