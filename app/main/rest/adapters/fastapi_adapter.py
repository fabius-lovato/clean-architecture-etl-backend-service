from typing import Any, Dict, List

import fastapi

from app.services.rest.http import HttpHeaderAbstraction, HttpKeyValue, HttpParamsAbstraction, HttpFormDataAbstraction, HttpRequestAbstraction
from app.services.rest.http import HttpResponseAbstraction


class FastApiHeaderAdapter(HttpHeaderAbstraction):
    def __init__(self, fastapi_headers: fastapi.datastructures.Headers):
        self.__fastapi_headers = fastapi_headers

    def has(self, key: str) -> bool:
        return key in self.__fastapi_headers

    def get(self, key: str, default = None) -> str | None:
        return self.__fastapi_headers.get(key, default)

    def set(self, key: str, option_value: str) -> str:
        self.__fastapi_headers[key] = option_value

    def remove(self, key: str) -> str:
        if key in self.__fastapi_headers:
            self.__fastapi_headers.pop(key)

    def list(self) -> List[HttpKeyValue]:
        headers = []
        for item in self.__fastapi_headers.items():
            option = HttpKeyValue(item[0], item[1])
            headers.append(option)

        return headers

class FastApiQueryParamsAdapter(HttpParamsAbstraction):
    def __init__(self, fastapi_query_params: fastapi.datastructures.QueryParams):
        self.fastapi_query_params = fastapi_query_params

    def has(self, key: str) -> bool:
        return key in self.fastapi_query_params

    def get(self, key: str, default = None) -> str | None:
        return self.fastapi_query_params.get(key, default)

    def list(self) -> List[HttpKeyValue]:
        params = []
        for item in self.fastapi_query_params.items():
            option = HttpKeyValue(item[0], item[1])
            params.append(option)

        return params

class FastApiPathParamsAdapter(HttpParamsAbstraction):
    def __init__(self, fastapi_path_params: Dict):
        self.fastapi_path_params = fastapi_path_params

    def has(self, key: str) -> bool:
        return key in self.fastapi_path_params

    def get(self, key: str, default = None) -> str | None:
        return self.fastapi_path_params.get(key, default)

    def list(self) -> List[HttpKeyValue]:
        params = []
        for item in self.fastapi_path_params:
            option = HttpKeyValue(item, self.fastapi_path_params[item])
            params.append(option)

        return params

class FastApiFormDataAdapter(HttpFormDataAbstraction):
    def __init__(self, fastapi_form_data: fastapi.datastructures.FormData):
        self.fastapi_form_data = fastapi_form_data

    def has(self, key: str) -> bool:
        return key in self.fastapi_form_data

    def get(self, key: str, default = None) -> str | None:
        return self.fastapi_form_data.get(key, default)

    def set(self, key: str, option_value: str) -> str:
        self.fastapi_form_data[key] = option_value

    def remove(self, key: str) -> str:
        if key in self.fastapi_form_data:
            self.fastapi_form_data.pop(key)

    def list(self) -> List[HttpKeyValue]:
        params = []
        for item in self.fastapi_form_data:
            option = HttpKeyValue(item, self.fastapi_form_data[item])
            params.append(option)

        return params

class FastApiRequestAdapter(HttpRequestAbstraction):

    def __init__(self, fastapi_request: fastapi.Request):
        self.__original     = fastapi_request
        self.__headers      = FastApiHeaderAdapter(fastapi_request.headers)
        self.__query_params = FastApiQueryParamsAdapter(fastapi_request.query_params)
        self.__path_params  = FastApiPathParamsAdapter(fastapi_request.path_params)
        self.__form         = FastApiFormDataAdapter(fastapi_request._form)

    def header(self) -> HttpHeaderAbstraction:
        return self.__headers

    def query_params(self) -> HttpParamsAbstraction:
        return self.__query_params

    def path_params(self) -> HttpParamsAbstraction:
        return self.__path_params

    def body(self) -> bytes:
        return self.__original.body()

    def body_json(self) -> Dict:
        return self.__original.json()

    def form(self) -> HttpParamsAbstraction:
        return self.__form


class FastApiResponseAdapter(HttpResponseAbstraction):

    def __init__(self, fastapi_response: fastapi.Response):
        self.__original     = fastapi_response
        self.__headers      = FastApiHeaderAdapter(fastapi_response.headers)

    def header(self) -> HttpHeaderAbstraction:
        return self.__headers

    def body(self) -> bytes:
        return self.__original.body()

    def set_body(self, data: Any):
        if not isinstance(data, str):
            data = str(data)
        self.__original.body = bytes(data, 'utf-8')

    def status_code(self) -> int | None:
        return self.__original.status_code

    def set_status_code(self, code: int):
        self.__original.status_code = code
