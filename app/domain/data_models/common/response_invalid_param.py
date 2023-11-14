from app.domain.data_models.common import UseCaseResponse

class ResponseInvalidParam(UseCaseResponse):

    def __init__(self, msg: str, field: str = None, detail: str = None):
        self._field = field
        self._msg = msg
        self._detail = detail

    @property
    def field(self):
        return self._field

    @property
    def msg(self):
        return self._msg

    @property
    def detail(self):
        return self._detail
