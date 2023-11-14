import os

from app.domain.usecases import UseCase
from app.domain.usecases.pix.batch import PixBatchAddItemsFromFileParams
from app.domain.validations.pix_batch_add_items_from_file_params_validator import PixBatchAddItemsFromFileParamsValidation
from app.domain.validations.pix_batch_add_items_from_file_params_validator import PixBatchAddItemsFromCSVParamsValidation
from app.domain.validations.validator_contract import ParamValidator

from app.infrastructure.database.gcp_datastore.config.connection import GCPDatastoreConnection
from app.infrastructure.database.gcp_datastore.payment.pix_batch_repository import PixBatchRepository
from app.infrastructure.database.gcp_datastore.payment.pix_batch_items_repository import PixBatchItemsRepository
from app.main.rest.services.pix.batch.pix_batch_payment_validator import PixBatchPaymentFromFileValidator
from app.services.exceptions import DatabaseConnection

from app.services.usecases.pix.batch.add_items_from_file import AddPixBatchItemsUploadFile
from app.services.usecases.pix.batch.reader.csv_file_reader import PixBatchCSVFileReader
from app.services.usecases.pix.batch.reader.file_reader_contract import PixBatchFileContract, PixBatchFileValidationContract
from app.services.usecases.pix.batch.reader.xml_file_reader import PixBatchXMLFileReader
from app.services.usecases.pix.batch.reader.json_file_reader import PixBatchJSONFileReader
from app.services.usecases.pix.batch.reader.yaml_file_reader import PixBatchYAMLFileReader

def pix_batch_items_file_post_factory(params: PixBatchAddItemsFromFileParams) -> UseCase:
    try:
        db_client = GCPDatastoreConnection().client()
        try:
            pix_batch_repository = PixBatchRepository(db_client)
            pix_batch_items_repository = PixBatchItemsRepository(db_client)

            # `Reader` específico para o tipo/formato de arquivo.
            file_reader: PixBatchFileContract = None

            # Alguns parâmetros são específicos do tipo/formato de arquivo.
            params_validator: ParamValidator = None

            # Objeto `validator` que verifica a integridade dos pagamentos Pix extraídos do arquivo.
            payment_validator: PixBatchFileValidationContract = PixBatchPaymentFromFileValidator()
            file_type = __get_file_type_from_request(params)

            if file_type == 'CSV':
                # TODO: Incluir os outros parâmetros
                file_reader = PixBatchCSVFileReader(file=params.file,
                                                    encoding=params.encoding,
                                                    delimiter=params.delimiter)
                params_validator = PixBatchAddItemsFromCSVParamsValidation()
            elif file_type == 'XML':
                file_reader = PixBatchXMLFileReader(file=params.file, encoding=params.encoding, delimiter=params.delimiter)
                params_validator = PixBatchAddItemsFromFileParamsValidation()
            elif file_type == 'JSON':
                file_reader = PixBatchJSONFileReader(file=params.file, encoding=params.encoding, delimiter=params.delimiter)
                params_validator = PixBatchAddItemsFromFileParamsValidation()
            elif file_type in ['YML', 'YAML']:
                file_reader = PixBatchYAMLFileReader(file=params.file, encoding=params.encoding, delimiter=params.delimiter)
                params_validator = PixBatchAddItemsFromFileParamsValidation()
            else:
                params_validator = PixBatchAddItemsFromFileParamsValidation()

            return AddPixBatchItemsUploadFile(pix_batch_repository, pix_batch_items_repository, file_reader, params_validator, payment_validator)

        except Exception as e:
            print('Database connection failed!')
            print(e)
            raise Exception(msg='Internal error! Contact the system administrator')

    except Exception as e:
        print('Database connection failed!')
        print(e)
        raise DatabaseConnection(msg='Internal error! Contact the system administrator')




def __get_file_type_from_request(params: PixBatchAddItemsFromFileParams):
    if params.file_type and isinstance(params.file_type, str):
        return str(params.file_type).upper()

    if params.file and params.file.filename and isinstance(params.file.filename, str):
        return __extract_extension_from_file_name(params.file.filename)

    return None

def __extract_extension_from_file_name(filename: str) -> str:
    if filename:
        try:
            ext = os.path.splitext(filename)[1].upper()
            if ext:
                ext = ext[1:]
            return ext
        except TypeError:
            pass

    return None
