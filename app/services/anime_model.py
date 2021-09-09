class Anime:
    def __init__(self, anime: str, released_date: str, seasons: int):
        self.anime = anime.title()
        self.released_date = released_date
        self.seasons = seasons

    def data(self) -> dict:
        return  self.__dict__
