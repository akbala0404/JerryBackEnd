from datetime import datetime

# from typing import Optional
from bson.objectid import ObjectId
from pymongo.database import Database


class PostRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, input: dict):
        payload = {
            "address": input["address"],
            "name": input["name"],
            "lat": input["lat"],
            "lng": input["lng"],
            "created_at": datetime.utcnow(),
            "user_id": ObjectId(input["user_id"])
        }

        self.database["history"].insert_one(payload)

    def get_posts(self, user_id: str, page: int, page_size: int):
        # Calculate the offset based on the page and page_size
        offset = (page - 1) * page_size

        # Create a filter to retrieve posts only for the specified user_id
        filter_query = {"user_id": ObjectId(user_id)}

        total_count = self.database["history"].count_documents(filter_query)

        cursor = self.database["history"].find(filter_query).skip(offset).limit(page_size).sort("created_at")

        result = list(cursor)

        return {
            "total": total_count,
            "objects": result
        }
