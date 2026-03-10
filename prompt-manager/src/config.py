import os

from dotenv import load_dotenv

load_dotenv()

MONGO_URI: str = os.environ["MONGO_URI"]
API_BASE_URL: str = os.environ["API_BASE_URL"]
