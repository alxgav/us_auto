import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv

path = os.path.dirname(os.path.realpath(__file__))

load_dotenv(find_dotenv())

# user = os.getenv("user")
# url = os.getenv("url")
# password = os.getenv("pass")
# work_url = os.getenv("work_url")

try:
    user = os.environ["user"]
    url = os.environ["url"]
    password = os.environ["pass"]
    work_url = os.environ["work_url"]
except KeyError as err:
    logger.critical(f"Can't read env. Message: {err}")
    raise KeyError(err)


logger.add(
    f"{path}/log/log.log",
    format="{time} {level} {message}",
    level="WARNING",
    serialize=False,
    rotation="1 month",
    compression="zip",
)
