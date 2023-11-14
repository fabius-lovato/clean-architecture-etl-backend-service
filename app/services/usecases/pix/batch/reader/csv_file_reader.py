from fastapi import UploadFile
import codecs
import csv
from typing import Dict, List, Sequence
from app.domain.data_models.pix_batch_add_items_from_file_data_models import PixBatchFileErroItem
from app.services.usecases.pix.batch.reader.file_reader_contract import PixBatchFileContract, PixBatchFileResult, PixBatchFilePayment, PixBatchFileValidationContract

class PixBatchCSVFileReader(PixBatchFileContract):

    # TODO: Incluir no construtor os demais parâmetros de configuração.
    def __init__(self, file: UploadFile, encoding: str | None, delimiter: str | None):
        super().__init__(file, encoding)
        self._delimiter = delimiter

        self._ALLOWED_COLUMNS = {'amount', 'txid', 'key', 'ispb', 'branchnumber', 'accountnumber', 'accounttype', 'holdername', 'documentnumber', 'identifier', 'description'}
        self._COLUMNS_FOR_PAYMENT_WITH_PIXKEY = {'amount', 'key'}
        self._COLUMNS_FOR_MANUAL_PAYMENT = {'amount', 'ispb', 'branchnumber', 'accountnumber', 'accounttype', 'holdername', 'documentnumber'}

    def get_delimiter(self) -> str:
        return self._delimiter if self._delimiter else ';'

    def decode(self, validator: PixBatchFileValidationContract = None) -> PixBatchFileResult:
        if self.file:
            print(f'File: {self.file.filename}, Size: {self.file.size}, Encoding: {self.get_encoding()}, Delimiter: {self.get_delimiter()}')

            try:
                reader = csv.DictReader(codecs.iterdecode(self.file.file, self.get_encoding()), delimiter=self.get_delimiter())

                return self._parser_data_csv(reader, validator)
            except Exception as e:
                print(f'Erro ao acessar do {self.file.filename}.')
                print(e)

                raise

        return None

    def _parser_data_csv(self, reader: csv.DictReader, validator: PixBatchFileValidationContract) -> PixBatchFileResult:
        row_index = 0
        items = []

        errors = self._check_header(reader.fieldnames)
        if errors:
            return PixBatchFileResult(items, errors)

        for row in reader:
            row_index += 1

            row_data = self._mount_item(row)
            row_errors = None
            if validator:
                row_errors = validator.check(row_data, row_index, row_index+1)

            if row_errors:
                errors.extend(row_errors)
            else:
                items.append(row_data)

        return PixBatchFileResult(items, errors)

    def _check_header(self, fieldnames: Sequence | None) -> List:
        errors = []
        if not fieldnames or len(fieldnames) <= 0:
            errors.append(PixBatchFileErroItem(1, 1, 'header', 'Arquivo .CSV sem colunas definidas.'))

        else:
            # Altera-se o nome das colunas/fields do header para tornar a identificação dos campos
            # mais fácil e flexível.
            for k,v in enumerate(fieldnames):
                fieldnames[k] = v.lower().strip()

            for index, name, in enumerate(fieldnames):
                if not name:
                    errors.append(PixBatchFileErroItem(1, index + 1, 'column', f"A coluna {index + 1} deve possuir um nome ou título definido."))

                elif name not in self._ALLOWED_COLUMNS:
                    errors.append(PixBatchFileErroItem(1, index + 1, 'column', f"A coluna '{name}' é desconhecida ou não suportada."))

            for allowed_field in self._ALLOWED_COLUMNS:
                if len([col for col in fieldnames if col == allowed_field]) > 1:
                    index = len(fieldnames) - fieldnames[::-1].index(allowed_field)
                    errors.append(PixBatchFileErroItem(1, index,
                                                       'column', f"A coluna '{allowed_field}' está duplicada."))

            columns = set(fieldnames)

            if not self._COLUMNS_FOR_PAYMENT_WITH_PIXKEY.issubset(columns) and \
               not self._COLUMNS_FOR_MANUAL_PAYMENT.issubset(columns):
                errors.append(PixBatchFileErroItem(1, 1, 'header',
                                                   'O arquivo não contém a estrutura de campos mínima para especificar um dos três métodos de pagamentos Pix.'))

        return errors

    def _mount_item(self, row: Dict) -> PixBatchFilePayment:

        return PixBatchFilePayment({
            'amount':             self._extract_clean_text_from(row, 'amount'),
            'identifier':         self._extract_clean_text_from(row, 'identifier'),
            'description':        self._extract_clean_text_from(row, 'description'),
            'to': {
                'txId':           self._extract_clean_text_from(row, 'txid'),
                'key':            self._extract_clean_text_from(row, 'key'),
                'ispb':           self._extract_clean_text_from(row, 'ispb'),
                'branchNumber':   self._extract_clean_text_from(row, 'branchnumber'),
                'accountNumber':  self._extract_clean_text_from(row, 'accountnumber'),
                'accountType':    self._extract_clean_text_from(row, 'accounttype'),
                'holdername':     self._extract_clean_text_from(row, 'holdername'),
                'documentNumber': self._extract_clean_text_from(row, 'documentnumber')
            }
        })

    def _extract_clean_text_from(self, row: Dict, col_name: str | None) -> str | None:
        text = row.get(col_name)
        if text:
            text = text.strip()

        return (None if not text else text)

    def _find_duplicate_on(self, row_data: List, items) -> int | None:
        return row_data.index(row_data)  # TODO
