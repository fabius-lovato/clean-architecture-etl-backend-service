from abc import abstractmethod

from app.domain.entities.pix_batch_entity import PixBatchEntity


class PixBatchRepositoryContract():
    @abstractmethod
    def get_pix_batch_by_id(self, pix_batch_id: str | int) -> PixBatchEntity | None:
        raise NotImplementedError()

    @abstractmethod
    def update_pix_batch_total(self, pix_batch_id: str | int, total_items: int, total_amount: float) -> PixBatchEntity | None:
        raise NotImplementedError()
