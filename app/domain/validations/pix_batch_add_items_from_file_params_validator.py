import codecs
import os

from typing import Any, Optional
from app.domain.data_models.common import ResponseInvalidParam
from app.domain.validations.validator_contract import ParamValidator
from app.domain.usecases.pix.batch.add_items_from_file import PixBatchAddItemsFromFileParams, UploadFileParam


class PixBatchAddItemsFromFileParamsValidation(ParamValidator):

    def check(self, params: PixBatchAddItemsFromFileParams, i18n: Optional[Any] = None) -> ResponseInvalidParam | None:
        err = self._check_file_param(params.file, i18n) or \
              self._check_encoding(params.encoding, i18n) or \
              self._check_file_type(file_type=params.file_type, filename=params.file.filename, i18n=i18n)

        return err

    def _is_supported_file_type(self, file_type: str) -> bool:
        if file_type:
            file_type = file_type.strip().upper()

        return file_type in ['CSV', 'JSON', 'XML', 'YML', 'YAML']

    def _check_file_param(self, file: UploadFileParam, i18n: Optional[Any] = None) -> ResponseInvalidParam | None:

        if file is None:
            return ResponseInvalidParam(field='file', msg='Arquivo não especificado.', detail='Necessário informar arquivo com os pagamentos Pix.')

        if not file.filename:
            return ResponseInvalidParam(field='field.filename', msg='Nome do arquivo não especificado.', detail='Ao efetuar o upload do arquivo com os pagamentos Pix, adote um nome compatível com o formato de arquivo suportado.')

        if file.size <= 0:
            return ResponseInvalidParam(field='field.size', msg='Arquivo vazio.', detail='Não há pagamentos a serem importados.')

        return None

    def _check_file_type(self, file_type: str, filename: str, i18n: Optional[Any] = None) -> ResponseInvalidParam | None:

        if file_type:
            if self._is_supported_file_type(file_type):
                return None
            return ResponseInvalidParam(field='file_type', msg='Formato de arquivo desconhecido ou não suportado.', detail=f'O tipo "{file_type}" não é de um formato de arquivo suportado.')


        file_extension = self._get_file_extension(filename)
        if self._is_supported_file_type(file_extension):
            return None

        return ResponseInvalidParam(field='field.filename', msg='Formato de arquivo desconhecido ou não suportado.', detail=f'A extensão {file_extension} não é de um formato de arquivo suportado.')

    def _get_file_extension(self, filename: str) -> str:
        if filename:
            ext = os.path.splitext(filename)[1].upper()
            if ext:
                ext = ext[1:]
            return ext

        return None

    def _check_encoding(self, encoding : str, i18n: Optional[Any] = None) -> ResponseInvalidParam | None:
        if encoding:
            try:
                codecs.lookup(encoding)
            except LookupError:
                return ResponseInvalidParam(field='encoding', msg='Encoding desconhecido ou não suportado.', detail=f'O encoding {encoding} não é válido ou não suportado.')

        return None


class PixBatchAddItemsFromCSVParamsValidation(PixBatchAddItemsFromFileParamsValidation):

    def check(self, params: PixBatchAddItemsFromFileParams, i18n: Optional[Any] = None) -> ResponseInvalidParam | None:
        err = super().check(params, i18n) or \
              self._check_csv_params(params, i18n)

        return err

    def _check_csv_params(self, params: PixBatchAddItemsFromFileParams, i18n: Optional[Any] = None) -> ResponseInvalidParam | None:

        err = self._check_delimiter(params.delimiter, i18n)
        # TODO: Implementar as demais validações.

        return err

    def _check_delimiter(self, delimiter : str, i18n: Optional[Any] = None) -> ResponseInvalidParam | None:
        if delimiter:
            if len(delimiter) != 1:
                return ResponseInvalidParam(field='delimiter', msg='O delimitado de coluna deve ser somente 1 caracter.', detail=f'A string "{delimiter}" não é um delimitador válido.')

        return None
