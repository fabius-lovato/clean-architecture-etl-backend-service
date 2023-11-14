from typing import Dict, List
from app.domain.data_models.pix_batch_add_items_from_file_data_models import PixBatchFileErroItem
from app.services.usecases.pix.batch.reader.file_reader_contract import PixBatchFilePayment, PixBatchFileValidationContract

from app.utils.ispb import is_ispb_valid
from app.utils.validation import detect_pix_key, is_account_branch_valid, is_account_number_valid, is_account_type_valid, is_amount_valid, is_txid_valid
from app.utils.validation import is_cnpj_valid, is_cpf_or_cnpj_valid, is_cpf_valid, is_pix_identifier_valid, is_pix_key_type_valid, is_pix_key_valid


class PixBatchPaymentFromFileValidator(PixBatchFileValidationContract):

    def check(self, data: PixBatchFilePayment, row_index: int, file_line: int, **kwargs) -> List[Dict] | None:

        data_errors = self._validate_row_data(data, row_index, file_line)

        required_errors = self._validate_required_fields(data, row_index, file_line)
        data_errors.extend(required_errors)

        return data_errors


    def _validate_row_data(self, row_data: PixBatchFilePayment, row_index: int, file_line: int) -> List:
        errors = []
        if row_data.amount:
            if not is_amount_valid(row_data.amount):
                errors.append(PixBatchFileErroItem(file_line, row_index, 'amount',
                                                   f"O valor '{row_data.amount}' presente na linha {row_index} não é um valor válido."))
            else:
                if float(row_data.amount) < 0.01:
                    errors.append(PixBatchFileErroItem(file_line, row_index, 'amount', 'O valor mínimo para um pagamento Pix é 1 centavo.'))

        if row_data.description and len(row_data.description) > 140:
            errors.append(PixBatchFileErroItem(file_line, row_index, 'description',
                                               f"A descrição do pagamento informado na linha {row_index} ultrapassou o limite de 140 caracteres."))

        if row_data.identifier and not is_pix_identifier_valid(row_data.identifier):
            errors.append(PixBatchFileErroItem(file_line, row_index, 'identifier',
                                               f"O valor '{row_data.identifier}' na linha {row_index} não é um identificador de transação válido."))

        if row_data.to.txId and not is_txid_valid(row_data.to.txId):
            errors.append(PixBatchFileErroItem(file_line, row_index, 'txId',
                                               f"O txId '{row_data.to.txId}' especificado na linha {row_index} não é valido."))

        if row_data.to.key and not is_pix_key_valid(None, row_data.to.key):
            errors.append(PixBatchFileErroItem(file_line, row_index, 'key', f"O valor '{row_data.to.key}' não é um tipo de chave Pix conhecido."))

        if row_data.to.ispb and not is_ispb_valid(row_data.to.ispb):
            errors.append(PixBatchFileErroItem(file_line, row_index, 'ispb',
                                               f"O código ISPB {row_data.to.ispb} não representa uma instituição financeira válida."))

        if row_data.to.branchNumber and not is_account_branch_valid(row_data.to.branchNumber):
            errors.append(PixBatchFileErroItem(file_line, row_index, 'branchNumber',
                                               f"O valor '{row_data.to.branchNumber}' especificado na linha {row_index} não é um número de agência bancária válida."))

        if row_data.to.accountNumber and not is_account_number_valid(row_data.to.accountNumber):
            errors.append(PixBatchFileErroItem(file_line, row_index, 'accountNumber',
                                               f"O valor '{row_data.to.accountNumber}' especificado na linha {row_index} não é um número de conta financeira válida."))

        if row_data.to.accountType and not is_account_type_valid(row_data.to.accountType):
            errors.append(PixBatchFileErroItem(file_line, row_index, file_line, 'accountType',
                                               f"O valor '{row_data.to.accountType}' especificado na linha {row_index} não é um tipo de conta financeira válida ou suportada."))

        if row_data.to.documentNumber:
            key_pix_type = detect_pix_key(row_data.to.key)

            if key_pix_type == 'cpf':
                if not is_cpf_valid(row_data.to.documentNumber):
                    errors.append(PixBatchFileErroItem(file_line, row_index, 'documentNumber',
                                                       f"O valor '{row_data.to.documentNumber}' especificado na linha {row_index} não é um CPF válido."))
                elif key_pix_type == 'cnpj':
                    if not is_cnpj_valid(row_data.to.documentNumber):
                        errors.append(PixBatchFileErroItem(file_line, row_index, 'documentNumber',
                                                           f"O valor '{row_data.to.documentNumber}' especificado na linha {row_index} não é um CNPJ válido."))
                else:
                    if not is_cpf_or_cnpj_valid(row_data.to.documentNumber):
                        errors.append(PixBatchFileErroItem(file_line, row_index, 'documentNumber',
                                                           f"O valor '{row_data.to.documentNumber}' especificado na linha {row_index} não é um CPF ou CNPJ válido."))

        return errors

    def _validate_required_fields(self, row_data: PixBatchFilePayment, row_index: int, file_line: int) -> List[Dict]:

        errors = []
        if row_data.amount is None:
            errors.append(PixBatchFileErroItem(file_line, row_index, 'amount', 'Necessário especificar um valor para o pagamento Pix.'))

        if row_data.to.txId and row_data.to.key:
            errors.append(PixBatchFileErroItem(file_line, row_index, 'key', 'Pagamentos Pix por QR Code não devem especificar uma chave Pix.'))
        else:
            if not row_data.to.txId and not row_data.to.key:
                if not row_data.to.ispb:
                    errors.append(PixBatchFileErroItem(file_line, row_index, 'ispb',
                                                       f"O campo 'ispb' é requerido em pagamento Pix do tipo manual."))

                if not row_data.to.branchNumber:
                    errors.append(PixBatchFileErroItem(file_line, row_index, 'branchNumber',
                                                       f"O campo 'branchNumber' é requerido em pagamento Pix do tipo manual."))

                if not row_data.to.accountNumber:
                    errors.append(PixBatchFileErroItem(file_line, row_index, 'accountNumber',
                                                       f"O campo 'accountNumber' é requerido em pagamento Pix do tipo manual."))

                if not row_data.to.accountType:
                    errors.append(PixBatchFileErroItem(file_line, row_index, 'accountType',
                                                       f"O campo 'accountType' é requerido em pagamento Pix do tipo manual."))

                if not row_data.to.holderName:
                    errors.append(PixBatchFileErroItem(file_line, row_index, 'holderName',
                                                       f"O campo 'holderName' é requerido em pagamento Pix do tipo manual."))

                if not row_data.to.documentNumber:
                    errors.append(PixBatchFileErroItem(file_line, row_index, 'documentNumber',
                                                       f"O campo 'documentNumber' é requerido em pagamento Pix do tipo manual."))

        return errors
