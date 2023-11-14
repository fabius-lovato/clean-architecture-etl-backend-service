from abc import ABC, abstractmethod
from typing import Any, Optional

from app.domain.data_models.common import UseCaseResponse


class UseCase(ABC):

    @abstractmethod
    def run(self, **kwargs: Optional[Any]) -> UseCaseResponse:
        raise NotImplementedError('Usecase runner not implemented!')
