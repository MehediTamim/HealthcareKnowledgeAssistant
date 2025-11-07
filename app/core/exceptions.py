from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str):
        detail = {"message": message}
        super().__init__(status_code=status_code, detail=detail)


def raise_bad_request(message: str):
    raise CustomHTTPException(status.HTTP_400_BAD_REQUEST, message)


def raise_unauthorized(message: str = "Invalid API key"):
    raise CustomHTTPException(status.HTTP_401_UNAUTHORIZED, message)


def raise_internal_error(message: str = "Internal server error"):
    raise CustomHTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, message)
