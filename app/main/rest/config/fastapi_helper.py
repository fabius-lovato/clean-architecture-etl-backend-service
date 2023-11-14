from http import HTTPStatus
import json
import os
import re
from typing import List, Any
from importlib import import_module

from fastapi import APIRouter, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from ruamel.yaml import YAML




def config_exceptions(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        print(f'Parâmetros inválidos: {exc}')

        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST.value,
            content=jsonable_encoder(
                {
                    'errors': [
                        {
                            'field': error['loc'],
                            'message': error['msg'],
                        }
                        for error in exc.errors()
                    ]
                }
            )
        )



def config_openapi_doc(app: FastAPI, file_path: str, encoding: str = 'UTF-8') -> None:
    """

    Args:
        app (FastAPI): _description_
    """
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding=encoding) as openapi_file:
            yaml = YAML(typ='safe', pure=True)
            app.openapi_schema = json.loads(json.dumps(yaml.load(openapi_file), default=str))


def __match_file_list(file_path: str, options: List[str]) -> bool:

    for op in options:
        if file_path.endswith(op):
            return True

        if re.search(op, file_path):
            return True

    return False

def __find_endpoints_modules(start_path: str,
                           include_files: List[str] = None,
                           exclude_files: List[str] = None) -> List[str]:
    """
        Lista todos os módulos python que atende a critérios de buscas.
        É utilizado para varregar recursivamente um diretório listando todos os arquivos python que possivelmente contém a definição de um
        endpoint/rota FastAPI.

    Args:
        start_path (str):        Path ou ponto inicial da pesquisa.
        include_files (List):    Lista opcional com o nome dos arquivos a serem considerados. Se especificado, irá considerar somente os arquivos
                                 que atende a pelo menos um dos patterns especificados.
                                 A listagem deve conter expressões regulares.
        exclude_files (List):    Lista opcional com os nomes dos arquivos a serem desconsiderados. Se especificado, qualquer arquivo que tenha
                                 o mesmo nome ou que atenda ao formato especificado nessa lista será descartado.

    Returns:
        List[str]: Retorna uma lista com os nomes dos módulos python que atende aos critérios de busca, já ordenados por ordem alfabética.
    """
    python_files = []
    for file_or_dir in os.listdir(start_path):
        current_path = f'{start_path}/{file_or_dir}'

        is_private = file_or_dir.startswith('__') or file_or_dir.endswith('__.py')
        if is_private:
            continue

        is_a_directory = os.path.isdir(current_path)
        if not is_a_directory:
            is_not_a_python_file = not file_or_dir.endswith('.py')
            if is_not_a_python_file:
                continue

            if include_files and not __match_file_list(current_path, include_files):
                continue

            if exclude_files and __match_file_list(current_path, exclude_files):
                continue

            module_name = current_path[:-3].replace('/', '.')
            python_files.append(module_name)
        else:
            new_modules = __find_endpoints_modules(start_path=current_path, include_files=include_files, exclude_files=exclude_files)

            python_files += new_modules

    return sorted(python_files)

def __load_modules(modules: List[str], ignore_exceptions: bool = False) -> List[APIRouter]:
    """
        Carrega uma lista de módulos python em busca de definições de Routers do FastAPI.
        Esse método efetua o carregamento dinâmico dos endpoints da aplicação que serão servidos pelo FastAPI.

    Args:
        modules (List[str]):      Lista com o nome de todos os módulos que devem ser carregados.
        ignore_exceptions (bool): Flag que permite ignorar excessões levantadas durante o carregamento dos módulos.

    Returns:
        List[APIRouter]: Retorna uma lista com todos os routers FastAPI encontrados.
    """
    fastapi_routers = []
    for module in modules:

        try:
            module_imported = import_module(module)

            vars = module_imported.__dir__()
            for attrname in vars:
                attr = getattr(module_imported, attrname)

                if not isinstance(attr, APIRouter):
                    continue

                fastapi_routers.append(attr)

        except ImportError as ex:
            if not ignore_exceptions:
                raise ex

    return fastapi_routers


def __check_str_list(param: Any, param_name: str) -> List[str] | None:
    if param is None:
        return None
    elif isinstance(param, str):
        param = [param]
    elif not isinstance(param, List):
        raise TypeError(f'Invalid type value assigned to the parameter {param_name}!')

    result = []
    if isinstance(param, List):
        for item in param:
            if item is not None:
                if not isinstance(item, str):
                    raise TypeError(f'Invalid type value assigned to the parameter {param_name}!')
                result.append(item)


    return result if len(result) > 0 else None

def load_routes(app: FastAPI,
                start_path: str | None,
                include_files: List[str] = None,
                exclude_files: List[str] = None,
                ignore_exceptions: bool = False):
    """
      Método que atua como um facilitador para carregar dinamicamente as controllers (routers) que deverão ser associadas ao servidor REST
      provido pelo FastAPI.
      Esse método flexibiliza quais rotas serão ou não carregadas, permitindo customizar a aplicação e oferecendo serviços específicos.

    Args:
        app (FastAPI):           Instância FastAPI do servidor REST que receberá as rotas.
        start_path (str):        Path ou ponto inicial onde as rotas/controladores estão localizados.
        include_files (List):    Lista, opcional, com o nome dos arquivos a serem considerados. Se especificado, somente os arquivos com os nomes
                                 listados é que serão carregados. Todos os demais serão descartados.
                                 É possível utilizar uma expressão regular e incluir diretórios. Ex: '/pix/.*/.*_file.py'
        exclude_files (List):    Lista, opcional, com os nomes dos arquivos a serem desconsiderados. Se especificado, qualquer arquivo que tenha
                                 o mesmo nome ou que atenda ao formato especificado nessa lista não será carregado.
        igore_exceptions (bool): Instrui o carregamento das rotas a ignorar arquivos que levantaram excessão ao sere carregados. Default False.
    """

    include_files = __check_str_list(include_files, 'include_files')
    exclude_files = __check_str_list(exclude_files, 'exclude_files')

    modules = __find_endpoints_modules(start_path, include_files, exclude_files)

    routes = __load_modules(modules, ignore_exceptions = ignore_exceptions)

    for router in routes:
        app.include_router(router)
