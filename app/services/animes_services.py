from app.services import connect_db
from app.services.anime_model import Anime
from app.services.exc import DataAlreadyExistsError, IncorrectDataError

TABLE_NAME = 'animes'
FIELDNAMES = ('id', 'anime', 'released_date', 'seasons')


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


def get_all_animes():
    ...


def add_anime(data):
    REQUIRED_KEYS = ['anime', 'released_date', 'seasons']
    wrong_keys = []
    for key in data:
        if key not in REQUIRED_KEYS:
            wrong_keys.append(key)
    if wrong_keys:
        raise IncorrectDataError(REQUIRED_KEYS, wrong_keys)
    
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


def get_all_animes():
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
