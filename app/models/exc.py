class IncorrectDataError(Exception):
    def __init__(self, required_keys: list, wrong_keys: list, *args) -> None:
        self.message = {
            'available_keys': list(required_keys),
            'wrong_keys_sent': list(wrong_keys)
        }
        super().__init__(self.message, *args)


class DataAlreadyExistsError(Exception):
    def __init__(self, data_name: str, *args) -> None:
        self.message = {
            'error': f'{data_name.title()} already exists.'
        }
        super().__init__(self.message, *args)


class InexistentDataError(Exception):
    def __init__(self, *args) -> None:
        self.message = {
            'error': 'Not Found'
        }
        super().__init__(self.message, *args)
