from core.exceptions import CustomException


class DatabaseTokenException(CustomException):
    code = 400
    error_code = "INVALID_DATABASE_ERROR"
    message = "invalid database credential error"
