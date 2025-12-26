import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SYS_USER = os.getenv("SYS_USER")
    SYS_PASSWORD = os.getenv("SYS_PASSWORD")

settings = Settings()