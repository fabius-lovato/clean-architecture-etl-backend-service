from fastapi import UploadFile

from xml.etree import ElementTree

from typing import Dict, List, Sequence
from app.services.usecases.pix.batch.reader.file_reader_contract import PixBatchFileContract, PixBatchFileResult, PixBatchFilePayment

class PixBatchXMLFileReader(PixBatchFileContract):
    def __init__(self, file: UploadFile, encoding: str | None, delimiter: str | None):
        super().__init__(file, encoding)
        self._delimiter = delimiter

        self._ALLOWED_COLUMNS = {'amount', 'key', 'type', 'txid', 'institution', 'branch', 'accountnumber', 'accounttype', 'name', 'document', 'identifier', 'description'}
        self._COLUMNS_FOR_PAYMENT_WITH_QRCODE = {'amount', 'txid', 'institution', 'branch', 'accountnumber', 'accounttype', 'name', 'document'}
        self._COLUMNS_FOR_PAYMENT_WITH_PIXKEY = {'amount', 'type', 'key'}
        self._COLUMNS_FOR_MANUAL_PAYMENT = {'amount', 'institution', 'branch', 'accountnumber', 'accounttype', 'name', 'document'}


    def get_delimiter(self) -> str:
        return self._delimiter if self._delimiter else ';'

    def decode(self) -> PixBatchFileResult:
        if self.file:
            print(f'File: {self.file.filename}, Size: {self.file.size}, Encoding: {self.get_encoding()}, Delimiter: {self.get_delimiter()}')

            try:
                file_content = tree = ElementTree.parse(self.file)
                root = tree.getroot()

                result = self._load_data_from_xml_root(root)

                return result
            except Exception as e:
                print(f'Erro ao acessar do {self.file.filename}.')

                raise Exception('Erro ao cadastrar item de lote')

        return None

    def _load_data_from_xml_root(self, root: ElementTree.Element) -> PixBatchFileResult:

        for node in root:
            pass

        return PixBatchFileResult()

    def _mount_item(self, row: Dict) -> PixBatchFilePayment:

        return None

    def _extract_clean_text_from(self, row: Dict, col_name: str | None) -> str | None:
        text = row.get(col_name)
        if text:
            text = text.strip()

        return (None if not text else text)
