from http import HTTPStatus
from pydantic import BaseModel
import json

from app.domain.data_models.common import UseCaseResponse, ResponseSuccess, ResponseInvalidParam, ResponseUnauthorized, ResponseInternalError
from app.domain.data_models.common import ResponseResourceNotFound, ResponseNotAllowed
from app.domain.data_models.pix_batch_add_items_from_file_data_models import PixBatchAddItemsFromFileResponseError, PixBatchAddItemsFromFileResponseSuccess, PixBatchFileUploadInfo

from app.domain.usecases.pix.batch import PixBatchAddItemsFromFileParams, UploadFileParam
from app.main.rest.models.pix.batch.items_from_file_model import PixBatchFileConfigForAll, PixBatchFilePostResponse

from app.services.mappers.rest.rest_api_mapper import RestApiRequestMapper, RestApiResponseMapper
from app.services.rest.http import HttpRequestAbstraction, HttpResponseAbstraction


class PixBatchAddItemsFromFileMapper(RestApiRequestMapper):

    @classmethod
    def map(cls, request: HttpRequestAbstraction, body: PixBatchFileConfigForAll, batch_key: str | int = None,
            **kwargs) -> PixBatchAddItemsFromFileParams:

        obj = PixBatchAddItemsFromFileParams()
        obj.batch_id           = batch_key

        obj.file               = UploadFileParam(body.file.file, body.file.filename, body.file.size)
        obj.encoding           = body.encoding
        obj.file_type          = body.file_type
        obj.ignore_duplicates  = body.ignore_duplicated

        obj.quote_char         = body.quote_char
        obj.skip_initial_space = body.skip_initial_space

        if body.escape_char:
            try:
                obj.escape_char = body.escape_char.encode().decode('unicode_escape')
            except UnicodeDecodeError:
                obj.escape_char = body.escape_char

        if body.line_terminator:
            try:
                obj.line_terminator = body.line_terminator.encode().decode('unicode_escape')
            except UnicodeDecodeError:
                obj.line_terminator = body.line_terminator

        if body.delimiter:
            try:
                obj.delimiter = body.delimiter.encode().decode('unicode_escape')
            except UnicodeDecodeError:
                obj.delimiter = body.delimiter

        return obj


class PixBatchAddItemsFromFileMapperResponse(RestApiResponseMapper):

    @classmethod
    def map(cls, use_case_response: UseCaseResponse, response: HttpResponseAbstraction):

        status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
        body = None

        # TODO: O tratamento de tipos comuns de erros deve ser concentrado em uma classe ou método para evitar redundância de código desnecessária.
        if isinstance(use_case_response, ResponseSuccess):
            status_code, body = cls._map_on_success(use_case_response)

        elif isinstance(use_case_response, PixBatchAddItemsFromFileResponseError):
            status_code, body = cls._map_on_failure(use_case_response)

        elif isinstance(use_case_response, ResponseResourceNotFound):
            status_code, body = cls._map_on_not_found(use_case_response)

        elif isinstance(use_case_response, ResponseInvalidParam):
            status_code, body = cls._map_on_bad_request(use_case_response)

        elif isinstance(use_case_response, ResponseUnauthorized):
            status_code, body = cls._map_on_unauthorized(use_case_response)

        elif isinstance(use_case_response, ResponseNotAllowed):
            status_code, body = cls._map_on_not_allowed(use_case_response)

        elif isinstance(use_case_response, ResponseInternalError):
            status_code, body = cls._map_on_internal_server_error(use_case_response)


        response.set_status_code(status_code)
        if body:
            response.set_body(json.dumps(body))

    @classmethod
    def _map_on_success(cls, data: PixBatchAddItemsFromFileResponseSuccess) -> (int, BaseModel):

        # TODO: A geração da resposta em formato JSON deve ser movido para uma classe mapper adequada.
        body = {
            "file": {
                "name": data.file.name,
                "size": data.file.size,
                "type": data.file.type,
                "totalLines": data.file.total_lines
            },
            "total_count": data.total_count,
            "total_amount": data.total_amount
        }

        return (HTTPStatus.CREATED.value, body)

    @classmethod
    def _map_on_failure(cls, data: PixBatchAddItemsFromFileResponseError) -> (int, BaseModel):
        # TODO: Mover a responsabilidade de geração de resposta HTTP para uma classe mapper.
        body = {
            "file": {
                "name": data.file.name,
                "size": data.file.size,
                "type": data.file.type,
                "totalLines": data.file.total_lines
            },
            "totalErrorCount": data.total_error_count,
            "errors": []
        }

        for err in data.errors:
            body['errors'].append(
                {
                    "fileline": err.fileline,
                    "index": err.index,
                    "field": err.field,
                    "description": err.description
                }
            )

            # São reportados apenas os 100 primeiros erros para evitar problemas de comunicação por excesso de payload.
            # TODO: Modificar o comportamento dos READERs para parar o processamento do arquivo após encontrar n inconsistências.
            if len(body['errors']) >= 100:
                break

        return (HTTPStatus.PRECONDITION_FAILED.value, body)

    @classmethod
    def _map_on_not_found(cls, data: ResponseResourceNotFound) -> (int, BaseModel):
        if data.resource == 'batch_id':
            return (HTTPStatus.NOT_FOUND.value, None)

        #print('Resource not found ({data.resource})!')
        return (HTTPStatus.PRECONDITION_FAILED.value, None)

    @classmethod
    def _map_on_bad_request(cls, data: ResponseInvalidParam) -> (int, BaseModel):
        body = {
            "field": data.field,
            "message": data.msg,
            "detail": data.detail
        }
        return (HTTPStatus.BAD_REQUEST.value, body)

    @classmethod
    def _map_on_unauthorized(cls, data: ResponseUnauthorized) -> (int, BaseModel):
        return (HTTPStatus.UNAUTHORIZED.value, None)

    @classmethod
    def _map_on_not_allowed(cls, data: ResponseNotAllowed) -> (int, BaseModel):
        body = {
            "message": data.msg,
            "detail": data.detail
        }
        return (HTTPStatus.BAD_REQUEST.value, body)

    @classmethod
    def _map_on_internal_server_error(cls, data: ResponseInternalError) -> (int, BaseModel):
        return (HTTPStatus.INTERNAL_SERVER_ERROR.value, None)
