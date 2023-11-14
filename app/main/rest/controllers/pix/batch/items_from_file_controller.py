from http import HTTPStatus
from fastapi import APIRouter, Request, Response, Depends, Path

from app.domain.data_models.common import ResponseInternalError, UseCaseResponse
from app.domain.usecases.pix.batch.add_items_from_file import PixBatchAddItemsFromFileParams
from app.main.factories.pix.batch.items_from_file_factory import pix_batch_items_file_post_factory
from app.main.rest.adapters.fastapi_adapter import FastApiRequestAdapter, FastApiResponseAdapter
from app.main.rest.mappers.pix_batch_add_items_from_file_mapper import PixBatchAddItemsFromFileMapper, PixBatchAddItemsFromFileMapperResponse

from app.main.rest.models import BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError, ServerInternalError
from app.main.rest.models.pix.batch.items_from_file_model import PixBatchFileConfigForAll, PixBatchFileErrorResponse, PixBatchFilePostResponse
from app.services.exceptions import DatabaseConnection


router = APIRouter(
    prefix='/pix/batch/{batch_key}/items/file',
    tags=["Pix em Lote"]
)

@router.post(
    path='',
    summary='Inserção de itens em um lote Pix existente através do upload de arquivo.',
    description='Este endpoint oferece suporte à inserção eficiente de múltiplos pagamentos Pix em um lote não processado.<br>' +
                'Ele fornece uma solução conveniente para adicionar vários pagamentos Pix de uma só vez por meio do upload de arquivos.<br>' +
                'Os clientes têm a flexibilidade de escolher entre vários formatos de arquivo, incluindo .CSV, .JSON, .XML e .YAML.<br>' +
                'Essa funcionalidade simplifica significativamente o processo de inclusão massiva de pagamentos Pix, tendo como foco a eficiência operacional.',
    status_code=HTTPStatus.CREATED.value,

    responses={
        HTTPStatus.CREATED.value: {
            "description": "Sucesso. Pagamentos Pix foram inseridos no lote.",
            'model': PixBatchFilePostResponse
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Os dados da requisição não atendem aos requisitos de obrigatoriedade, formatação e consistência.",
            'model': BadRequestError
        },
        HTTPStatus.UNAUTHORIZED.value: {
            "description": "Usuário não autorizado a efetuar essa operação.",
            'model': UnauthorizedError
        },
        HTTPStatus.FORBIDDEN.value: {
            "description": "Método de autenticação inválido ou transação não permitida.",
            'model': ForbiddenError
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "Lote Pix não encontrado.",
            'model': NotFoundError
        },
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            "description": "Encontrado inconsistências no arquivo de lote submetido.",
            'model': PixBatchFileErrorResponse
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "description": "Ocorreu um erro interno ao processar a requisição.",
            'model': ServerInternalError
        },
    }
)
def post(request: Request, response: Response,
         batch_key: str | int = Path(description='Chave de identificação do lote que receberá os pagamentos PIX.'),
         file_config: PixBatchFileConfigForAll = Depends(PixBatchFileConfigForAll.as_form)
        ) -> Response:

    use_case_response: UseCaseResponse = None
    # TODO: Processamento de uma requisição REST tende a ter sempre os mesmos passos:
    #   1º) Usa o adapter para abstrair a leitura dos dados da requisição;
    #   2º) Faz uso de um mapper específico para converter a DTO na estrutura de entrada do Use Case;
    #   3º) Faz uso de uma factory para instanciar e preparar a execução do Use Case apropriado;
    #   4º) Efetuo a execução do Use Case; e
    #   5º) Mapeia o retorno do Use Case para a respectiva resposta HTTP;
    # É recomendado a criação de um método ou classe para eliminar a redundância desses passos em todas as rotas da API.
    try:
        fastapi_request = FastApiRequestAdapter(request)
        fastapi_response = FastApiResponseAdapter(response)

        params: PixBatchAddItemsFromFileParams = PixBatchAddItemsFromFileMapper.map(fastapi_request, body=file_config, batch_key=batch_key)
        use_case = pix_batch_items_file_post_factory(params)

        use_case_response = use_case.run(params)
    except DatabaseConnection as e:
        # TODO: Logar informações referente ao erro.
        use_case_response = ResponseInternalError(msg=e.message)

        PixBatchAddItemsFromFileMapperResponse.map(use_case_response, e)

    # TODO: Fazer o tratamento dos demais tipos de excessões conhecidas.
    #except ...

    except Exception as e:
        # BUG: Essa é uma situação que não deveria ocorrer.
        use_case_response = ResponseInternalError(msg=e.__str__())

    try:
        PixBatchAddItemsFromFileMapperResponse.map(use_case_response, fastapi_response)
    except Exception as e:
        # BUG: Essa é uma situação que não deveria ocorrer.
        print("Erro desconhecido ao mapear dados de retorno do Use Case.")
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value

    return response



@router.put(path='')
def put(request: Request, response: Response) -> Response:
    fastapi_request = FastApiRequestAdapter(request)
    print(fastapi_request.body())
    print(fastapi_request.body_json())
