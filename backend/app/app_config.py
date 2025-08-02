import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_URL = os.getenv("DATABASE_URL")
model = "o4-mini"
