from app.domain.data_models.common import UseCaseResponse

class ResponseUnauthorized(UseCaseResponse):

    def __init__(self, msg: str, reason: str = None):
        self._msg = msg
        self._reason = reason

    @property
    def msg(self):
        return self._msg

    @property
    def reason(self):
        return self._reason
