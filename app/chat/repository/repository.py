
from typing import Any, List
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult

# from ..utils.security import hash_password


class ChatRepository:
    def __init__(self, database: Database):
        self.database = database
    