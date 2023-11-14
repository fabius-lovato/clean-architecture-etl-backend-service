from app.domain.data_models.common import UseCaseResponse

class ResponseResourceNotFound(UseCaseResponse):

    def __init__(self, resource: str, msg: str , detail: str = None):
        self._resource = resource
        self._msg = msg
        self._detail = detail

    @property
    def resource(self):
        return self._resource

    @property
    def msg(self):
        return self._msg

    @property
    def detail(self):
        return self._detail
