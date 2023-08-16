class DatabaseAlreadyExistsExceptions(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(self.message)


class DatabaseUnknownError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(self.message)


class FileNotExistsError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(self.message)
