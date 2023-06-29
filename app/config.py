import os
from loguru import logger
from time import time
from dotenv import load_dotenv, find_dotenv

path = os.path.dirname(os.path.realpath(__file__))

load_dotenv(find_dotenv())

user = os.getenv('user')
url = os.getenv('url')
password = os.getenv('pass')
work_url = os.getenv('work_url') 

auction = ('COPART', 'IAAI')


logger.add(f'{path}/log/log.log', 
           format= '{time} {level} {message}', 
           level='DEBUG', 
           serialize=False, 
           rotation='1 month', 
           compression='zip')

def time_run(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        total_time = time() - start_time
        if total_time < 1:
            total_time = 'less second'
        else:
            total_time = f'{round(total_time, 2)} seconds'
        logger.info(f'{total_time} ')
        return result
    return wrapper