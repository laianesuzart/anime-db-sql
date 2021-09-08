from environs import Env
from os import environ
import psycopg2

env = Env()
env.read_env()

HOST = environ.get('HOST')
DATABASE = environ.get('DATABASE')
USER = environ.get('USER')
PASSWORD = environ.get('PASSWORD')
URL_PREFIX = environ.get('URL_PREFIX')


def connect_db():
    return psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
