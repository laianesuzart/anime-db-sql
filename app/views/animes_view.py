from flask import Blueprint
from ..services import URL_PREFIX

bp_animes = Blueprint('animes', __name__, url_prefix=URL_PREFIX)


@bp_animes.route('/animes', methods=['GET', 'POST'])
def get_create():
    ...


@bp_animes.route('/animes/<int:anime_id>')
def filter(anime_id: int):
    ...


@bp_animes.route('/animes/<int:anime_id>', methods=['PATCH'])
def update(anime_id: int):
    ...


@bp_animes.route('/animes/<int:anime_id>', methods=['DELETE'])
def delete(anime_id: int):
    ...
