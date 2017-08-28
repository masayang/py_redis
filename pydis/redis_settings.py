from os.path import join, dirname
from dotenv import load_dotenv
import os


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


redis_config = {
    "host": os.environ.get("REDIS_HOST"),
    "port": int(os.environ.get("REDIS_PORT")),
    "db": int(os.environ.get("REDIS_DB")),
    "password": os.environ.get("REDIS_PASSWORD")
}