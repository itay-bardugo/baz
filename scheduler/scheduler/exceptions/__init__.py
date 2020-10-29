INVALID_REQUEST = 1
SERVICE_UNREACHABLE = 2
ACTION_DATE_NOT_VALID = 3


class ApiError(BaseException):
    def __init__(self, code, *args: object) -> None:
        super().__init__(*args)
        self.code = code

    def to_dict(self):
        return {
            "status": self.code,
            "details": "error number: {}".format(self.code)
        }
