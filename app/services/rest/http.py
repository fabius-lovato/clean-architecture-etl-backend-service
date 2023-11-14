from abc import ABC, abstractmethod
from typing import Any, List


class HttpKeyValue:
    def __init__(self, option: str, value: Any):
        self.__key = option
        self.__value = value

    @property
    def key(self) -> str:
        return self.__key

    @property
    def value(self) -> str:
        return self.__value

    def __str__(self):
        return f"{self.key}: {self.value}"

class HttpHeaderAbstraction(ABC):

    @abstractmethod
    def has(self, key: str) -> str:
        raise NotImplementedError("HttpHeader's has method not implemented!")

    @abstractmethod
    def get(self, key: str, default = None) -> str:
        raise NotImplementedError("HttpHeader's get method not implemented!")

    @abstractmethod
    def set(self, key: str, option_value: str) -> str:
        raise NotImplementedError("HttpHeader's set method not implemented!")

    @abstractmethod
    def remove(self, key: str) -> str:
        raise NotImplementedError("HttpHeader's remove method not implemented!")

    @abstractmethod
    def list(self) -> List[HttpKeyValue]:
        raise NotImplementedError("HttpHeader's remove method not implemented!")

class HttpParamsAbstraction(ABC):
    @abstractmethod
    def has(self, key: str) -> str:
        raise NotImplementedError("FastApiParams' has method not implemented!")

    @abstractmethod
    def get(self, key: str, default = None) -> str:
        raise NotImplementedError("FastApiParams' get method not implemented!")

    @abstractmethod
    def list(self) -> List[HttpKeyValue]:
        raise NotImplementedError("FastApiParams' remove method not implemented!")

class HttpFormDataAbstraction(ABC):

    @abstractmethod
    def has(self, key: str) -> str:
        raise NotImplementedError("HttpFormData's has method not implemented!")

    @abstractmethod
    def get(self, key: str, default = None) -> str:
        raise NotImplementedError("HttpFormData's get method not implemented!")

    @abstractmethod
    def set(self, key: str, option_value: str) -> str:
        raise NotImplementedError("HttpFormData's set method not implemented!")

    @abstractmethod
    def remove(self, key: str) -> str:
        raise NotImplementedError("HttpFormData's remove method not implemented!")

    @abstractmethod
    def list(self) -> List[HttpKeyValue]:
        raise NotImplementedError("HttpFormData's remove method not implemented!")

class HttpRequestAbstraction(ABC):

    @abstractmethod
    def header(self) -> HttpHeaderAbstraction:
        raise NotImplementedError("HttpRequest's header method not implemented!")

    @abstractmethod
    def query_params(self) -> HttpParamsAbstraction:
        raise NotImplementedError("HttpRequest's query_params method not implemented!")

    @abstractmethod
    def path_params(self) -> HttpParamsAbstraction:
        raise NotImplementedError("HttpRequest's url_params method not implemented!")

    @abstractmethod
    def body(self) -> bytes:
        raise NotImplementedError("HttpRequest's body method not implemented!")

    @abstractmethod
    def body_json(self) -> bytes:
        raise NotImplementedError("HttpRequest's body method not implemented!")

    @abstractmethod
    def form(self) -> HttpParamsAbstraction:
        raise NotImplementedError("HttpRequest's body method not implemented!")

class HttpResponseAbstraction(ABC):

    @abstractmethod
    def header(self) -> HttpHeaderAbstraction:
        raise NotImplementedError("HttpRequest's header method not implemented!")

    @abstractmethod
    def body(self) -> Any:
        raise NotImplementedError("HttpRequest's body.get() method not implemented!")

    @abstractmethod
    def set_body(self, data: bytes):
        raise NotImplementedError("HttpRequest's body.set method not implemented!")

    @abstractmethod
    def status_code(self) -> int | None:
        raise NotImplementedError("HttpRequest's status_code.get method not implemented!")

    @abstractmethod
    def set_status_code(self, data: int):
        raise NotImplementedError("HttpRequest's status_code.set method not implemented!")

class HttpError(Exception):
    def __init__(self, status_code: int, message: str = None):
        self.status_code = status_code
        self.message = message
