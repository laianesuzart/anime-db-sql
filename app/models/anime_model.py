from psycopg2 import connect, sql
from psycopg2.errors import UniqueViolation
from typing import Union
from .configs import configs
from .exc import DataAlreadyExistsError, IncorrectDataError, InexistentDataError


def create_table() -> None:
    conn = connect(**configs)
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


class Anime:
    REQUIRED_KEYS = ['anime', 'released_date', 'seasons']

    def __init__(self, fields: Union[dict, tuple]) -> None:
        if type(fields) is dict:
            for key in self.REQUIRED_KEYS:
                if key not in fields:
                    raise IncorrectDataError(self.REQUIRED_KEYS, [])
            self.check_incorrect_keys(fields)

            for key, value in fields.items():
                setattr(self, key, value)
            self.anime = self.anime.title()
        
        if type(fields) is tuple:
            self.id, self.anime, self.released_date, self.seasons = fields

    def save(self):
        conn = connect(**configs)
        cur = conn.cursor()

        columns = [sql.Identifier(key) for key in self.__dict__.keys()]
        values = [sql.Literal(value) for value in self.__dict__.values()]

        query = sql.SQL(
            """
                INSERT INTO
                    animes (id, {columns})
                VALUES
                    (DEFAULT, {values})
                RETURNING *;
            """).format(columns=sql.SQL(',').join(columns),
                        values=sql.SQL(',').join(values))

        try:
            cur.execute(query)
        except UniqueViolation:
            raise DataAlreadyExistsError('anime')

        fetch_result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        new_anime = Anime(fetch_result)

        return new_anime

    @classmethod
    def check_incorrect_keys(cls, data: dict):
        wrong_keys = []
        for key in data:
            if key not in cls.REQUIRED_KEYS:
                wrong_keys.append(key)
        if wrong_keys:
            raise IncorrectDataError(cls.REQUIRED_KEYS, wrong_keys)
    
    @classmethod
    def update(cls, id: int, data: dict):
        cls.check_incorrect_keys(data)

        if data.get('anime'):
            data.update({'anime': data['anime'].title()})

        conn = connect(**configs)
        cur = conn.cursor()

        columns = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]

        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = row({values})
                WHERE
                    id={id}
                RETURNING *
            """).format(id=sql.Literal(str(id)),
                       columns=sql.SQL(',').join(columns),
                       values=sql.SQL(',').join(values))

        cur.execute(query)
        fetch_result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if not fetch_result:
            raise InexistentDataError

        anime = Anime(fetch_result)

        return anime

    @staticmethod
    def get_all() -> list:
        conn = connect(**configs)
        cur = conn.cursor()

        cur.execute('SELECT * FROM animes;')
        fetch_result = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()

        animes = [Anime(anime_data).__dict__ for anime_data in fetch_result]

        return animes

    @staticmethod
    def get_by_id(id: int):
        conn = connect(**configs)
        cur = conn.cursor()

        cur.execute('SELECT * FROM animes WHERE id = (%s);', (id,))
        fetch_result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if not fetch_result:
            raise InexistentDataError
        
        anime = Anime(fetch_result)

        return anime

    @staticmethod
    def delete(id: int) -> None:
        conn = connect(**configs)
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM animes
            WHERE id = (%s)
            RETURNING *;
        """, (id,))
        fetch_result = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if not fetch_result:
            raise InexistentDataError
