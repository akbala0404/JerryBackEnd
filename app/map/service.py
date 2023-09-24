from app.config import database
from pydantic import BaseSettings
# from .adapters.here_service import HereService
from .repository.repository import MapRepository
from .adapters.map_service import MapService
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config(BaseSettings):
    HERE_API_KEY: str


class Service:
    def __init__(self, repository: MapRepository):
        # config = Config()        
        self.repository = repository
        self.map_service = MapService(os.environ.get("GOOGLE_MAPS_API_KEY"))


def get_service():
    repository = MapRepository(database)
    return Service(repository)
