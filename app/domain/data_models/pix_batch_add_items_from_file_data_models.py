from typing import List
from app.domain.data_models.common import UseCaseResponse, ResponseSuccess, ResponseError


class PixBatchFileUploadInfo(UseCaseResponse):
    name: str
    size: int
    type: str
    total_lines: int

    def __init__(self):
        self.size = 0
        self.total_lines = 0


class PixBatchAddItemsFromFileResponseSuccess(ResponseSuccess):
    file: PixBatchFileUploadInfo
    total_count: int
    total_amount: float

    def __init__(self):
        self.file = PixBatchFileUploadInfo()
        self.total_count = 0
        self.total_amount = 0



class PixBatchFileErroItem(UseCaseResponse):
    fileline: int
    index: int
    field: str
    description: str

    def __init__(self, fileline: int = None, index: int = None, field: str = None, description: str = None):
        self.fileline = fileline
        self.index = index
        self.field = field
        self.description = description

class PixBatchAddItemsFromFileResponseError(ResponseError):
    file: PixBatchFileUploadInfo
    total_error_count: int
    errors: List[PixBatchFileErroItem]

    def __init__(self, msg: str = None, file: PixBatchFileUploadInfo = None, total_error_count: int = None, errors: List[PixBatchFileErroItem] = None):
        super().__init__(msg=msg)
        self.file = file
        self.total_error_count = total_error_count
        self.errors = errors
