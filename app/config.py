import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    LLM_API_KEY = os.getenv("LLM_API_KEY")

