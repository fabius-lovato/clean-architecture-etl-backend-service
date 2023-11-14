from app.domain.data_models.common import UseCaseResponse

class ResponseError(UseCaseResponse):

    def __init__(self, msg: str):
        self._msg = msg

    @property
    def msg(self):
        return self._msg
