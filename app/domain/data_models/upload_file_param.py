from typing import Any
from app.domain.data_models.common import UseCaseParams


class UploadFileParam(UseCaseParams):
    file: Any
    filename: str
    size: int

    def __init__(self, file: Any, filename: str, size: int):
        self.file = file
        self.filename = filename
        self.size = size
