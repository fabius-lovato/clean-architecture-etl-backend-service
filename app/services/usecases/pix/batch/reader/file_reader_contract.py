from abc import abstractmethod
from fastapi import UploadFile
from typing import Any, Dict, List

class PixBatchFilePaymentAccount:
    def __init__(self, obj: Dict = None):
        if not obj:
            obj = {}

        self.txId           = obj.get('txId', None)
        self.key            = obj.get('key', None)
        self.ispb           = obj.get('ispb', None)
        self.branchNumber   = obj.get('branchNumber', None)
        self.accountNumber  = obj.get('accountNumber', None)
        self.accountType    = obj.get('accountType', None)
        self.holderName     = obj.get('holdername', None)
        self.documentNumber = obj.get('documentNumber', None)

class PixBatchFilePayment:
    def __init__(self, obj: Dict = None):
        if not obj:
            obj = {}

        self.amount      = obj.get('amount', None)
        self.description = obj.get('description', None)
        self.identifier  = obj.get('identifier', None)
        self.to          = PixBatchFilePaymentAccount(obj.get('to', None))

class PixBatchFileResult:
    def __init__(self, items: List[PixBatchFilePayment] = None, errors: List[Dict] = None):

        self.items: List[PixBatchFilePayment] = [] if items is None else items
        self.errors: List[Dict] = [] if errors is None else errors


class PixBatchFileValidationContract():

    @abstractmethod
    def check(self, data: PixBatchFilePayment, row_index: int, file_line: int, **kwargs ) -> List[Any] | None:
        raise NotImplementedError()

class PixBatchFileContract():
    def __init__(self, file: UploadFile, encoding: str | None):
        self.file = file
        self._encoding = encoding

    def get_encoding(self) -> str:
        return self._encoding if self._encoding else 'ISO-8859-1'

    @abstractmethod
    def decode(self, validator: PixBatchFileValidationContract = None) -> PixBatchFileResult:
        raise NotImplementedError()
