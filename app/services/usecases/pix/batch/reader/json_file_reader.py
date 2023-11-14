from fastapi import UploadFile
import json
from typing import Dict, List, Sequence
from app.services.usecases.pix.batch.reader.file_reader_contract import PixBatchFileContract, PixBatchFileResult, PixBatchFilePayment


class PixBatchJSONFileReader(PixBatchFileContract):
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
                reader = json.load(self.file.file, )
                result = self._parser_data_csv(reader)

                return result
            except Exception as e:
                print(f'Erro ao acessar do {self.file.filename}.')

                raise Exception('Erro ao cadastrar item de lote')

        return None

    def _parser_data_csv(self, reader: object) -> PixBatchFileResult:
        row_index = 0
        row_count_error = 0
        total_amount = 0
        items = []

        errors = self._check_header(reader.fieldnames)
        if errors:
            return items, errors

        for row in reader:
            row_index += 1

            row_data = self._mount_item(row)

            row_errors = self._validate_row_data(row_index, row_data)

            required_errors = self._validate_required_fields(row_index, row_data)
            row_errors.extend(required_errors)

            if not row_errors and not ignore_duplicates:
                found_index = self._find_duplicate_on(row_data, items)
                if found_index:
                    row_errors.append(
                        {
                            'line': row_index,
                            'msg': f'O item da linha "{row_index}" é contém os mesmos dados da linha {found_index}.'
                        }
                    )

            if row_errors:
                errors.extend(row_errors)
                row_count_error += 1
            else:
                total_amount += int(row_data.amount)
                items.append(row_data)

        return {
            'row_count': row_index,
            'row_count_error': row_count_error,
            'total_amount': total_amount,
            'items': items,
            'errors': errors
        }

    def _mount_item(self, row: Dict) -> PixBatchFilePayment:
        return None

    def _extract_clean_text_from(self, row: Dict, col_name: str | None) -> str | None:
        text = row.get(col_name)
        if text:
            text = text.strip()

        return (None if not text else text)
