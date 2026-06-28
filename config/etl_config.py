import os
from dotenv import load_dotenv

load_dotenv()

class ETLConfig:
    weather_conditions = os.getenv("WEATHER_CONDITIONS").split(",")