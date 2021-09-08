from environs import Env
from os import environ

env = Env()
env.read_env()

HOST = environ.get('HOST')
DATABASE = environ.get('DATABASE')
USER = environ.get('USER')
PASSWORD = environ.get('PASSWORD')
URL_PREFIX = environ.get('URL_PREFIX')
