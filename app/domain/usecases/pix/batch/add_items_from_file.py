from abc import abstractmethod
from typing import Any, Optional
from app.domain.data_models.common import UseCaseParams, UseCaseResponse
from app.domain.data_models.upload_file_param import UploadFileParam

from app.domain.usecases import UseCase


class PixBatchAddItemsFromFileParams(UseCaseParams):
    # Identificador do lote
    batch_id: str | int

    # Commom parameters for all file formats.
    file: UploadFileParam
    encoding: Optional[str]
    file_type: Optional[str]
    ignore_duplicates: Optional[bool]

    # CSV file paramenters
    delimiter: Optional[str]
    quote_char: Optional[str]
    escape_char: Optional[str]
    skip_initial_space: Optional[bool]
    line_terminator: Optional[str]


class AddPixBatchItemsUploadFile(UseCase):

    @abstractmethod
    def run(self, params: PixBatchAddItemsFromFileParams = None, **kwargs) -> UseCaseResponse:
        raise NotImplementedError()
