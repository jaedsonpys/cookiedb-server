class InvalidDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidMessageError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
