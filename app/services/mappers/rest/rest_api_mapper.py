from abc import ABC, abstractmethod
from typing import Any, Optional

from app.domain.data_models.common import UseCaseParams, UseCaseResponse
from app.services.rest.http import HttpRequestAbstraction, HttpResponseAbstraction



class RestApiRequestMapper(ABC):
    @classmethod
    @abstractmethod
    def map(cls, request: HttpRequestAbstraction, body: Optional[Any], **kwargs) -> UseCaseParams:
        raise NotImplementedError('Rest API request mapper not implemented!')


class RestApiResponseMapper(ABC):
    @classmethod
    @abstractmethod
    def map(cls, use_case_response: UseCaseResponse, response: HttpResponseAbstraction):
        raise NotImplementedError('Rest API response mapper not implemented!')
