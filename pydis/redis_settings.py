from os.path import join, dirname
from dotenv import load_dotenv
import os


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


redis_config = {
    "host": os.getenv("REDIS_HOST", "127.0.0.1"),
    "port": int(os.getenv("REDIS_PORT", "6379")),
    "db": int(os.getenv("REDIS_DB", "0")),
    "password": os.getenv("REDIS_PASSWORD", None)
}