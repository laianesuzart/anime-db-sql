from flask import Blueprint, request
from app.models.exc import DataAlreadyExistsError, IncorrectDataError, InexistentDataError
from app.models.anime_model import Anime

bp_animes = Blueprint('animes', __name__)


@bp_animes.route('/animes', methods=['GET', 'POST'])
def get_create():
    if request.method == 'POST':
        data = request.get_json()
        try:
            anime = Anime(data)
            new_anime = anime.save().__dict__
            return new_anime, 201
        except IncorrectDataError as err:
            return err.message, 422
        except DataAlreadyExistsError as err:
            return err.message, 409

    if request.method == 'GET':
        animes = Anime.get_all()
        return {'data': animes}, 200


@bp_animes.route('/animes/<int:anime_id>')
def filter(anime_id: int):
    try:
        anime = Anime.get_by_id(anime_id).__dict__
        return {'data': anime}, 200
    except InexistentDataError as err:
        return err.message, 404


@bp_animes.route('/animes/<int:anime_id>', methods=['PATCH'])
def update(anime_id: int):
    data = request.get_json()
    try:
        updated_anime = Anime.update(anime_id, data).__dict__
        return updated_anime, 200
    except IncorrectDataError as err:
        return err.message, 422
    except InexistentDataError as err:
        return err.message, 404


@bp_animes.route('/animes/<int:anime_id>', methods=['DELETE'])
def delete(anime_id: int):
    try:
        Anime.delete(anime_id)
        return '', 204
    except InexistentDataError as err:
        return err.message, 404
