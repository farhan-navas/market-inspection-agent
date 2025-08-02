import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:

    def __init__(self):
        self.MODEL = "o4-mini"
        
        self.DB_CONNECTION_URL = os.getenv("DATABASE_URL")

config = AppConfig()