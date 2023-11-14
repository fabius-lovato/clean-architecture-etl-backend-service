from fastapi import FastAPI
from app.main.rest.config import config_openapi_doc, load_routes, config_exceptions

def prepare_rest_api_server() -> FastAPI:
    """
        Método responsável pela configuração e preparação do servidor REST utilizando a biblioteca FastAPI.
        A prepração/configuração inclui:
            - Carregar as rotas (controllers) da API;
            - Atribuir os handlers das exceptions;
            - Disponibilizar Swagger UI;
            - Disponibilizar ReDoc;
            - Configurar CORS;
            - ...
    """
    app = FastAPI()

    load_routes(app, start_path='app/main/rest/controllers', include_files=['.*_controller.py'], exclude_files=[])
    config_exceptions(app)
    config_openapi_doc(app, 'docs/swagger/openapi.yaml', encoding='utf-8')

    return app
