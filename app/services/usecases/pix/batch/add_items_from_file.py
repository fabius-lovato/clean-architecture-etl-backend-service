from typing import List
import os
from app.domain.data_models.common import UseCaseResponse, ResponseResourceNotFound, ResponseNotAllowed, ResponseInvalidParam
from app.domain.data_models.pix_batch_add_items_from_file_data_models import PixBatchAddItemsFromFileResponseError, PixBatchAddItemsFromFileResponseSuccess, PixBatchFileUploadInfo
from app.domain.entities.pix_batch_entity import PixBatchEntity
from app.domain.validations.validator_contract import ParamValidator

from app.domain.usecases.pix.batch import PixBatchAddItemsFromFileParams
from app.domain.usecases.pix.batch import AddPixBatchItemsUploadFile as AddPixBatchItemsUploadFileContract
from app.services.repositories.contracts.pix_batch_items_repository_contract import PixBatchItemsRepositoryContract
from app.services.repositories.contracts.pix_batch_repository_contract import PixBatchRepositoryContract
from app.services.usecases.pix.batch.reader import PixBatchFileContract
from app.services.usecases.pix.batch.reader.file_reader_contract import PixBatchFilePayment, PixBatchFileResult, PixBatchFileValidationContract

from app.domain.entities.pix_batch_items_entity import PixBatchItemEntity

class AddPixBatchItemsUploadFile(AddPixBatchItemsUploadFileContract):

    def __init__(self,
                 pix_batch_repository: PixBatchRepositoryContract,
                 pix_batch_items_repository: PixBatchItemsRepositoryContract,
                 file_reader: PixBatchFileContract,
                 params_validator: ParamValidator,
                 payment_validator: PixBatchFileValidationContract,) -> None:

        self._pix_batch_repository = pix_batch_repository
        self._pix_batch_items_repository = pix_batch_items_repository
        self._file_reader = file_reader
        self._params_validator = params_validator
        self._payment_validator = payment_validator

    def run(self, params: PixBatchAddItemsFromFileParams) -> UseCaseResponse:

        err = self._params_validator.check(params)
        if err:
            return err

        pix_batch_data: PixBatchEntity = self._pix_batch_repository.get_pix_batch_by_id(params.batch_id)
        if not pix_batch_data:
            return ResponseResourceNotFound(resource='batch_id', msg='Pix lote não encontrado')

        if not pix_batch_data.is_pending():
            return ResponseNotAllowed(resource='batch_id',
                                      msg='Não é permitido inserir novos pagamentos Pix nesse lote.',
                                      details=f'O lote {params.batch_id} não está pendente.',
                                      reason='A inclusão de novos pagamentos só é permitida enquanto o processamento do lote não foi iniciado.')

        result: PixBatchFileResult = self._file_reader.decode(self._payment_validator)

        if len(result.items) > 0:
            # Evita processamento extra quando já foram encontrados inconsistências.
            if not params.ignore_duplicates and len(result.errors) == 0:
                self._check_duplicated(result)
        else:
            if len(result.errors) == 0:
                return ResponseInvalidParam(field='file', msg='Arquivo vazio.', detail='O arquivo informado não contém pagamentos Pix.')

        if len(result.errors) == 0:
            self._insert_items_into_pix_batch(result, pix_batch_data)

        return self._mount_response(result, params)

    def _check_duplicated(self, result: PixBatchFileResult):
        # TODO:

        pass

    def _insert_items_into_pix_batch(self, result: PixBatchFileResult, pix_batch_data: PixBatchEntity):

        # FIXME: A inserção dos pagamentos e a atualização do lote são operações que devem fazer parte de um transação.
        for item in result.items:

            pix_batch_item = self.__map_pix_batch_file_payment_to_entity(item)

            if not self._pix_batch_items_repository.insert_pix_batch_item(pix_batch_data.id, pix_batch_item):
                # TODO: tratar falha na inserção do item na base de dados.
                pass

            pix_batch_data.total_amount += pix_batch_item.amount
            pix_batch_data.total_items += 1


        if not self._pix_batch_repository.update_pix_batch_total(pix_batch_data.id, pix_batch_data.total_items, pix_batch_data.total_amount):
            # TODO: tratar falha na atualização dos dados do lote
            pass

    def _mount_response(self, result: PixBatchFileResult, params: PixBatchAddItemsFromFileParams):

        if len(result.errors) > 0:
            return self._mount_error_response(result, params)

        return self._mount_success_response(result, params)

    def _mount_success_response(self, result: PixBatchFileResult, params: PixBatchAddItemsFromFileParams) -> PixBatchAddItemsFromFileResponseSuccess:

        success = PixBatchAddItemsFromFileResponseSuccess()
        success.file = self._mount_file_result(params)
        success.total_count = len(result.items)
        success.total_amount = self.__get_total_mount(result.items)

        return success

    def _mount_error_response(self, result: PixBatchFileResult, params: PixBatchAddItemsFromFileParams) -> PixBatchAddItemsFromFileResponseError:

        failure = PixBatchAddItemsFromFileResponseError(msg='Encontrado inconsistências na requisição.')
        failure.file = self._mount_file_result(params)
        failure.total_error_count = len(result.errors)
        failure.errors = result.errors

        return failure

    def _mount_file_result(self, params: PixBatchAddItemsFromFileParams):
        file_result = PixBatchFileUploadInfo()
        file_result.name = params.file.filename
        file_result.size = params.file.size
        file_result.type = self.__get_file_type_from_request(params)
        #file_result.total_lines = ?

        return file_result

    def __get_total_mount(self, items: List[PixBatchFilePayment]):
        total_amount = 0
        for item in items:
            total_amount += float(item.amount)

        return total_amount

    def __get_file_type_from_request(self, params: PixBatchAddItemsFromFileParams):
        if params.file_type and isinstance(params.file_type, str):
            return str(params.file_type).upper()

        if params.file and params.file.filename and isinstance(params.file.filename, str):
            return self.__extract_extension_from_file_name(params.file.filename)

        return None

    def __extract_extension_from_file_name(self, filename: str) -> str:
        if filename:
            try:
                ext = os.path.splitext(filename)[1].upper()
                if ext:
                    ext = ext[1:]
                return ext
            except TypeError:
                pass

        return None


    def __map_pix_batch_file_payment_to_entity(self, payment: PixBatchFilePayment) -> PixBatchItemEntity:
        pix_batch_item = PixBatchItemEntity()

        pix_batch_item.amount            = float(payment.amount)
        pix_batch_item.tx_id             = payment.to.txId
        pix_batch_item.pix_key           = payment.to.key
        pix_batch_item.institution       = payment.to.ispb
        pix_batch_item.branch            = payment.to.branchNumber
        pix_batch_item.account_number    = payment.to.accountNumber
        pix_batch_item.account_type      = payment.to.accountType
        pix_batch_item.holder_name       = payment.to.holderName
        pix_batch_item.document_number   = payment.to.documentNumber
        pix_batch_item.identifier        = payment.identifier
        pix_batch_item.description       = payment.description

        return pix_batch_item
