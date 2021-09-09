from app.services.helper import check_incorrect_keys
from app.services.anime_model import Anime
from app.services.exc import DataAlreadyExistsError, IncorrectDataError, InexistentDataError
from environs import Env
from os import environ
import psycopg2

env = Env()
env.read_env()

HOST = environ.get('HOST')
DATABASE = environ.get('DATABASE')
USER = environ.get('USER')
PASSWORD = environ.get('PASSWORD')


def connect_db():
    return psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

FIELDNAMES = ('id', 'anime', 'released_date', 'seasons')
REQUIRED_KEYS = ['anime', 'released_date', 'seasons']


def create_table() -> None:
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS animes (
            id              BIGSERIAL    PRIMARY KEY,
            anime           VARCHAR(100) NOT NULL UNIQUE,
            released_date   DATE         NOT NULL,
            seasons         INTEGER      NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def add_anime(data: dict) -> dict:
    check_incorrect_keys(REQUIRED_KEYS, data)
    try:
        anime = Anime(**data)
    except TypeError:
        raise IncorrectDataError(REQUIRED_KEYS, [])

    anime_data = anime.data()

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM animes
        WHERE anime = (%s);
    """, (anime_data['anime'],))
    has_anime = bool(cur.fetchone())

    if has_anime:
        raise DataAlreadyExistsError('anime')

    cur.execute("""
        INSERT INTO animes
            (anime, released_date, seasons)
        VALUES
            (%(anime)s, %(released_date)s, %(seasons)s)
        RETURNING *;
    """,
    anime_data)
    new_anime = cur.fetchone()

    processed_data = dict(zip(FIELDNAMES, new_anime))

    conn.commit()
    cur.close()
    conn.close()

    return processed_data


def get_all_animes() -> list:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM animes')
    animes = cur.fetchall()

    processed_data = [dict(zip(FIELDNAMES, anime)) for anime in animes]

    conn.commit()
    cur.close()
    conn.close()

    return processed_data


def get_anime_by_id(anime_id: int) -> dict:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM animes
        WHERE id = (%s)
    """, (anime_id,))
    anime = cur.fetchone()

    if not anime:
        raise InexistentDataError
    
    processed_data = dict(zip(FIELDNAMES, anime))

    conn.commit()
    cur.close()
    conn.close()

    return processed_data


def update_anime(anime_id: int, data: dict) -> dict:
    check_incorrect_keys(REQUIRED_KEYS, data)

    if data.get('anime'):
        data.update({'anime': data['anime'].title()})

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM animes
        WHERE id = (%s)
    """, (anime_id,))
    old_anime = cur.fetchone()

    if not old_anime:
        raise InexistentDataError

    old_anime = dict(zip(FIELDNAMES, old_anime))
    data.setdefault('anime', old_anime['anime'])
    data.setdefault('released_date', old_anime['released_date'])
    data.setdefault('seasons', old_anime['seasons'])

    cur.execute("""
        UPDATE animes
        SET anime = (%s), released_date = (%s), seasons = (%s)
        WHERE id = (%s)
        RETURNING *;
    """, 
    (data['anime'], data['released_date'], data['seasons'], anime_id,))
    anime = cur.fetchone()

    processed_data = dict(zip(FIELDNAMES, anime))

    conn.commit()
    cur.close()
    conn.close()

    return processed_data


def delete_anime(anime_id: int) -> None:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM animes
        WHERE id = (%s);
    """, (anime_id,))
    anime = cur.fetchone()

    if not anime:
        raise InexistentDataError
    
    cur.execute("""
        DELETE FROM animes
        WHERE id = (%s);
    """, (anime_id,))

    conn.commit()
    cur.close()
    conn.close()
