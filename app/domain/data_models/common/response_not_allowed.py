from app.domain.data_models.common import ResponseError

class ResponseNotAllowed(ResponseError):

    def __init__(self, msg: str, resource: str = None, detail: str = None, reason: str = None):
        super().__init__(msg=msg)
        self._resource = resource
        self._detail = detail
        self._reason = reason

    @property
    def resource(self):
        return self._resource

    @property
    def detail(self):
        return self._detail

    @property
    def reason(self):
        return self._reason
