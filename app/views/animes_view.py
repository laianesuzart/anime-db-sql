from flask import Blueprint, request
from app.services.exc import DataAlreadyExistsError, IncorrectDataError, InexistentDataError
from app.services.animes_services import add_anime, get_all_animes, get_anime_by_id, update_anime
from ..services import URL_PREFIX

bp_animes = Blueprint('animes', __name__, url_prefix=URL_PREFIX)


@bp_animes.route('/animes', methods=['GET', 'POST'])
def get_create():
    if request.method == 'POST':
        data = request.get_json()
        try:
            new_anime = add_anime(data)
            return new_anime, 201
        except IncorrectDataError as err:
            return err.message, 422
        except DataAlreadyExistsError as err:
            return err.message, 409

    if request.method == 'GET':
        animes = get_all_animes()
        return {'data': animes}, 200


@bp_animes.route('/animes/<int:anime_id>')
def filter(anime_id: int):
    try:
        anime = get_anime_by_id(anime_id)
        return {'data': anime}, 200
    except InexistentDataError as err:
        return err.message, 404


@bp_animes.route('/animes/<int:anime_id>', methods=['PATCH'])
def update(anime_id: int):
    data = request.get_json()
    try:
        updated_anime = update_anime(anime_id, data)
        return updated_anime, 200
    except IncorrectDataError as err:
        return err.message, 422
    except InexistentDataError as err:
        return err.message, 404


@bp_animes.route('/animes/<int:anime_id>', methods=['DELETE'])
def delete(anime_id: int):
    ...
