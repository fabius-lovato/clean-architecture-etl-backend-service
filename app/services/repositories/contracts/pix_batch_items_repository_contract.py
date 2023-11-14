from abc import abstractmethod

from app.domain.entities.pix_batch_items_entity import PixBatchItemEntity


class PixBatchItemsRepositoryContract():
    @abstractmethod
    def get_pix_batch_item_by_id(self, pix_batch_item_id: str) -> PixBatchItemEntity | None:
        raise NotImplementedError()

    @abstractmethod
    def insert_pix_batch_item(self, pix_batch_id: int, pix_batch_item: PixBatchItemEntity) -> PixBatchItemEntity | None:
        raise NotImplementedError()
