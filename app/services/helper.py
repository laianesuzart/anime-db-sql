from .exc import IncorrectDataError


def check_incorrect_keys(required_keys: list, data):
    wrong_keys = []
    for key in data:
        if key not in required_keys:
            wrong_keys.append(key)
    if wrong_keys:
        raise IncorrectDataError(required_keys, wrong_keys)
