class BaseException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ScrapingException(BaseException):
    pass


class NoFilesException(BaseException):
    pass


class TaskNotFoundException(BaseException):
    pass
