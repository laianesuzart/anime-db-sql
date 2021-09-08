from app.services.helper import check_incorrect_keys
from app.services import connect_db
from app.services.anime_model import Anime
from app.services.exc import DataAlreadyExistsError, IncorrectDataError, InexistentDataError

TABLE_NAME = 'animes'
FIELDNAMES = ('id', 'anime', 'released_date', 'seasons')
REQUIRED_KEYS = ['anime', 'released_date', 'seasons']


def create_table() -> None:
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
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
    create_table()
    try:
        anime = Anime(**data)
    except TypeError:
        raise IncorrectDataError(REQUIRED_KEYS, [])

    anime_data = anime.data()

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT * FROM {TABLE_NAME}
        WHERE anime = '{anime_data['anime']}';
    """)
    has_anime = bool(cur.fetchone())

    if has_anime:
        raise DataAlreadyExistsError('anime')

    cur.execute(f"""
        INSERT INTO {TABLE_NAME}
            ({anime.atributes()})
        VALUES
            ({anime.values()})
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
    create_table()

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT * FROM {TABLE_NAME}
    """)
    animes = cur.fetchall()

    processed_data = [dict(zip(FIELDNAMES, anime)) for anime in animes]

    conn.commit()
    cur.close()
    conn.close()

    return processed_data


def get_anime_by_id(anime_id: int) -> dict:
    create_table()

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT * FROM {TABLE_NAME}
        WHERE id = {anime_id}
    """)
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
    create_table()
    atributes = ', '.join([f'{key} = %s' for key in list(data.keys())])
    if data.get('anime'):
        data.update({'anime': data['anime'].title()})
    values = tuple(data.values())

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE {TABLE_NAME}
        SET {atributes}
        WHERE id = {anime_id}
        RETURNING *;
    """, 
    values)
    anime = cur.fetchone()

    if not anime:
        raise InexistentDataError
    
    processed_data = dict(zip(FIELDNAMES, anime))

    conn.commit()
    cur.close()
    conn.close()

    return processed_data