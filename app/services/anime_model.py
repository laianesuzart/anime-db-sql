class Anime:
    def __init__(self, anime: str, released_date: str, seasons: int):
        self.anime = anime.title()
        self.released_date = released_date
        self.seasons = seasons

    def atributes(self) -> str:
        parameters_list = list(self.__dict__.keys())
        return ', '.join(parameters_list)

    def values(self) -> str:
        values_list = [f'%({value})s' for value in list(self.__dict__.keys())]
        return ', '.join(values_list)

    def data(self) -> dict:
        return  self.__dict__

