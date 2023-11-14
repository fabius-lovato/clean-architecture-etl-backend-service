from app.domain.data_models.common import ResponseError

class ResponseGenericError(ResponseError):

    def __init__(self, msg: str, code: str = None, detail: str = None, reason: str = None):
        super().__init__(msg=msg)
        self._code = code
        self._detail = detail
        self._reason = reason

    @property
    def code(self):
        return self._code

    @property
    def detail(self):
        return self._detail

    @property
    def reason(self):
        return self._reason
