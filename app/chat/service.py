from app.config import database
from pydantic import BaseSettings
# from .adapters.here_service import HereService
from .repository.repository import ChatRepository
from .adapters.chat_service import ChatService
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class Config(BaseSettings):
    HERE_API_KEY: str


class Service:
    def __init__(self, repository: ChatRepository):
        # config = Config()        
        self.repository = repository
        self.chat_service = ChatService(os.environ.get("OPEN_AI_KEY"))
        # self.here_service = HereService(config.HERE_API_KEY)


def get_service():
    repository = ChatRepository(database)
    return Service(repository)
