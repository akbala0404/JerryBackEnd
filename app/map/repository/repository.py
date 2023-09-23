from typing import Any, List
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


# from ..utils.security import hash_password


class MapRepository:
    def __init__(self, database: Database):
        self.database = database

# class Service:
#     def __init__(self, repository: MapRepository):
#         # config = Config()        
#         self.repository = repository
#         self.chat_service = ChatService(os.environ.get("OPEN_AI_KEY"))
#         # self.here_service = HereService(config.HERE_API_KEY)


# def get_service():
#     repository = ChatRepository(database)
#     return Service(repository)
