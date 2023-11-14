from abc import ABC, abstractmethod
from typing import Any, Optional
from app.domain.data_models.common import UseCaseParams, ResponseInvalidParam


class ParamValidator(ABC):

    @abstractmethod
    def check(self, params: UseCaseParams, i18n: Optional[Any] = None) -> ResponseInvalidParam | None:
        raise NotImplementedError()
